#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>

import os,sys
import ohms
from ohms.utils.login import client
from ohms.config import GRADEBOOK_NAME

def get_homework():
    print '''\nPlease type the name of the Python module that contains 
the OHMS assignment.

For example, to create a database for Homework_1.py, type: Homework_1'''
    hw_id = raw_input()
    if hw_id[-3:]==".py": hw_id = hw_id[:-3]
    try:
        _tmp = __import__(name="ohms.homeworks."+hw_id,fromlist=['homework'])
        return _tmp.homework, hw_id
    except ImportError:
        print '''\nNo homework module with the specified name was found. 
Is it in the homeworks/ directory?'''
        sys.exit()

def create_database(homework):
    # create spreadsheet
    print '\nCreating database...'
    spreadsheet = client.CreateDatabase(homework.name)

    # create homework questions
    for (i,q) in enumerate(homework.questions):
        print 'Creating Question %d...' % (i+1)
        fields = ['id','timestamp']
        for j in range(q(0).num_answers):
            fields.extend(['ans%d' % j,'score%d' % j,'comment%d' % j])
        spreadsheet.CreateTable('Question%d' % (i+1),fields)

        # clean up by deleting Sheet1 that was created by default
    print 'Cleaning up...'
    spreadsheet.GetTables(name='Sheet 1')[0].Delete()
    
def update_grades():
    print '\nFetching grades and homework spreadsheets....'
    homework,hw_id = get_homework()
    hw_db = client.GetDatabases(name=homework.name)[0]
    grades_db = client.GetDatabases(name=GRADEBOOK_NAME)[0]
    grades = grades_db.GetTables(name="")[0]
    records = grades.FindRecords("")

    # fetch homework name and if not in gradebook, add it 
    hw_name = "".join(ch for ch in hw_id.lower() if ch.isalnum())
    grades.LookupFields() # this sets grades.fields
    if hw_name not in grades.fields:
        print 'Adding entry for %s in gradebook...' % hw_name
        grades.fields.append(hw_name)
        grades.SetFields(grades.fields)

    print 'Getting records...'
    # for each student
    for record in records:
        student_id = record.content['id']
        score = 0
        # calculate point value of entire assignment
        if student_id=='MAXIMUM':
            for i,question in enumerate(homework.questions):
                score += sum(question(0).max_pts)
        # otherwise calculate student's score
        else:
            for i,question in enumerate(homework.questions):
                q = hw_db.GetTables(name='Question%d' % (i+1))[0]
                submissions = q.FindRecords('id==%s' % student_id)
                if submissions:
                    for j in range(len(question(0).max_pts)):
                        q_score = submissions[-1].content['score%d' % j]
                        score += float(q_score if q_score else 0)
        # write the grade into the gradebook
        if score:
            print 'Score for %s: %i' % (student_id, score)
            record.content[hw_name] = str(score)
            record.Push()
        else:
            print 'Omitting for %s' % student_id
        
def update_ids():
    print "\nExtracting the ID of each spreadsheet..."
    spreadsheets = client.GetDatabases(name="")
    sp_dict = {}
    for sp in spreadsheets:
        sp_name = sp.entry.title.text
        sp_type,sp_id = sp.entry.resourceId.text.split(":")
        if sp_type != "spreadsheet":
            continue
        print "%s\t\tID: %s" % (sp_name,sp_id)
        worksheets = sp.GetTables(name="")
        wk_ids = [wk.entry.id.text.split("/")[-1] for wk in worksheets]
        sp_dict[sp_name] = {
            "sp_id": sp_id,
            "wk_ids": wk_ids
            }
    location = os.path.dirname(ohms.__file__)
    print "\nNow writing IDs to %s..." % location
    file(location + '/utils/ids.py','w').write("ids = " + repr(sp_dict))

def main(argv=None):
    print '''What would you like to do today?

(1) Tally grades for an OHMS assignment and write to gradebook.
(2) Create a database for an OHMS assignment.
(3) Update local copy of database ID's for an OHMS assignment.

Please enter a number.
'''
    try:
        choice = int(raw_input())
    except:
        print "\nYour selection was not understood. Please try again."
        sys.exit()

    if choice==1:
        update_grades()
    elif choice==2:
        homework,_ = get_homework()
        create_database(homework)
        update_ids()
    elif choice==3:
        update_ids()
    else:
        print "Your selection was not understood. Please try again."
        sys.exit()

    print '\nDone!'
    sys.exit()

if __name__ == "__main__":
    main()

    
