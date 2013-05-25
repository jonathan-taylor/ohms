#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>



import random, os, datetime
try:
    from ohms.config import FILE_UPLOAD_DIR
except ImportError:
    FILE_UPLOAD_DIR = ''

import IPython.utils.traitlets as traits
        
class Homework(traits.HasTraits):
    
    questions = traits.List
    text = traits.Unicode
    name = traits.Unicode
    due_date = traits.Instance(datetime.datetime)
    
class Question(traits.HasTraits):

    name = traits.Unicode
    parts = traits.List
    solution = traits.Unicode
    answer = traits.Unicode
    submits_allowed = traits.Int
    lockout_time = traits.Int
    seed = traits.Int(0)
    text = traits.Unicode
    max_pts = traits.List([1])
    num_answers = traits.Int
    seed = traits.Int
    type = traits.Unicode

    @property
    def num_answers(self):
        return len(self.max_pts)

    def to_JSON(self,solution=False):
        data = {
            "type": self.type,
            "text": self.text,
            "max_pts": self.max_pts
            }
        if solution: data['solution'] = {
            "text": self.solution,
            "answer": self.answer
                }
        return data

    def _seed_changed(self):
        random.seed(self.seed)
        for part in self.parts:
            part.seed = self.seed

    def check(self,responses,student_id=None):
        """
        Check answers, returning a dict of scores and comments
        """
        return None


class MultiPartQuestion(Question):
    """
    Question with multiple parts (which are themselves questions)
    """

    active_parts = traits.List()
    list_type = traits.Unicode("a")

    def _parts_changed(self):
        self.active_parts = []
        self.max_pts = []
        for part in self.parts:
            part.seed = self.seed
            self.active_parts.append(part)
            self.max_pts.extend(part.max_pts)

    def to_JSON(self,solution=False):
        data = {
            "type": self.type,
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

    def check(self,responses,student_id=None):
        return {"scores": [""], "comments": [""]}


class LaTeXAnswer(ShortAnswer):
    pass

class TrueFalse(Question):
    """
    Basic True/False question
    """

    comment_if_wrong = traits.Unicode

    def check(self,responses,student_id=None):
        if responses[0] not in ["T","F"]:
            responses[0] = ""
            return { "scores": [0], "comments": [""] }
        else:
            # check the true/false question
            score = (responses[0]==self.answer.upper())*self.max_pts[0]
            comment = self.comment_if_wrong if not score else ""
            return { "scores": [score], "comments": [comment] }

class MultipleChoice(Question):
    """
    Basic multiple choice question with one correct answer
    """
    # subclasses should override these class attributes

    choices = traits.List
    comments_by_choice = traits.List
    compact = traits.Bool(False)
    answer = traits.Int

    def to_JSON(self,solution=False):
        data = Question.to_JSON(self, solution)
        data['choices'] = self.choices

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

class MultipleResponse(MultipleChoice):

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

    body = traits.List
    exact_match = traits.Bool
    is_string = traits.Bool
    answer = traits.List

    def _text_changed(self):
        # first create an array with 
        self.body = self.text.split("____")
        # insert an input box between every element of the list
        j = 0
        while 2*j+1 < len(self.body):
            self.body.insert(2*j+1,{
                    "type": "String" if self.is_string else "Float",
                    "max_pts": self.max_pts[j]
                    })
            j += 1

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

    encoding = traits.Unicode("b")

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



def add_explanation(question):
    """
    Take a question and add an explain part.
    """
    new_question = MultiplePartQuestion()
    new_question.text = question.text
    question.text = ''
    explanation = ShortAnswer()
    new_question.parts = [question, explanation]
    return new_question

