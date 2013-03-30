#!/usr/bin/python

#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>

# add OHMS package location to python path
import os, sys, cgi, json
from datetime import datetime
PATH_TO_OHMS = os.path.expanduser("~/local/lib/python/")
sys.path.insert(0, PATH_TO_OHMS)
import ohms.web as web

# check whether user is logged in
student_id = os.environ.get("WEBAUTH_USER")
student_name = os.environ.get("WEBAUTH_LDAP_DISPLAYNAME")
referer = os.environ.get("HTTP_REFERER")
if student_id==None or referer==None:
    print "Status: 401 Unauthorized\n"
    sys.exit()
else:
    referer = os.path.basename(referer)

data = {
    "student_name": student_name,
    "current_time": datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
}

# routes depending on the refering page
if referer in ["index.html",""]:
    data.update(web.get_hw_list())
    print 'Content-Type: application/json\n'
    print json.dumps(data)

elif referer[:9]=="view.html":
    hw_id = referer.split("?")[-1][3:]
    post_vars = cgi.FieldStorage()
    action = post_vars.getvalue("action") 
    if action=="load_homework":
        data.update(web.get_homework(student_id,hw_id,student_name))
    elif action=="load_response":
        q_id = int(post_vars.getvalue("q_id")[1:])
        tmp = web.get_response(student_id,hw_id,q_id)
        if tmp: data.update(tmp)
    elif action=="submit_response":
        answers = post_vars.getlist("answers")
        q_id = int(post_vars.getvalue("q_id")[1:])
        data.update(web.submit_response(answers,student_id,hw_id,q_id))
    else:
        print "Status: 400 Bad Request \n"
        sys.exit()
    print 'Content-Type: application/json\n'
    print json.dumps(data)

elif referer[:9]=="sols.html":
    hw_id = referer.split("?")[-1][3:]
    data.update(web.get_solutions(student_id,hw_id,student_name))
    print 'Content-Type: application/json\n'
    print json.dumps(data)

elif referer=="grades.html":
    data.update(web.get_grades(student_id))
    print 'Content-Type: application/json\n'
    print json.dumps(data)
