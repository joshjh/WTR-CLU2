__author__ = 'josh'

import xlrd
import getopt
import sys
import openbook
import error_log
import USR_analyse
import gyh_t_x_compare
import tasbat
import os
import re

def main(argv):
    # get options from the command line.  -h help. -i input file. -t type of input
    try:
        opts, args = getopt.getopt(argv, 'hi:t:')
        for opt, arg in opts:
            if opt in ('-i'):
                inputfile = arg
            elif opt in ('-t'):
                type = arg

    except getopt.GetoptError:
        print('Usage: -h help -i input file -t USR ALW')
    # create an error log object to the passed to each function for recording errors
    errors = error_log.held_errors()
    # blank the postcode file before it gets the append write function in ALW_Interpreter
    with open('output_postcodes.txt', 'w') as file:
        file.close()
    # call openbook to run down the XLS sheets creating objects for each line (person-USR) or (person-Allowance DB)

    SP_object_list = openbook.openbook('test-data/usr.xls', sheet_type='USR')
    SP_allow_db = openbook.openbook('test-data/allowdb.xls', sheet_type='ALW')
    SP_gyh_t_db = openbook.openbook('test-data/GYH_T.xls', sheet_type='OBIEE_GYH_T')

    # dropping of multi tasbats with consistant naming - run each
    for root, dirs, files in os.walk('test-data'):
        for file in files:
            f_tasbat = re.search('TASBAT', file)
            if f_tasbat and os.path.isfile('test-data/' + f_tasbat.string):
                print('TASBAT found file: {}, executing'.format(f_tasbat.string))
                open_tasbat = openbook.openbook('test-data/' + f_tasbat.string, sheet_type='TASBAT')
                tasbat.tasbat_execute(open_tasbat)

    # main loop through each person object generated from the USR.  Missing out persons without assignment number.
    for x in range(len(SP_object_list)):
        if SP_object_list[x].Assignment_Number != '':
            print('\nIDENTIFIED ANOMOLIES FOR SP {} {}'.format(SP_object_list[x].whois, str(SP_object_list[x].Assignment_Number)[:8]))
            # the main call for the USR to check the current object
            USR_analyse.run(SP_object_list[x], SP_allow_db, errors)

        else:
            errors.held_errors('SP: ' + SP_object_list[x].whois[0] + ' ' + SP_object_list[x].whois[1] +' is a unarrived entity')

    gyh_t_x_compare.run(SP_allow_db, SP_gyh_t_db, errors)
    errors.dump_held_errors()

if __name__ == '__main__':
    main(sys.argv[1:])