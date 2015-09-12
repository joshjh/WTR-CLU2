__author__ = 'josh'
import mechanize
import re

def get_mileage(ps1, ps2):
    """
    :param ps1: The home post code
    :param ps2: Our current post code
    :return: The mileage between the two from AA routefinder
    """
    br = mechanize.Browser()
    br.open('http://www.theaa.com/route-planner/classic/planner_main.jsp')
    br.select_form = list(br.forms())[0]
    br["fromPlace"] = ps1
    br["toPlace"] = ps2
    br.submit()  # AA routeplanner returns a confidence check for the post codes

    # we know we are happy with the post codes so submit again
    br.select_form(name="routePlanner")
    response = br.submit()
    for y in response:
        match = re.search('miles', y)

        if match:
            y = y.lstrip() # returns without left chars
            y = round(float(y[:5]), -1) # round to closest 10
            rsp = y
            break
        else:
            rsp = '{}-ISBAD'.format(ps2)
    return rsp

# file format [0] postcode, [1] name, [2] service no, [3] ALW_mileage
print('\nstarting mileage comparison against output_miles.txt')
f = open('output_postcodes.txt', 'r')
for line in f:
    elements = line.split(':')
    print ('checking ', elements)
    print elements[0]
    checked_mileage = get_mileage('G848HL', elements[0])
    print(checked_mileage)


