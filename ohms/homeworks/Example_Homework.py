#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
#  Copyright (c) 2012, Kinjal Basu <kinjal@stanford.edu>
#  Copyright (c) 2012, Edison Tam <edison.tam@stanford.edu>

from ohms.question import *
import random
from datetime import datetime
from ohms.utils.stats.normal_distribution import ZTestQuestion

class Ch26Ex1(MultiPartQuestion):

    name = "Ch. 26 Review Exercise 1"

    class Part1(TrueFalse):
        text = "The <i>P</i>-value of a test equals its observed significance level."
        answer = "t"
        max_pts = [4]
        solution = "True. This is by definition."

    class Part2(TrueFalse):
        text = r'''The alternative hypothesis is another way of explaining 
        the results; it says the difference is due to chance.'''
        answer = "f"
        max_pts = [4]
        solution = "False. The null says it's chance, the alternative says it's real."

    parts = [Part1,Part2]

class Ch26Ex2(MultiPartQuestion):

    name = "Chapter 26 Review Exercise 2"
    text = r'''With a perfectly balanced roulette wheel, in the long run,
    red numbers should turn up 18 times in 38. To test its wheel, one
    casino records the results of 3,800 plays, finding 1,890 red numbers. Is
    that too many reds? Or chance variation?'''

    class PartA(MultiPartQuestion):
        
        text = r'''Let's set up a box model for this problem.'''
        list_type = 'i'

        class PartI(MultipleChoice):
            text = r'''The box in this case consists of...'''
            choices = ['''0's and 1's with a 1 indicating red.''',
                       '''the numbers on a roulette wheel.''']
            answer = 0
            max_pts = [1]

        class PartII(MultipleChoice):
            text = r'''The number 1,890 represents...'''
            choices = ['''the sum of 38 draws from this box.''',
                       '''the mean of 38 draws from this box.''',
                       '''the sum of 3,800 draws from this box.''',
                       '''the mean of 3,800 draws from this box.''']
            answer = 2
            max_pts = [1]

        parts = [PartI,PartII]
    
    class PartB(MultiPartQuestion):

        list_type = 'i'

        class PartI(FillInTheBlank):
            text = r'''The null says that the percentage of reds in the box 
is ____%.'''
            is_string = False
            answer = [[47.4]]
            exact_match = False
            max_pts = [1]
        
        class PartII(MultipleChoice):
            text = r'''The alternative says that the percentage of reds in 
the box is:'''
            choices = ["less than this","more than this"]
            answer = 1
            max_pts = [1]
        
        parts = [PartI,PartII]
            
    class PartC(MultiPartQuestion):

        list_type='i'

        class PartI(MultipleChoice):
            text = r'''The SE for the <b>number</b> of reds is:'''
            choices = [r'''\(\sqrt{3800} \times 
\sqrt{\frac{18}{38} \times \frac{20}{38}}\)''',
r'''\(\sqrt{3800} \times \sqrt{\frac{1890}{3800} \times 
\frac{1910}{3800}}\)''',
r'''\(\frac{\sqrt{\frac{18}{38} \times
            \frac{20}{38}}}{\sqrt{3800}}\)''',
r'''\(\frac{\sqrt{\frac{1890}{3800} \times
            \frac{1910}{3800}}}{\sqrt{3800}}\)''']
            answer = 0
            max_pts = [1]

        class PartII(ZTestQuestion):
            z = 2.9
            is_signed = True
            two_sided = "no"
            max_pts = [2,2]
            solution = r'''The expected number of reds (computed using the null) 
is 1800. The SD of the box (also computed using the null) is nearly 0.5, 
so the SE for the number of reds is \(\sqrt{3800} \times 0.5 \approx
            31\). So 
$$z = \frac{\text{observed} - \text{expected}}{SE} = \frac{1890 - 1800}{31}
\approx 2.9,$$
and \(P \approx 0.2\%\).
'''
#         class PartII(FillInTheBlank):
#             text = r'''Compute <i>z</i> and <i>P</i>.<br><br>
# <i>z</i> = ____ and <i>P</i> = ____%
# '''
#             is_string = False
#             answer = [[2.9],[.15,.17,.19]]
#             exact_match = False
#             max_pts = [2,2]

        parts = [PartI,PartII]

    class PartD(TrueFalse):
        text = r'''There were too many reds.'''
        answer = "t"
        max_pts = [1]
        solution = "True. The <i>P</i>-value is less than 5%."

    parts = [PartA,PartB,PartC,PartD]

