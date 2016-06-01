__author__ = 'josh'
from CLU_FIXED_VALUES import bcolors
import getopt
import sys
import openbook
import error_log
import USR_analyse
import gyh_t_x_compare
import tasbat
import os
import re

def main():
    # create an error log object to the passed to each function for recording errors
    errors = error_log.held_errors()
    
    # blank the postcode file before it gets the append write function in ALW_Interpreter
    with open('output_postcodes.txt', 'w') as file:
        file.close()
        
        for root, dirs, files in os.walk('test-data'):
            f_found_files = []
            #  the below uses consistant naming traits through re.search to pull out files of different types from
            # the folder test-data and assign the file path to f_*** 

            for file in files:
                f_tasbat = re.search('TASBAT', file)
                f_usr = re.search('-Unit Status Report', file)
                f_allowdb = re.search('Allowance_Database', file)
                f_gyh_t = re.search('Claimant Report', file)
                # to do f_landedlog

                if f_tasbat and os.path.isfile('test-data/' + f_tasbat.string):
                    f_found_files.append('tasbat')
                    print(bcolors.OKGREEN + 'TASBAT found file: {}, executing'.format(f_tasbat.string) + bcolors.ENDC)
                    open_tasbat = openbook.openbook('test-data/' + f_tasbat.string, sheet_type='TASBAT')
                    tasbat.tasbat_execute(open_tasbat)
                
                # f_found_files will prevent the execution of more than one file of type usr or alw, which would cause
                # carnage.
                
                if f_usr and os.path.isfile('test-data/' + f_usr.string) and 'usr' not in f_found_files:
                    print(bcolors.OKGREEN + 'USR found file: {}, executing'.format(f_usr.string) + bcolors.ENDC)
                    SP_object_list = openbook.openbook('test-data/' + f_usr.string, sheet_type='USR')
                    f_found_files.append('usr')
                    
                if f_allowdb and os.path.isfile('test-data/' + f_allowdb.string) and 'alw' not in f_found_files:
                    print(bcolors.OKGREEN + 'Allowance DB found file: {}, executing'.format(f_allowdb.string) + bcolors.ENDC)
                    SP_allow_db = openbook.openbook('test-data/' + f_allowdb.string, sheet_type='ALW')
                    f_found_files.append('alw')
                 
                if f_gyh_t and os.path.isfile('test-data/' + f_gyh_t.string) and 'gyh_t' not in f_found_files:
                    print(bcolors.OKGREEN + 'GYH_T found file: {}, executing'.format(f_gyh_t.string) + bcolors.ENDC)
                    SP_gyh_t_db = openbook.openbook('test-data/' + f_gyh_t.string, sheet_type='OBIEE_GYH_T')
                    f_found_files.append('gyh_t')   
                    gyh_t_x_compare.run(SP_allow_db, SP_gyh_t_db, errors)
        
        # main loop through each person object generated from the USR.  Missing out persons without assignment number.
        for x in range(len(SP_object_list)):
            if SP_object_list[x].Assignment_Number != '':
                print(bcolors.BOLD + '\nIDENTIFIED ANOMOLIES FOR SP {} {}'.format(SP_object_list[x].whois,
                                    str(SP_object_list[x].Assignment_Number)[:8]) + bcolors.ENDC)
                # the main call for the USR to check the current object
                USR_analyse.run(SP_object_list[x], SP_allow_db, errors)
    
            else:
                errors.held_errors('SP: ' + SP_object_list[x].whois[0] + ' ' + SP_object_list[x].whois[1] +
                                                                                ' is a unarrived entity')
        errors.dump_held_errors()

if __name__ == '__main__':
    main()
    # pointless .py code line counter
    clu_lines = 0
    for root, dirs, files in os.walk('./'):
        for i in files:
            pyfile = re.search('.py$', i)
            try:
                with open(pyfile.string) as f:
                    clu_lines += len(f.readlines())
                    f.close()
            except (TypeError, AttributeError):
                pass
            
    print('CLU is now {} lines of code'.format(clu_lines))