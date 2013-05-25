#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
#  Copyright (c) 2012, Kinjal Basu <kinjal@stanford.edu>
#  Copyright (c) 2012, Edison Tam <edison.tam@stanford.edu>

import ohms.question2
reload(ohms.question2)
from ohms.question2 import *
import random
from datetime import datetime
from ohms.utils.stats.normal_distribution import ZTestQuestion

q1 = MultiPartQuestion(name="Ch. 26 Review Exercise 1")
part1 = TrueFalse(text="The <i>P</i>-value of a test equals its observed significance level.",
                  answer='T',
                  max_pts=[4],
                  solution="True. This is by definition.")
part2 = TrueFalse(text='''The alternative hypothesis is another way of explaining 
        the results; it says the difference is due to chance.''',
                  answer = "f",
                  max_pts = [4],
                  solution = "False. The null says it's chance, the alternative says it's real.")
q1.parts = [part1, part2]

q2 = MultiPartQuestion(name="Chapter 26 Review Exercise 2", 
                       text=r'''With a perfectly balanced roulette wheel, in the long run,
    red numbers should turn up 18 times in 38. To test its wheel, one
    casino records the results of 3,800 plays, finding 1,890 red numbers. Is
    that too many reds? Or chance variation?''')
partA = MultiPartQuestion(text = r'''Let's set up a box model for this problem.''',
                          list_type = 'i')
partAI  = MultipleChoice(text=r'''The box in this case consists of...''',
                         choices = ['''0's and 1's with a 1 indicating red.''',
                                    '''the numbers on a roulette wheel.'''],
                         answer = 0,
                         max_pts = [1])
partAII = MultipleChoice(text = r'''The number 1,890 represents...''',
                         choices = ['''the sum of 38 draws from this box.''',
                                    '''the mean of 38 draws from this box.''',
                                    '''the sum of 3,800 draws from this box.''',
                                    '''the mean of 3,800 draws from this box.'''],
                         answer = 2,
                         max_pts = [1])
partA.parts = [partAI, partAII]

    
partB = MultiPartQuestion(list_type='i')
partBI = FillInTheBlank(text = r'''The null says that the percentage of reds in the box 
is ____%.''',
                        is_string = False,
                        answer = [[47.4]],
                        exact_match = False,
                        max_pts = [1])
partBII = MultipleChoice(text = r'''The alternative says that the percentage of reds in 
the box is:''',
                         choices = ["less than this","more than this"],
                         answer = 1,
                         max_pts = [1])
partB.parts = [partBI,partBII]
            
partC = MultiPartQuestion(list_type='i')
partCI = MultipleChoice(text = r'''The SE for the <b>number</b> of reds is:''',
                        choices = [r'''\(\sqrt{3800} \times 
\sqrt{\frac{18}{38} \times \frac{20}{38}}\)''',
r'''\(\sqrt{3800} \times \sqrt{\frac{1890}{3800} \times 
\frac{1910}{3800}}\)''',
r'''\(\frac{\sqrt{\frac{18}{38} \times
            \frac{20}{38}}}{\sqrt{3800}}\)''',
r'''\(\frac{\sqrt{\frac{1890}{3800} \times
            \frac{1910}{3800}}}{\sqrt{3800}}\)'''],
                        answer = 0,
                        max_pts = [1])
# partCII = ZTestQuestion(z = 2.9,
#                         is_signed = True,
#                         two_sided = "no",
#                         max_pts = [2,2],
#                         solution = r'''The expected number of reds (computed using the null) 
# is 1800. The SD of the box (also computed using the null) is nearly 0.5, 
# so the SE for the number of reds is \(\sqrt{3800} \times 0.5 \approx
#             31\). So 
# $$z = \frac{\text{observed} - \text{expected}}{SE} = \frac{1890 - 1800}{31}
# \approx 2.9,$$
# and \(P \approx 0.2\%\).
# ''')
# partC.parts = [partCI, partCII]

partD = TrueFalse(text=r'''There were too many reds.''',
                  answer = "t",
                  solution = "True. The <i>P</i>-value is less than 5%.")

q2.parts = [partA,partB,partC,partD]



homework = Homework(name="Example Homework 1",
                    text = r'''
<p><b>Materials</b> (opens in new window): <a href='../restricted/normal.pdf' target='_blank'>Normal Table</a></p>
''',
                    questions=[q1,q1,q2],
                    due_date=datetime(2012,11,16,23,59,59))


