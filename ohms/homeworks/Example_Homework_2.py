#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
#  Copyright (c) 2012, Julia Fukuyama <jaf88@stanford.edu>
#-----------------------------------------------------------------

from question import *
import random
from datetime import datetime
from utils.normal import ZTestQuestion

class Ch28Ex1(MultiPartQuestion):
    name = "Ch. 28 Review Exercise 1"
    text = '''You are drawing 100 times at random with replacement
    from a box. Fill in the blanks, using the options below.'''
    
    class PartA(MCQuestion):
        text = '''To test the null hypothesis that the average of
        the box is 2, you would use:'''
        choices = ['the one-sample <i>z</i>-test',
                   'the two-sample <i>z</i>-test',
                   '''the \(\chi^2\)-test, with a null hypothesis
                   that tells you the contents of the box''',
                   'the \(\chi^2\)-test for independence']
        answer = 0
        max_pts = [5]
        
    class PartB(MCQuestion):
        text = r'''To test the null hypothesis that the box is
        \(\fbox{\(\fbox{1}\fbox{2}\fbox{3}\)}\), you would use:'''
        choices = ['the one-sample <i>z</i>-test',
                   'the two-sample <i>z</i>-test',
                   '''the \(\chi^2\)-test, with a null hypothesis
                   that tells you the contents of the box''',
                   'the \(\chi^2\)-test for independence']
        answer = 2
        max_pts = [5]
    
    parts = [PartA,PartB]

class Ch28Ex2(MultiPartQuestion):
    
    name = "Ch. 28 Review Exercise 2"
    text = r'''
    As part of a study on the selection of grand juries in
    Alameda county, the educational level of grand jurors was
    compared with the county distribution.
    '''
    list_type = 'i'

    class PartI(FillInTheBlank):

        is_string = False
        exact_match = False
        answer = [[17.6],[30.1],[7.4],[6.9]]
        max_pts = [1,1,1,1]
        text = r'''
        The data on the percentage of people in the county
        and the number of grand jurors attaining each educational
        level is shown below. Fill in the expected number of
        jurors attaining each educational level if the grand jury
        had been selected as a simple random sample from the
        population. (<b>Note</b>: the expected "number" can and should be a 
        decimal.)
        
        <table class="table">
        <thead>
          <th style="width:30%">Educational Level</td>
          <th style="width:20%">County</td>
          <th style="width:20%">Number of jurors</td>
          <th style="width:30%">Expected "number"</td>
        </thead>
        <tbody>
        <tr>
          <td>Elementary</td>
          <td>28.4%</td>
          <td>1</td>
          <td>____</td>
        </tr>
        <tr>
          <td>Secondary</td>
          <td>48.5%</td>
          <td>10</td>
          <td>____</td>
        </tr>
        <tr>
          <td>Some college</td>
          <td>11.9%</td>
          <td>16</td>
          <td>____</td>
        </tr>
        <tr>
          <td>College degree</td>
          <td>11.2%</td>
          <td>35</td>
          <td>____</td>
        </tr>
        <tr>
          <td><b>Total</b></td>
          <td><b>100.0%</b></td>
          <td><b>62</b></td>
          <td></td>
        </tr>
        </tbody>
        </table>
        '''

    class PartII(FillInTheBlank):

        text = r'''The test statistic is \(\chi^2 = \) ____ with ____ degrees of freedom, 
        corresponding to a <i>P</i>-value between ____% and ____%.'''
        max_pts = [2,1,0.5,0.5]
        is_string = False
        exact_match = False
        answer = [[153.5],[3],[0],[0.5]]

    class PartIII(MCQuestion):

        text = r'''Could a simple random sample from the county show a distribution
        of education level so different from the county-wide one? Choose one option
        and explain.
        '''
        choices = ['This is absolutely impossible.',
                   'This is possible, but fantastically unlikely.',
                   'This is possible but unlikely&mdash;the chance is around 1% or so.',
                   'This is quite possible&mdash;the chance is around 10% or so.',
                   'This is nearly certain.']
        comments_by_choice = ['''The <i>p</i>-value may be small, but is it <i>absolutely</i> impossible?''',
                              "","","",""]
        answer = 1
        max_pts = [2]

    parts = [PartI,PartII,PartIII]