class Ch26Ex5(MultiPartQuestion):

    name = "Chapter 26 Review Exercise 5"
    text = r'''A newspaper article says that on the average, college
    freshmen spend 7.5 hours a week going to parties. One administrator
    does not believe that these figures apply at her college, which has
    nearly 3,000 freshmen. She takes a simple random sample of 100
    freshmen, and interviews them. On average, they report 6.6 hours a
    week going to parties, and the SD is 9 hours. Is the difference
    between 6.6 and 7.5 real?'''

    class PartA(MultiPartQuestion):
        
        text = r'''Let's set up a box model for this problem.'''
        list_type = 'i'

        class PartI(MultipleChoice):
            text = r'''The box in this case consists of...'''
            choices = ['''0's and 1's with a 1 indicating that the student
            went to parties.''',
                       '''the number of hours each student spent going to parties.''']
            answer = 1
            max_pts = [1]

        class PartII(MultipleChoice):
            text = r'''The number 6.6 represents...'''
            choices = ['''the sum of 100 draws from this box.''',
                       '''the mean of 100 draws from this box.''',
                       '''the sum of 3,000 draws from this box.''',
                       '''the mean of 3,000 draws from this box.''']
            answer = 1
            max_pts = [2]

        parts = [PartI,PartII]


    class PartB(MultiPartQuestion):

        text = r'''Fill in the blanks.'''
        list_type = 'i'

        class PartI(FillInTheBlank):
            text = r'''The null says that the average of the box is 
____.'''
            is_string = False
            answer = [[7.5]]
            exact_match = True
            max_pts = [1]

        class PartII(MultipleChoice):
            text = r'''The alternative says that the average is:'''
            choices = ["less than this.","more than this."]
            answer = 0
            max_pts = [1]

        parts = [PartI,PartII]

    class PartC(MultiPartQuestion):

        list_type = 'i'

        class PartI(ZTestQuestion):
            z = -1.0
            is_signed = True
            two_sided = "no"
            max_pts = [2,2]
            solution = r'''Under the null, the expected value is 7.5 hours,
            and we observed a mean of 6.6 hours. Since the SE for the mean
            of 100 draws is \(SD/\sqrt{n}=9/\sqrt{100}=0.9\),
            $$z = \frac{\text{observed}-\text{expected}}{SE} = 
            \frac{6.6-7.5}{0.9} = -1.$$
            We know from the normal table that the chance of observing a 
            \(z\)-score so small is \(P \approx 16\%\)'''

        class PartII(TrueFalse):
            text = r'''The difference can be explained by chance.'''
            answer = "t"
            max_pts = [1]
            solution = r'''True. The <i>p</i>-value tells us that there is a
            16% chance of observing a result so extreme.'''

        parts = [PartI,PartII]

    parts = [PartA,PartB,PartC]


