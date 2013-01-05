#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>

from ohms.config import PATH_TO_GDATA,GMAIL_EMAIL,GMAIL_PW
import sys
sys.path.insert(0,PATH_TO_GDATA)
from gdata.spreadsheet.text_db import Database,DatabaseClient

client = DatabaseClient(GMAIL_EMAIL,GMAIL_PW)




