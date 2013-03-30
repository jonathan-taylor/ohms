#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
#  Copyright (c) 2012-2013, Praveen Bommannavar <bommanna@stanford.edu>

import os,sys
from ohms.utils.login import client
from ohms.utils.seed import get_seed
from ohms.answer import Answer
from ohms.config import GRADEBOOK_NAME
from datetime import datetime, timedelta

def import_homework(hw_id):
    """
    import the homework object
    """
    try:
        _tmp = __import__(name="ohms.homeworks."+hw_id,fromlist=['homework'])
        return _tmp.homework
    except:
        return None

def fetch_hw_ids(hw_name,q_id):
    """
    get spreadsheet and worksheet ID's corresponding to homework and question
    """
    from ohms.utils.ids import ids
    try:
        sp_data = ids[hw_name]
        sp_id = sp_data["sp_id"]
        wk_id = sp_data["wk_ids"][q_id]
        return sp_id, wk_id
    except:
        print "Status: 403 Forbidden\n"
        sys.exit()

def fetch_worksheet(sp_id,wk_id):
    spreadsheet = client.GetDatabases(spreadsheet_key=sp_id)[0]
    return spreadsheet.GetTables(worksheet_id=wk_id)[0]

def fetch_responses(student_id,sp_id,wk_id):
    worksheet = fetch_worksheet(sp_id,wk_id)
    records = worksheet.FindRecords("id == %s" % student_id)
    return records

def get_hw_list():
    # get path to OHMS package
    ohms_dir = os.path.dirname(__file__)
    # iterate over homeworks in directory
    from pkgutil import iter_modules
    hw_list = []
    for hw_id in [name for _,name,_ in iter_modules([ohms_dir+'/homeworks'])]:
        homework = import_homework(hw_id)
        hw_list.append((homework.due_date, {
                    "id": hw_id,
                    "name": homework.name,
                    "due_date": homework.due_date.strftime('%m/%d/%Y %H:%M:%S')
                    }))
    # sort the list by due date
    hw_list.sort(key=lambda x: x[0])
    return { "hw_list": [x[1] for x in hw_list] }

def get_homework(student_id,hw_id,student_name=""):
    # import the appropriate homework
    homework = import_homework(hw_id)
    if not homework:
        print "Status: 404 Not Found\n"
        sys.exit()
    # set the seed
    seed = get_seed(student_id)
    # initialize questions
    questions = [q(seed) for q in homework.questions]
    # extract name and body from each question
    qs = [{
            "name":q.name,
            "data":q.to_JSON(solution=False),
            } for q in questions]
    # return homework name and question data
    return {
        "student_name": student_name,
        "name": homework.name,
        "text": homework.text,
        "due_date" : homework.due_date.strftime("%m/%d/%Y %H:%M:%S"), 
        "questions": qs 
        }

def get_solutions(student_id,hw_id):
    # import the appropriate homework
    hw = import_homework(hw_id)
    if not hw:
        print "Status: 404 Not Found\n"
        sys.exit()
    # check that due date has not passed
    curr_time = datetime.now()
    if curr_time < hw.due_date:
        print "Status: 401 Unauthorized\n"
        sys.exit()
    # set the seed
    seed = get_seed(student_id)
    # initialize questions
    questions = [q(seed) for q in hw.questions]
    # extract name, body, solutions from each question
    qs = [{
            "name":q.name,
            "data":q.to_JSON(solution=True),
            } for q in questions]
    # return homework name and question data
    return {
        "name": hw.name, 
        "due_date" : hw.due_date.strftime("%m/%d/%Y %H:%M:%S"), 
        "questions": qs,
        }