class Ch26Ex6(MultiPartQuestion):

    name = "Ch. 26 Review Exercise 6"
    text = r'''In 1969, Dr. Spock came to trial before Judge Ford, in
    Boston's federal court house. The charge was conspiracy to violate the
    Mlitary Service Act. "Of all defendants, Dr. Spock, who had given wise
    and welcome advice on child-rearing to millions of mothers, would have
    liked women on his jury." The jury was drawn from a "venire," or
    panel, of 350 persons selected by the clerk. This venire included only
    102 women, although a majority of the eligible jurors in the district
    were female. At the next stage in selecting the jury to hear the case,
    Judge Ford chose 100 potential jurors out of these 350 persons. His
    choice included 9 women.'''

    class PartA(ZTestQuestion):
        text = r'''350 people are chosen at random from large population
which is over 50% female. The <i>z</i>-score for a jury with only 
102 women is ____, and the chance that the sample includes 102 
women or fewer is about ____%.'''
        z = -7.8
        is_signed = True
        two_sided = "no"
        max_pts = [2,2]
        solution = r'''
In the best case for Judge Ford, we are tossing a coin 350 times, and 
asking for the chance of getting 102 heads or fewer. The expected 
number of heads is 175 and the SE is about 9.3, so 
$$z \approx \frac{102-175}{9.3} \approx -7.8.$$ The chance is about 0.
'''
        
    class PartB(FillInTheBlank):
        text = r'''100 people are chosen at random (without replacement)
        from a group consisting of 102 women and 248 men. The <i>z</i>-score 
for a jury with only 9 women is ____, and the chance that 
        the sample includes 9 women or fewer is about ____%.'''
        is_string = False
        answer = [[(-5.4,-5.2),(-4.5,-4.3)],[0]]
        exact_match = False
        max_pts = [2,2]
        solution = r'''100 draws are made at random without replacement from 
a box with 102 1's and 248 0's, where 1 = woman and 0 = man. The expected 
number of 1's is 29. If the draws are made with replacement, the SE for 
the number of 1's is \(\sqrt{100} \times \sqrt{0.29 \times 0.71} 
\approx 4.54\). So 
$$z \approx \frac{9-29}{4.54} = -4.4.$$ 
The chance is about 0.
'''

    class PartC(MultipleChoice):
        text = "From this, we can conclude that:"
        choices = ['''the lack of women in both the venire  
and the final jury could well have happened by chance.''',
'''the lack of women in the clerk's venire is unlikely to 
have happened by chance, but the lack of women in the final 
jury could well have happened by chance.''',
'''the lack of women on the final jury is unlikely to 
have happened by chance, but the lack of women in the clerk's 
venire could well have happened by chance.''',
'''the lack of women in both the venire and jury is unlikely to 
have happened by chance.''']
        answer = 3
        max_pts = [2]
        solution = r'''
Both <i>p</i>-values are essentially 0, so the lack of women is highly 
unlikely to have happened by chance.
'''
   
    parts = [PartA,PartB,PartC]

class Ch27Ex3(MultiPartQuestion):

    name = "Ch. 27 Review Exercise 3"
    text = r'''The Gallup poll asks respondents how they would rate the
    honesty and ethical standards of people in different fields &mdash; very
    high, high, average, low or very low. The percentage who rated clergy
    "very high or high" dropped from 60% in 2000 to 54% in 2005. This may
    have been due to scandals involving sex abuse; or it may have been a
    chance variation. (You may assume that in each year, the results are
    based on independent simple random samples of 1,000 persons in each
    year.)'''

    class PartA(MultipleChoice):
        text = "Which test is appropriate here?"
        choices = ["one sample z-test","two sample z-test"]
        answer = 1
        compact = False
        max_pts = [1]
        solution = ""

    class PartB(ShortAnswer):
        text = r'''Formulate the null and alternative hypotheses in terms of 
a box model. Do you need one box or two? Why? How many tickets go into 
each box? How many draws? What do the tickets show? What do the null and 
alternative hypotheses say about the box(es)?'''
        max_pts = [4]

    class PartC(MultiPartQuestion):

        class PartI(ZTestQuestion):
            z = -2.7
            is_signed = False
            two_sided = "no"
            max_pts = [2,2]
            solution = r'''
Note that the units here are percents. Thus, we will convert everything to
            decimals (e.g., \(54\% = .54\)). First, we calculate the SE of the percentage in 2000 and 2005:
\begin{align*}
\text{SE in 2000} &= \frac{\sqrt{.6 \times (1-.6)}}{\sqrt{1000}} = .015 \\
\text{SE in 2005} &= \frac{\sqrt{.54 \times (1-.54)}}{\sqrt{1000}} = .016 \\
\end{align*}
Hence, the SE for the difference between the percentages in these two
            years is:
$$\text{SE diff} = \sqrt{(\text{SE in 2000})^2 +
            (\text{SE in 2005})^2} = \sqrt{.015^2 + .016^2} = .022.$$
Hence the <i>z</i>-score is:
$$z = \frac{\text{obs diff} - \text{exp diff}}{\text{SE diff}} = \frac{(.54 - .60)-0}{.022} \approx -2.7$$
If we look up \(z = -2.7\) on the normal table, we obtain \(P \approx 0.3\%\).
'''

        class PartII(MultipleChoice):
            text = "What is the cause of the difference between 60% and 54%?"
            choices = ["chance variation", "scandals", "cannot be determined"]
            answer = 2
            compact = True
            max_pts = [1]
            comments_by_choice = ["",'''The hypothesis test only shows that 
the difference is real. It does not necessarily say what caused it.''',""]
        
        parts = [PartI,PartII]

    parts = [PartA,PartB,PartC]


