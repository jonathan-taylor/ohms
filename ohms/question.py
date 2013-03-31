#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>

import random
from ohms.config import FILE_UPLOAD_DIR
import os

class Homework(object):

    def __init__(self,name,questions,due_date,text=""):
        self.name = name
        self.text = text
        self.questions = questions
        self.due_date = due_date

class Question(object):

    name = ""
    parts = []
    solution = ""
    submits_allowed = 2   # submissions allowed before lockout 
    lockout_period = 6    # time of lockout period (in hours)

    def to_JSON(self,solution=False):
        data = {
            "text": self.text,
            "max_pts": self.max_pts
            }
        if solution: data['solution'] = {
            "text": self.solution
            }
        return data

        return None

    def set_seed(self,seed):
        """
        Set the seed, this should be called in the constructor 
        of all subclasses
        """
        self.seed = seed
        random.seed(seed)
        
    def check(self,responses,student_id=None):
        """
        Check answers, returning a dict of scores and comments
        """
        return None


class MultiPartQuestion(Question):
    """
    Question with multiple parts (which are themselves questions)
    """
    text = ""   # introductory text (optional)
    parts = []  # each part is itself a question object
    list_type = "a"

    def __init__(self,seed):
#        self.set_seed(seed)
        self.active_parts = []
        self.num_answers = 0
        self.max_pts = []
        for i,part in enumerate(self.parts):
            self.active_parts.append(part(seed))
            self.max_pts.extend(self.active_parts[i].max_pts)
            self.num_answers += self.active_parts[i].num_answers

    def to_JSON(self,solution=False):
        data = {
            "text": self.text,
            "parts": [p.to_JSON(solution) for p in self.active_parts],
            "list_type": self.list_type
            }
        if solution: data['solution'] = {}
        return data

    def check(self,responses,student_id=None):
        scores = []
        comments = []
        end = 0
        for i, part in enumerate(self.active_parts):
            # extract responses corresponding to current part
            start = end
            end = start + part.num_answers
            resp = responses[start:end]
            # call the check method for that part
            out = part.check(resp)
            scores.extend(out['scores'])
            comments.extend(out['comments'])
            # write any changes to the answer back
            responses[start:end] = resp
        return { "scores": scores, "comments": comments }


class ShortAnswer(Question):
    """
    Basic open-ended short answer question.
    """
    # subclasses should override these class attributes
    text = ""
    max_pts = [1]
    solution = ""

    def __init__(self,seed):
        self.num_answers = 1
    
    def to_JSON(self,solution=False):
        data = {
            "type": "ShortAnswer",
            "text": self.text,
            "max_pts": self.max_pts[0],
            }
        if solution: data['solution'] = {"text": self.solution}
        return data

    def check(self,responses,student_id=None):
        return {"scores": [""], "comments": [""]}


class LaTeXAnswer(ShortAnswer):

    def to_JSON(self,solution=False):
        data = {
            "type": "LaTeXAnswer",
            "text": self.text,
            "max_pts": self.max_pts[0],
            }
        if solution: data['solution'] = {"text": self.solution}
        return data


class TrueFalse(Question):
    """
    Basic True/False question
    """
    # subclasses should override these class attributes
    text = ""
    answer = ""
    comment_if_wrong = ""
    max_pts = [1]
    solution = ""

    def __init__(self,seed):
        self.num_answers = 1

    def to_JSON(self,solution=False):
        data = {
            "type": "TrueFalse",
            "text": self.text,
            "max_pts": self.max_pts[0],
            }
        if solution: data['solution'] = {
            "answer": self.answer, 
            "text": self.solution,
            }
        return data


    def check(self,responses,student_id=None):
        if responses[0] not in ["T","F"]:
            responses[0] = ""
            return { "scores": [0], "comments": [""] }
        else:
            # check the true/false question
            score = (responses[0]==self.answer.upper())*self.max_pts[0]
            comment = self.comment_if_wrong if not score else ""
            return { "scores": [score], "comments": [comment] }


class TrueFalseWithExplanation(MultiPartQuestion):
    """
    Basic True/False question with explanation
    """
    text = ""
    answer = ""
    comment_if_wrong = ""
    max_pts = [1,1]
    solution = ""
    list_type = ""

    def __init__(self,seed):
        class TrueFalsePart(TrueFalse):
            answer = self.answer
            comment_if_wrong = self.comment_if_wrong
            max_pts = [self.max_pts[0]]
        class ExplanationPart(ShortAnswer):
            max_pts = [self.max_pts[1]]
            solution = self.solution

        self.parts = [TrueFalsePart, ExplanationPart]

        super(TrueFalseWithExplanation,self).__init__(seed)


class MultipleChoice(Question):
    """
    Basic multiple choice question with one correct answer
    """
    # subclasses should override these class attributes
    text = ""
    choices = []
    comments_by_choice = [] # comment to return depending on user choice
    answer = None # should be index of "choices" array
    max_pts = [1]
    solution = ""
    compact = False

    def __init__(self,seed):
#        self.set_seed(seed)
        self.num_answers = 1

    def to_JSON(self,solution=False):
        data = {
            "type": "MultipleChoice",
            "text": self.text,
            "choices": self.choices,
            "max_pts": self.max_pts[0],
            "compact": self.compact
            }
        if solution: data['solution'] = {
            "answer": self.answer, 
            "text": self.solution,
            }
        return data

    def check(self,responses,student_id=None):
        try:
            response = int(responses[0])
        except:
            responses[0] = ""
            return {"scores": [0], "comments": [""]}
        response = int(responses[0])
        score = self.max_pts[0] * (response==self.answer)
        if self.comments_by_choice:
            comment = self.comments_by_choice[response]
        else:
            comment = ""
        return {"scores": [score], "comments": [comment]}
        
