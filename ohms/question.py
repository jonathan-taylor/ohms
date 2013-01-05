#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>

import random
from answer import Answer,String,Float,TrueFalseAnswer,Text,MultipleChoiceAnswer

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

    def to_JSON(self,solution=False):
        json = {
            "text": self.text,
            "max_pts": self.max_pts
            }
        if solution: json['solution'] = {
            "text": self.solution
            }
        return json

        return None

    def set_seed(self,seed):
        """
        Set the seed, this should be called in the constructor 
        of all subclasses
        """
        self.seed = seed
        random.seed(seed)
        
    def cast(self,responses):
        """
        Cast each response to the appropriate type
        """
        cast_responses = []
        for i, answer in enumerate(self.answers):
            cast_responses.append(answer.cast(responses[i]))
        return cast_responses

    def check(self,responses):
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
        self.answers = []
        self.max_pts = []
        for i,part in enumerate(self.parts):
            self.active_parts.append(part(seed))
            self.max_pts.extend(self.active_parts[i].max_pts)
            self.answers.extend(self.active_parts[i].answers)

    def to_JSON(self,solution=False):
        json = {
            "text": self.text,
            "parts": [p.to_JSON(solution) for p in self.active_parts],
            "list_type": self.list_type
            }
        if solution: json['solution'] = {}
        return json

    def check(self,responses):
        scores = []
        comments = []
        end = 0
        for i, part in enumerate(self.active_parts):
            start = end
            end = start + len(part.answers)
            out = part.check(responses[start:end])
            scores.extend(out['scores'])
            comments.extend(out['comments'])
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
        self.answers = [Text()]
    
    def to_JSON(self,solution=False):
        json = {
            "type": "ShortAnswer",
            "text": self.text,
            "max_pts": self.max_pts[0],
            }
        if solution: json['solution'] = {"text": self.solution}
        return json

    def check(self,responses):
        return {"scores": [""], "comments": [""]}


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
        self.answers = [TrueFalseAnswer()]

    def to_JSON(self,solution=False):
        json = {
            "type": "TrueFalse",
            "text": self.text,
            "max_pts": self.max_pts[0],
            }
        if solution: json['solution'] = {
            "answer": self.answer, 
            "text": self.solution,
            }
        return json


    def check(self,responses):
        # cast all answers to the appropriate type
        responses = self.cast(responses)
        # check the true/false question
        score = (responses[0]==self.answer)*self.max_pts[0]
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
        self.answers = [MultipleChoiceAnswer(self.choices)]

    def to_JSON(self,solution=False):
        json = {
            "type": "MultipleChoice",
            "text": self.text,
            "choices": self.choices,
            "max_pts": self.max_pts[0],
            "compact": self.compact
            }
        if solution: json['solution'] = {
            "answer": self.answer, 
            "text": self.solution,
            }
        return json

    def check(self,responses):
        responses = self.cast(responses)
        score = self.max_pts[0] * (responses[0]==self.answer)
        if self.comments_by_choice:
            comment = self.comments_by_choice[responses[0]]
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
        answer_class = String if self.is_string else Float
        self.answers = []
        j = 0
        while 2*j+1 < len(self.body):
            self.body.insert(2*j+1,{
                    "type": answer_class.__name__,
                    "max_pts": self.max_pts[j]
                    })
            j += 1
            self.answers.append(answer_class())

    def to_JSON(self,solution=False):
        json = {
            "type": "FillInTheBlank",
            "body": self.body,
            "max_pts": self.max_pts
            }
        if solution: json['solution'] = {
            "answer": self.answer, 
            "text": self.solution,
            }
        return json

    def check(self,responses):
        # cast all responses to their appropriate type
        responses = self.cast(responses)
        # calculate the score for each blank
        scores = []
        comments = []
        for i, response in enumerate(responses):
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