class Ch27Ex8(MultiPartQuestion):

    name = "Ch. 27 Review Exercise 8"
    text = r'''One experiment contrasted responses to "prediction-request"
    and to "request-only" treatments, in order to answer two research
    questions.
<ol type = "i">
<li>Can people predict how well they will behave? </li>
<li>Do their predictions influence their behavior? </li> 
</ol>
In the prediction-request group, subjects were first asked to predict
    whether they would agree to do some volunteer work. Then they were
    requested to do the work. In the request-only group, the subjects were
    requested to do the work; they were not asked to make predictions
    beforehand. In parts (a-b-c), a two sample z-test may or may not be
    legitimate. If it is legitimate, make it. If not, why not?'''

    class PartA(MultiPartQuestion):
        text = r'''46 residents of Bloomington, Indiana were chosen at
        random for the "prediction-request" treatment. They were called
        and asked to predict "whether they would agree to spend 3 hours
        collecting for the American Cancer Society if contacted over the
        telephone with such a request." 22 out of 46 said that they would.
        Another 46 residents of that town were chosen at random for the
        "request-only" treatment. They were requested to spend the 3 hours
        collecting for the American Cancer Society. Only 2 out of 46
        agreed to do it.'''
        list_type = 'i'

        class PartI(ZTestQuestion):
            text = r'''Can the difference between 22/46 and 2/46 be due 
to chance? Conduct a hypothesis test, if possible; otherwise leave the 
blanks unfilled.<br><br>

<i>z</i> = ____ and <i>P</i> = ____%'''
            z = -5.4
            is_signed = False
            two_sided = "either"
            max_pts = [1,1]
            solution = r'''
The two samples are like independent draws from two boxes, so a two-sample <i>z</i>-test
            is valid. 

First, we calculate the SE of the fraction who predict they would
volunteer (\(\frac{22}{46} \approx .478\)) and the SE of the fraction
who actually do volunteer when requested (\(\frac{2}{46} \approx .043\)):
\begin{align*}
\text{SE}_\text{predict} &= \frac{\sqrt{.478 \times (1-.478)}}{\sqrt{46}} = .074 \\
\text{SE}_\text{request} &= \frac{\sqrt{.043 \times (1-.043)}}{\sqrt{46}} = .030 \\
\end{align*}
Hence, the SE for the difference between the percentages in these two
            years is:
$$\text{SE diff} = \sqrt{(\text{SE}_\text{predict})^2 +
            (\text{SE}_\text{request})^2} = \sqrt{.074^2 + .030^2} = .080.$$
Hence the <i>z</i>-score is:
$$z = \frac{\text{obs diff} - \text{exp diff}}{\text{SE diff}} = \frac{(.043-.478)-0}{.080} \approx -5.4$$
\(z = -5.4\) is off the charts, so \(P \approx 0\%\).
'''

        class PartII(ShortAnswer):
            text = r'''If the test above was not possible, say why. 
Otherwise, explain what the data say about the research questions (i) and 
(ii).'''
            max_pts = [2]
            solution = r'''
This answers (i). People cannot predict how they will behave.
'''

        parts = [PartI,PartII]

    class PartB(MultiPartQuestion):

        text = r'''Three days later, the prediction-request group was 
        called again and requested to spend 3 hours collecting for the
        American Cancer Society: 14 out of 46 agreed to do so.'''
        list_type = 'i'

        class PartI(ZTestQuestion):
            text = r'''Can the difference between 14/46 and 2/46 be due 
to chance? Conduct a hypothesis test, if possible; otherwise leave the 
blanks unfilled.<br><br>

<i>z</i> = ____ and <i>P</i> = ____%'''
            z = -3.5
            is_signed = False
            two_sided = "either"
            max_pts = [1,1]
            solution = r'''
The two samples are like independent draws from two boxes, so a two-sample <i>z</i>-test
            is valid. 

First, we calculate the SE of the fraction in the group which was asked to
predict (\(\frac{14}{46} \approx .304\)) and the SE of the fraction
in the group which was not asked beforehand (\(\frac{2}{46} \approx .043\)):
\begin{align*}
\text{SE}_\text{predict-request} &= \frac{\sqrt{.304 \times (1-.304)}}{\sqrt{46}} = .068 \\
\text{SE}_\text{request-only} &= \frac{\sqrt{.043 \times (1-.043)}}{\sqrt{46}} = .030 \\
\end{align*}
Hence, the SE for the difference between the percentages in these two
            years is:
$$\text{SE diff} = \sqrt{(\text{SE}_\text{predict-request})^2 +
            (\text{SE}_\text{request-only})^2} = \sqrt{.068^2 + .030^2} = .074.$$
Hence the <i>z</i>-score is:
$$z = \frac{.043-.304}{.074} \approx -3.5$$
\(z = -3.5\) corresponds to \(P \approx 0.0235\%\). A two-sided test
is also okay, for which you double the <i>p</i> value, \(P \approx 0.047\%\).
'''

        class PartII(ShortAnswer):
            text = r'''If the test above was not possible, say why. 
Otherwise, explain what the data say about the research questions (i) and 
(ii).'''
            max_pts = [2]
            solution = r'''
This answers (ii). People's predictions influence their behavior.
'''

        parts = [PartI,PartII]

    class PartC(MultiPartQuestion):

        list_type = 'i'

        class PartI(FillInTheBlank):
            text = r'''Can the difference between 22/46 and 14/46 be due 
to chance? Conduct a hypothesis test, if possible; otherwise leave the
            blanks unfilled.<br><br>

<i>z</i> = ____ and <i>P</i> = ____%'''
            answer = [[""],[""]]
            is_string = True
            exact_match = True
            max_pts = [1,1]

        class PartII(ShortAnswer):
            text = r'''If the test above was not possible, say why. 
Otherwise, explain what the data say about the research questions (i) and 
(ii).'''
            max_pts = [2]

            solution = r'''
The test above is not possible because the samples are not independent.
'''

        parts = [PartI,PartII]

    parts = [PartA,PartB,PartC]