class Ch29Ex4(ShortAnswer):
    name = "Ch 29 Review Exercise 4"
    text = r'''In employment discrimination cases, courts have held that there is proof of discrimination when the percentage of blacks among a firm's employees is lower than the percentage of blacks in the surrounding geographical region, provided the difference is "statistically significant" by the <i>z</i>-test. Suppose that in one city, 10% of the people are black. Suppose too that every firm in the city hires employees by a process which, as far as race is concerned, is equivalent to simple random sampling. Would any of these firms ever be found guilty of discrimination by the <i>z</i>-test? Explain briefly.'''
    max_pts = [10]
    solution = r'''Yes. By design, there is a 5% chance that we would
    reject the null hypothesis (of no discrimination) even if it was
    true. Thus, if we do a separate test for every firm in the city, we
    would expect about 5% of them to be found guilty of discrimination by
    this criteria, even if there is no discrimination. This is an example
    of data snooping (p. 547).
'''


class Ch29Ex33(MultiPartQuestion):

    name = "Ch. 29 Review Exercise 33"
    text = r'''
<p>In the US, there are two sources of national statistics on crime rates:
    (i) the FBI's Uniform Crime Reporting Program, which publishes
    summaries on all crimes reported to police agencies in jurisdictions
    covering virtually 100% of the population; (ii) the National Crime
    Survey, based on interviews with a nationwide probability sample of
    households.</p> 

<p>In 2001, 3% of the households in the sample told the interviewers they
had experienced at least one burglary within the past 12 months. The same
year, the FBI reported a burglary rate of 20 per 1,000 households, or
2%. Can this difference be explained as chance error? If not, how would
you explain it? You may assume that the Survey is based on a simple random
sample of 50,000 households out of 100 million households.</p>
'''

    class PartA(MultiPartQuestion):
        
        list_type = 'i'
        text = "First, let's set up a box model for this problem."

        class PartI(MCQuestion):
            text = r'''The box contains:'''
            choices = ['''100 million tickets with either 0 or 1, with 1 indicating households that have experienced a burglary in the past year''',
        '''50,000 tickets with either 0 or 1, with 1 indicating households that have experienced a burglary in the past year''',
        '''100 million tickets with numbers corresponding to how many burglaries a household has experienced in the past year''',
        '''50,000 tickets with numbers corresponding to how many burglaries a household has experienced in the past year''']
            answer = 0
            max_pts = [2]
        

        class PartII(MCQuestion):
            text = r'''What test is appropriate here?'''
            choices = ['''A 1-sample <i>z</i>-test testing the hypothesis
            that 3% of households have experienced a burglary in the past
            year.''',
                       '''A 1-sample <i>z</i>-test testing the hypothesis
            that 2% of households have experienced a burglary in the past
            year.''',
                       '''A 2-sample <i>z</i>-test testing the hypothesis
            that there is no difference between the percentage who
            report a burglary and the percentage who experienced one.'''
                       ]
            answer = 1
            max_pts = [2]
            comments_by_choice = ['''Think about which is the sample
            here&mdash;the National Crime Survey or the FBI report?''',
                                  "",
                                  '''Is the FBI figure of 2% really
            derived from a sample?''']

        parts = [PartI,PartII]


    class PartB(ZTestQuestion):
            z = 16.0
            is_signed = True
            two_sided = "no"
            max_pts = [2,2]


    class PartC(MCQuestion):
    	text = r'''What do you conclude?'''
        choices = ['''The difference between 2 and 3% is well within the range expected by chance.''',
                   '''The difference between 2 and 3% is almost impossible to explain by chance&mdash;many burglaries are not reported to the police''']
        answer = 1
        max_pts = [2]


    parts = [PartA,PartB,PartC]




class Ch29Ex34(MultiPartQuestion):
    name = "Ch 29 Review Exercise 34"
    text = r'''A statistician tosses a coin 100 times and gets 60 heads. His null hypothesis says that the coin is fair; the alternative, that the coin is biased&mdash;the probability of landing heads is more than 50%.'''
    
    class PartA(TFQuestion):
        text = r'''If the coin is fair, the chance of getting 60 or more heads is about 3%.'''
        answer = "t"
        max_pts = [2]
        solution = 'true (section 18.4)'

    class PartB(TFQuestion):
        text = r'''Given that it lands heads 60 times, there is only about a 3% chance for the coin to be fair.'''
        answer = 'f'
        max_pts = [2]
        solution = 'false (pp. 480-81)'

    class PartC(TFQuestion):
        text = r'''Given that it lands heads 60 times, there is about a 97% chance for the coin to be biased.'''
        answer = 'f'
        max_pts = [2]
        solution = 'false (pp.480-81)'

    class PartD(ShortAnswer):
        text = r'''Explain your answers to parts a, b, and c.'''
        max_pts = [3]

    parts = [PartA,PartB,PartC,PartD]