def get_response(student_id,hw_id,q_id):
    # import the appropriate homework and question
    hw = import_homework(hw_id)
    q = hw.questions[q_id](0) # use student seed instead of 0 here?
    # fetch spreadsheet and worksheet ID's for Google doc
    sp_id,wk_id = fetch_hw_ids(hw.name,q_id)
    # query worksheet for all entries with given student_id
    responses = fetch_responses(student_id,sp_id,wk_id)
    # if student has yet to submit a response, exit
    if not responses:
        return None
    # otherwise, fetch data from most recent response
    last = responses[-1].content
    n_parts = len(q.answers)
    answers = [last['ans%d' % i] for i in range(n_parts)]
    comments = [last['comment%d' % i] for i in range(n_parts)]
    points_raw = [last['score%d' % i] for i in range(n_parts)]
    points = {
        "earned": sum(float(x) for x in points_raw if x),
        "graded": sum(q.max_pts[i] for i,x in enumerate(points_raw) if x),
        "total": sum(q.max_pts)
        }
    # get timestamp of last 2 entries if they exist
    last_time = last['timestamp']
    last_last_time = responses[-2].content['timestamp'] if len(responses)>1 else None
    # return response data for question
    return {
        "last_last_time" : last_last_time,
        "last_time" : last_time,
        "answers" : answers,
        "points" : points,
        "comments" : comments,
        }

def submit_response(answers,student_id,hw_id,q_id):
    # import the appropriate homework and question
    hw = import_homework(hw_id)
    q = hw.questions[q_id](get_seed(student_id))
    # check that deadline has not passed
    curr_time = datetime.now()
    if curr_time > hw.due_date:
        print "Status: 410 Deadline Passed\n"
        sys.exit()
    # fetch spreadsheet and worksheet ID's for Google doc
    sp_id,wk_id = fetch_hw_ids(hw.name,q_id)
    # query worksheet for all entries with given student_id
    responses = fetch_responses(student_id,sp_id,wk_id)
    # check if user has submitted 2 entries in last 6 hours
    if len(responses) > 1:
        last_last_time = responses[-2].content['timestamp']
        last_last_time = datetime.strptime(last_last_time,'%m/%d/%Y %H:%M:%S')
        if curr_time < last_last_time + timedelta(hours=6):
            print "Status: 423 Locked\n"
            sys.exit()
    # validate answer by calling "check" method of question
    try:
        output = q.check(answers,student_id)
    except:
        print "Status: 400 Bad Request\n"
        sys.exit()
    scores = output["scores"]
    comments = output["comments"]
    # package new response and submit it
    new_response = {
        "id": student_id,
        "timestamp": curr_time.strftime("%m/%d/%Y %H:%M:%S")
        }
    for i,ans in enumerate(answers):
        new_response['ans%d' % i] = unicode(ans)
        new_response['score%d' % i] = str(scores[i])
        new_response['comment%d' % i] = unicode(comments[i])
    worksheet = fetch_worksheet(sp_id,wk_id)
    worksheet.AddRecord(new_response)
    # calculate the total points per question
    points = {
        "earned": sum(float(x) for x in scores if x),
        "graded": sum(q.max_pts[i] for i,x in enumerate(scores) if type(x)
                      in [int,float]),
        "total": sum(q.max_pts)
        }
    # return response data
    return {
        "last_last_time" : responses[-1].content['timestamp'] if responses else None,
        "last_time" : new_response["timestamp"],
        "points" : points,
        "comments" : comments
        }
            
def get_grades(student_id):
    """
    Retrieve grades for student from gradebook.
    """
    sp_id,wk_id = fetch_hw_ids(GRADEBOOK_NAME,0)
    grades = fetch_responses(student_id,sp_id,wk_id)
    maximum = fetch_responses("MAX",sp_id,wk_id)
    if not grades:
        return {}
    homeworks = []
    for hw, max_pts in maximum[0].content.iteritems():
        if max_pts and hw != "id":
            score = grades[0].content[hw]
            homeworks.append({
                    "homework": hw,
                    "score": score,
                    "max": max_pts
                    })
    return { "grades": homeworks }