class Ch27Ex10(ShortAnswer):

    name = "Ch. 27 Review Exercise 10"
    text = r'''An investigator wants to show that first-born children score
    higher on IQ tests than second-borns. He takes a simple random sample
    of 400 two-child families in a school district, both children being
    enrolled in elementary school. He gives these children the WISC
    vocabulary test (described in Exercise 7 pp. 507-508), with the
    following results.
<ol Type = "i">
<li>The 400 first-borns average 29 and their SD is 10. </li>
<li>The 400 second-borns average 28 and their SD is 10. </li>
</ol>
(Scores are corrected for age differences). He makes a two sample z-test:
$$\text{SE for first-born average} \approx 0.5$$
$$\text{SE for second-born average} \approx 0.5$$
$$\text{SE for difference} = \sqrt{0.5^2 + 0.5^2} \approx 0.7$$
$$z = 1/0.7 \approx 1.4,\,\, P \approx 8\%$$
</ol>
Comment briefly on the use of statistical tests.
'''
    max_pts = [10]
    solution = r'''
This test is not legitimate. There is dependence between the first-borns
    and second-borns.
'''


homework = Homework(name="Example Homework 1",
                    text = r'''
<p><b>Materials</b> (opens in new window): <a href='../restricted/normal.pdf' target='_blank'>Normal Table</a></p>
''',
                    questions=[Ch26Ex1,Ch26Ex2,Ch26Ex5,
                               Ch26Ex6,Ch27Ex3,Ch27Ex8, Ch27Ex10],
                    due_date=datetime(2012,11,16,23,59,59))


