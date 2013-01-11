=========================================
 OHMS: Online Homework Management System
=========================================

Introduction
============

This package provides the code necessary to deploy an 
online homework system on Stanford's AFS servers. 
Check out a demo [here](http://www.stanford.edu/~dlsun/ohms/).


Code Overview
=============

The code is organized into three directories:

1. WWW/ contains the HTML, CSS, and Javascript code.
2. cgi-bin/ contains a routing script that handles 
   incoming client-side requests and calls the 
   appropriate Python routines.
3. ohms/ contains the Python package that does most 
   of the server-side processing.


Dependencies
============

First, the code assumes that the script resides on 
Stanford's AFS servers so that the pages are 
protected by WebAuth, so that the user is required 
to login with their SUNet ID and this information 
is passed to the server. 

The only software dependencies are:
- Python 2.7 (already installed on Stanford AFS)
- GData Python Client (see Installation section below)


Configuration
=============

The cgi-bin/ohms/ and WWW/ directories come with 
.htaccess files which allow access to anyone in the 
Stanford community. To restrict access to your class 
roster, copy the .htaccess file in the WWW/restricted 
directory of your AFS course website.

Other than this, there are three configuration files  
that may need to be edited:

1. ohms/config.py MUST be edited with the details of 
   your Google account (so that data can be read/written).

2. PATH_TO_OHMS in cgi-bin/ohms/route.cgi only needs to 
   be edited if you plan to install OHMS somewhere other 
   than the default location (see Installation section 
   below).

3. ROUTE_FILE in WWW/js/namespace.js only needs to be 
   edited if you plan to install the WWW files to 
   somewhere other than WWW/ohms/ and the cgi-bin files 
   to somewhere other than cgi-bin/ohms/.


Installation
============

NOTE: The "user" which processes the CGI scripts 
takes the root directory of the web server as its home 
(i.e., ~/). For example, for the course Stats 60, ~/ 
would correspond to /afs/ir/class/stats60. Hereafter, 
we will refer to this directory as $HOME, although note 
that if you are logged into AFS as yourself, $HOME may 
already be set to your user home directory.

NOTE: The CGI "user" may not have permissions to execute 
scripts in $HOME. Make sure you give it the appropriate 
permissions by executing "fs sa ... rlidwka". Contact 
HelpSU if you have any questions about this.

Follow these steps to install OHMS:

1. Install GData Python client. Download the files and 
   run the setup script to install. We recommend that 
   your install to $HOME/local, i.e. run the command:
   python setup.py install --home=$HOME/local.

2. Install OHMS Python package. Simply copy the ohms/ 
   directory to $HOME/local/lib/python/. We also 
   recommend that you copy ohms_admin.py to the 
   same directory. This contains the utilities for 
   generating databases, computing student's scores, etc.

3. Copy the contents of the cgi-bin/ directory to 
   $HOME/cgi-bin/.

4. Copy the contents of the WWW/ directory to 
   $HOME/WWW/ohms (recommended).

You should be all ready to go! The homework files are 
located in the homeworks/ directory of the OHMS Python 
package (i.e., $HOME/local/lib/python/ohms/homeworks). 
If you write a file, it should automatically show up 
when you point your web browser to OHMS. Right now, 
only the example homeworks should show up.


Setup
=====

Unfortunately, you still won't be able to submit any 
answers to homeworks because the database is not 
set up yet. To do this, go to $HOME/local/lib/python 
and run 

python ohms_admin.py

Choose Option 2 and type in Example_Homework. This 
will set up a database for Example_Homework in 
your Google Drive account (check for yourself!). 
Once the setup is complete, you should be able to 
submit responses for Example_Homework to the 
spreadsheet. Repeat for Example_Homework_2 and for 
any homeworks that you may write.



