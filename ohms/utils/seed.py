#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>

def get_seed(student_id):
    seed = ''.join(str(ord(x)-48)[-1] for x in student_id) # should use SUID?
    return int(seed)
