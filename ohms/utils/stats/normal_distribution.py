#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>

from ohms.question import FillInTheBlank
from math import log10, floor, ceil, sqrt

normal_table = {
    0.0: 0.0, 0.25: 19.74, 2.0: 95.45, 
    3.0: 99.73, 4.0: 99.9937, 0.75: 54.67,
    1.0: 68.27, 0.1: 7.97, 2.2: 97.22, 
    0.5: 38.29, 3.3: 99.903, 4.3: 99.9983,
    3.05: 99.771, 1.9: 94.26, 1.75: 91.99, 
    0.3: 23.58, 0.4: 31.08, 0.85: 60.47, 
    3.9: 99.99, 2.5: 98.76, 2.3: 97.86, 
    3.25: 99.885, 0.6: 45.15, 3.95: 99.992, 
    1.1: 72.87, 0.55: 41.77, 1.3: 80.64, 
    3.75: 99.982, 2.6: 99.07, 2.95: 99.68, 
    4.25: 99.9979, 1.55: 87.89, 1.7: 91.09, 
    1.35: 82.3, 3.45: 99.944, 2.55: 98.92, 
    3.15: 99.837, 2.7: 99.31, 4.05: 99.9949, 
    4.15: 99.9967, 3.4: 99.933, 0.15: 11.92, 
    3.2: 99.863, 4.35: 99.9986, 1.45: 85.29, 
    2.75: 99.4, 3.55: 99.961, 1.95: 94.88, 
    2.85: 99.56, 3.7: 99.978, 2.45: 98.57, 
    4.4: 99.9989, 0.7: 51.61, 3.6: 99.968, 
    1.25: 78.87, 3.85: 99.988, 0.95: 65.79, 
    0.8: 57.63, 1.5: 86.64, 0.45: 34.73, 
    0.9: 63.19, 1.8: 92.81, 1.65: 90.11, 
    3.8: 99.986, 1.05: 70.63, 3.1: 99.806, 
    2.8: 99.49, 0.2: 15.85, 2.1: 96.43, 
    2.15: 96.84, 2.4: 98.36, 1.15: 74.99,
    0.35: 27.37, 1.4: 83.85, 4.1: 99.9959, 
    4.2: 99.9973, 2.65: 99.2, 4.45: 99.9991, 
    3.65: 99.974, 1.2: 76.99, 2.25: 97.56, 
    2.05: 95.96, 1.6: 89.04, 3.5: 99.953, 
    0.65: 48.43, 0.05: 3.99, 1.85: 93.57, 
    2.35: 98.12, 2.9: 99.63, 3.35: 99.919,
    4.5: 100.
}

def get_two_sided_p(z,round_func=round):
    z_round = min(round_func(20.*abs(z))/20,4.5)
    return 100.-normal_table[z_round]

def round_p(p,round_func=round):
    if p>1: return round_func(p)
    elif p:
        i = -int(floor(log10(p)))
        return round_func(p*(10**i))/10**i
    else: return 0

def same_sign(x,y):
    if x >= 0 and y >= 0: return True
    elif x <= 0 and y <= 0: return True
    else: return False


class ZTestQuestion(FillInTheBlank):
    """
    Class attributes to be set by user:
    z - either a single value or a tuple (a,b) containing 
        the acceptable range of z-scores a<=x<=b
    is_signed - boolean indicating if z-score sign matters
    two_sided - boolean indicating if test is 2-sided
    max_pts - point value of question
    solution - answer to question
    """

    # attributes to be set for each question
    z = 1.65
    tol = .05 # error tolerance
    is_signed = True
    two_sided = "no" # yes/no/either
    max_pts = [1,1]
    solution = ""

    # attributes that are automatically set for class
    text = "<i>z</i> = ____ and <i>P</i> = ____%"
    is_string = False
    exact_match = False

    def _z_changed(self):
        # if z < 1, acceptable z are +/- 0.05 of correct answer
        # otherwise, must be within 5% of correct answer
        z0 = self.z-self.tol if abs(self.z)<1. else (1-self.tol)*self.z
        z1 = self.z+self.tol if abs(self.z)<1. else (1+self.tol)*self.z
        z_range = (min(z0,z1),max(z0,z1))
        # get corresponding 2-sided p-values
        p0 = get_two_sided_p(z_range[0],floor)
        p1 = get_two_sided_p(z_range[1],ceil)
        # if sign doesn't matter, include negative solution
        if self.is_signed: z_range = [z_range]
        else: z_range = [z_range,(-z_range[1],-z_range[0])]
        # acceptable ranges for p-values
        (p0,p1) = (min(p0,p1),max(p0,p1))
        if self.two_sided=="no":
            p_range = [(round_p(p0/2,floor),round_p(p1/2,ceil))]
        elif self.two_sided=="yes":
            p_range = [(round_p(p0,floor),round_p(p1,ceil))]
        else:
            p_range = [(round_p(p0,floor),round_p(p1,ceil)),
                      (round_p(p0/2,floor),round_p(p1/2,ceil))]
        # set answer
        self.answer = [z_range, p_range]
        # call constructor of FillInTheBlank superclass
        super(ZTestQuestion,self).__init__(seed)
    

    def check(self,responses):
        out = super(ZTestQuestion,self).check(responses)
        # generate comments
        if responses[0]:
            if self.is_signed and not same_sign(self.z,float(responses[0])):
                out['comments'][0] = "Watch the sign of your <i>z</i>-score!"
            elif out['scores'][0] and not out['scores'][1]:
                out['comments'][1] = '''Your <i>z</i>-score is correct, but 
check the <i>P</i>-value again.'''
        return out
    