class MultipleChoiceWithExplanation(MultiPartQuestion):
    """
    Basic multiple choice question also requiring explanation
    """
    # subclasses should override these class attributes
    text = ""
    choices = []
    comments_by_choice = []
    answer = None # should be index of "choices" array
    max_pts = [1,1]
    solution = ""
    compact = False # whether or not to display choices in compact form

    def __init__(self,seed):
        class MultipleChoicePart(MultipleChoice):
            choices = self.choices
            comments_by_choice = self.comments_by_choice
            answer = self.answer
            max_pts = [self.max_pts[0]]
            compact = self.compact
        class ExplanationPart(ShortAnswer):
            max_pts = [self.max_pts[1]]
            solution = self.solution

        self.parts = [MultipleChoicePart, ExplanationPart]

        super(MultipleChoiceWithExplanation,self).__init__(seed)


class MultipleResponse(Question):
    """
    Basic multiple choice question with multiple correct answers
    """
    # subclasses should override these class attributes
    text = ""
    choices = []
    answer = None # should be string of ordered indices of choices array, separated by commas
    max_pts = [1]
    solution = ""
    compact = False

    def __init__(self,seed):
#        self.set_seed(seed)
        self.num_answers = 1

    def to_JSON(self,solution=False):
        data = {
            "type": "MultipleResponse",
            "text": self.text,
            "choices": self.choices,
            "max_pts": self.max_pts[0],
            "compact": self.compact
            }
        if solution: data['solution'] = {
            "answer": self.answer, 
            "text": self.solution,
            }
        return data

    def check(self,responses,student_id=None):
        score = self.max_pts[0] * (responses[0]==self.answer)
        return {"scores": [score], "comments": [""]}



class FillInTheBlank(Question):
    """
    Basic fill-in-the-blank question.

    Class Attributes:
    text - the text of the question, with 4 underscores (____) indicating 
           where the blanks should go (Default value: "")
    is_string - boolean indicating whether or not to expect strings or
                floats in the blanks (Default value: True)
    answer - a list where each element is a list containing the 
             acceptable answers.
             Each acceptable answer can be specified either as:
               - string/number: specifies a correct answer
               - tuple: specifies range of acceptable answers (numbers only)
    exact_match - boolean indicating whether to require exact match or 
                  to require loose match (defined below) (Default: True)
    max_pts - a list containing the point value of each blank
    solution - a string containing the solution (Default value: "")

    Note: A loose match is defined to be that the answer is contained in
    the user response (in the case of strings) or that the user response 
    is close (within 5%) of the answer (in the case of floats)
    """

    text = ""
    is_string = True
    answer = []
    exact_match = True
    max_pts = []
    solution = ""

    def __init__(self,seed):
        # first create an array with 
        self.body = self.text.split("____")
        # insert an input box between every element of the list
        self.num_answers = len(self.body)-1
        j = 0
        while 2*j+1 < len(self.body):
            self.body.insert(2*j+1,{
                    "type": "String" if self.is_string else "Float",
                    "max_pts": self.max_pts[j]
                    })
            j += 1

    def to_JSON(self,solution=False):
        data = {
            "type": "FillInTheBlank",
            "body": self.body,
            "max_pts": self.max_pts
            }
        if solution: data['solution'] = {
            "answer": self.answer, 
            "text": self.solution,
            }
        return data

    def check(self,responses,student_id=None):
        # calculate the score for each blank
        scores = []
        comments = []
        for i, response in enumerate(responses):

            # casting
            if self.is_string:
                response = unicode(response.rstrip())
            else:
                response = float(response) if response else float('inf')

            # if exact match, check that response is one of accepted answers
            if self.exact_match:
                score = (response in self.answer[i])*self.max_pts[i]
            # otherwise, if only loose match required...
            else:
                score = 0
                # for strings, check if answer keyword is contained in student response
                if self.is_string:
                    for keyword in self.answer[i]:
                        if keyword in response:
                            score = self.max_pts[i]
                            break
                # for floats...
                else:
                    # iterate over the acceptable answers
                    for poss_answer in self.answer[i]:
                        # if possible answer is a range, i.e. tuple (a,b)
                        if type(poss_answer)==tuple:
                            # check whether response is in the range (a,b)
                            if response >= poss_answer[0] and \
                                    response <= poss_answer[1]:
                                score = self.max_pts[i]
                                break
                        # if possible answer is a single value
                        else:
                            # check if response is within 5% of correct
                            if poss_answer and abs(1.*(response-poss_answer)/poss_answer) <= .05:
                                score = self.max_pts[i]
                                break
                            # if true response is 0, check if response is
                            # < .01
                            elif (not poss_answer) and 1.*abs(response-poss_answer) < 1e-2:
                                score = self.max_pts[i]
                                break
            scores.append(score)
            comments.append("") # not doing anything for comments right now
        return {"scores": scores, "comments": comments}

class FileUpload(Question):

    encoding = "b"

    def __init__(self,seed):
        self.num_answers = 1

    def to_JSON(self,solution=False):
        data = {
            "type": "FileUpload",
            "text": self.text,
            "max_pts": self.max_pts[0],
            }
        if solution: data['solution'] = {
            "text": self.solution,
            }
        return data

    def check(self,responses,student_id=None):
        if responses[0]:
            filename = os.path.join(FILE_UPLOAD_DIR,
                                    self.__class__.__name__ + "_" + str(student_id))
            fout = open(filename,'w'+self.encoding)
            fout.write(responses[0])
            fout.close()
            responses[0] = "File uploaded successfully!"
        else:
            responses[0] = ""
        return {"scores": [""], "comments": [responses[0]]}