class Ch29Ex35(MultiPartQuestion):

    name = "Ch. 29 Review Exercise 35"
    text = r'''
<p>The Multiple Risk Factor Intervention Trial tested the effect of an
    interviention to reduce three risk factors for coronary heart
    disease&mdash;serum cholesterol, blood pressure, and smoking. The
    subjects were 12,866 men age 35-57, at high risk for heart
    disease. 6,428 were randomized to the intervention group and 6,438 to
    the control. The intervention included counseling on diet and smoking,
    and in some cases therapy to reduce blood pressure. Subjects were
    followed for a minimum of 6 years.</p>

<p>For each part below, test the hypothesis of no difference between the
two groups described.</p>
'''

    class PartA(MultiPartQuestion):
        
        text = r'''On entry to the study, the diastolic blood pressure of the intervention group averaged 91.0 mm Hg; their SD was 7.6 mm Hg. For the control group, the figures were 90.9 and 7.7. (Blood pressure is measured in millimeters of mercury, or mmHg.)'''
        list_type = 'i'

        class PartI(ZTestQuestion):
            z = .74
            tol = .10
            is_signed = False
            two_sided = "either"
            max_pts = [1,1]
            
        class PartII(MCQuestion):
            text = "What do you conclude? (<b>Suggestion:</b> Think about whether this is a good or a bad thing.)"
            choices = ['''The intervention and control groups had similar diastolic blood pressures before the study began. Any difference is explainable by chance.''',
                       '''The intervention and control groups had significantly different diastolic blood pressures even before the study began.''']
            answer = 0
            max_pts = [1]
            

        parts = [PartI,PartII]


    class PartB(MultiPartQuestion):
        
        text = """After 6 years, the diastolic blood pressure of the intervention group averaged 80.5 mm Hg; their SD was 7.9 mm Hg. For the control group, the figures were 83.6 and 9.2."""
        list_type = 'i'

        class PartI(ZTestQuestion):
            z = -20.5
            is_signed = False
            two_sided = "either"
            max_pts = [1,1]

        class PartII(MCQuestion):
            text = "What do you conclude?"
            choices = ['''There is no evidence that the intervention reduces subjects' diastolic blood pressure.''',
                       '''The intervention significantly reduces subjects' diastolic blood pressure.''']
            answer = 1
            max_pts = [1]

        parts = [PartI,PartII]


    class PartC(MultiPartQuestion):
        
        text = r'''On entry to the study, the serum cholesterol level of the intervention group averaged 253.8 mg/dl; their SD was 36.4 mg/dl. For the control group, the figures were 253.5 and 36.8.'''
        list_type = 'i'

        class PartI(ZTestQuestion):
            z = .46
            tol = .10
            is_signed = False
            two_sided = "either"
            max_pts = [1,1]

        class PartII(MCQuestion):
            text = "What do you conclude? (<b>Suggestion:</b> Think about whether this is a good or a bad thing.)"
            choices = ['''The intervention and control groups had similar serum cholesterol levels before the study began. Any difference is explainable by chance.''',
                       '''The intervention and control groups had significantly different serum cholesterol levels even before the study began.''']
            answer = 0
            max_pts = [1]

        parts = [PartI,PartII]


    class PartD(MultiPartQuestion):
        
        text = r'''After 6 years, the serum cholesterol level of the intervention group averaged 235.5 mg/dl; their SD was 38.3 mg/dl. For the control group, the figures were 240.3 and 39.9.'''
        list_type = 'i'

        class PartI(ZTestQuestion):
            z = -7.
            is_signed = False
            two_sided = "either"
            max_pts = [1,1]

        class PartII(MCQuestion):
            text = "What do you conclude?"
            choices = ['''There is no evidence that the intervention reduces subjects' serum cholesterol levels.''',
                       '''The intervention significantly reduces subjects' serum cholesterol levels.''']
            answer = 1
            max_pts = [1]            

        parts = [PartI,PartII]

    class PartE(MultiPartQuestion):
        
        text = r'''On entry to the study, 59.3% of the intervention group were smoking, compared to 59.0% for the control group.'''
        list_type = 'i'

        class PartI(ZTestQuestion):
            z = .35
            tol = .10
            is_signed = False
            two_sided = "either"
            max_pts = [1,1]

        class PartII(MCQuestion):
            text = "What do you conclude? (<b>Suggestion:</b> Think about whether this is a good or a bad thing.)"
            choices = ['''The intervention and control groups had similar smoking habits before the study began. Any difference is explainable by chance.''',
                       '''The intervention and control groups differed significantly in their smoking habits before the study began.''']
            answer = 0
            max_pts = [1]

        parts = [PartI,PartII]

    class PartF(MultiPartQuestion):
        
        text = r'''After 6 years, the percentage of smokers was 32.3% in the intervention group and 45.6% in the control group.'''
        list_type = 'i'

        class PartI(ZTestQuestion):
            z = -15.6
            is_signed = False
            two_sided = "either"
            max_pts = [1,1]

        class PartII(MCQuestion):
            text = "What do you conclude?"
            choices = ['''There is no evidence that the intervention affects subjects' smoking habits.''',
                       '''The intervention significantly discourages smoking.''']
            answer = 1
            max_pts = [1]            

        parts = [PartI,PartII]


    class PartG(MultiPartQuestion):
        
        text = r'''In the treatment group, 211 men had died after 6 years, compared to 219 in the control group.'''
        list_type = 'i'

        class PartI(ZTestQuestion):
            z = -.38
            tol = .10
            is_signed = False
            two_sided = "either"
            max_pts = [1,1]

        class PartII(MCQuestion):
            text = "What do you conclude?"
            choices = ['''There is no evidence that the intervention affects mortality rate.''',
                       '''The intervention significantly reduces mortality rate.''']
            answer = 0
            max_pts = [1]                        

        parts = [PartI,PartII]            

    parts = [PartA,PartB,PartC,PartD,PartE,PartF,PartG]




