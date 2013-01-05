#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>

import random
import re

class Answer(object):

    expected_type = unicode

    def cast(self,response):
        try:
             return self.expected_type(response)
        except:
             if self.expected_type==int: return -1
             else: return self.expected_type("inf")        

class String(Answer):

    def cast(self,response):
        return super(String,self).cast(response.rstrip())


class NumberAnswer(Answer):

    def cast(self,response):
        response = response.replace(" ","")
        out = re.match("[^\d.-]*(-?[\d.]+)",response)
        if out:
            return super(NumberAnswer,self).cast(out.groups()[0])
        else:
            return super(NumberAnswer,self).cast("")

class Integer(NumberAnswer):
    expected_type = int
    

class Float(NumberAnswer):
    expected_type = float
        

class TrueFalseAnswer(Answer):
    expected_type = unicode

class Text(Answer):
    expected_type = unicode

class MultipleChoiceAnswer(Answer):
    expected_type = int
    compact = False

    def __init__(self,choices):
        self.choices = choices