class Ch29Ex39(ShortAnswer):
    name = "Ch. 29 Review Exercise 39"
    text = r'''
<p>M.S. Kanarek and associates studied the relationship between cancer
    rates and levels of asbestos in the drinking water, in 722 Census
    tracts around San Francisco Bay. After adjusting for age and various
    demographic variables, but not smoking, they found a "strong
    relationship" between the rate of lung cancer among white males and
    the concentration of asbestos fibers in the drinking water: <i>P</i> <
    1/1,000.</p>

<p>Multiplying the concentration of asbestos by a factor of 100 was
associated with an increase in the level of lung cancer by a factor of
about 1.05, on average. (If tract B has 100 times the concentration of
asbestos fibers in the water as tract A, and the lung cancer rate for
white males in tract A is 1 per 1,000 persons per year, a rate of 1.05 per
1,000 persons per year is predicted in tract B.)</p>

<p>The investigators tested over 200 relationships&mdash;different types
of cancer, different demographic groups, different ways of adjusting for
possible confounding variables. The <i>P</i>-value for lung cancer in
white males was by far the smallest one they got.</p>

<p>Does asbestos in the drinking water cause lung cancer? Is the effect a
strong one? Discuss briefly, making sure to address <b>both</b> questions.</p>
'''
    max_pts = [10]
    solution = r'''Lots of mistakes here: first, they did lots of tests, which makes <i>P</i>-values hard to interpret (p. 547). The effect they found is tiny, so it would not be that useful a result even if the <i>P</i>-values were valid. They also didn't account for smoking, which is a major cause of lung cancer. Their argument is weak, and there is no reason to think that asbestos in the water causes lung cancer.'''



homework = Homework(name='Example Homework 2',
                    text = r'''
<p><b>Materials</b> (opens in new window): 
<a href='../restricted/normal.pdf' target='_blank'>Normal Table</a></p>
''',
                    questions=[Ch28Ex1,Ch28Ex2,Ch29Ex4,Ch29Ex33,
                    Ch29Ex34,Ch29Ex35,Ch29Ex39],
                    due_date=datetime(2012,11,30,23,59,59))


