__author__ = 'josh'

import ALW_interpreter
from CLU_FIXED_VALUES import *
import datetime
""" Analyse a USR object """

def run(SP_object, SP_allow_db, errors):
    __check_fixed_values__(SP_object, errors)
    __check_against_ALW__(SP_object, SP_allow_db, errors)
    __check_acting_local__(SP_object, errors)
    __check_pscat_sfa__(SP_object, errors)
    __check_against_accomp_status__(SP_object, errors)
    __check_gyh_rounding__(SP_object, errors)
# not running the warrants until end of the year
# __get_warrants__(SP_object)

def __check_gyh_rounding__(SP_object, errors):
    try:
        if SP_object.Perm_GYH_Mileage%10 != 0:
             print(bcolors.FAIL + 'incorrect rounding: {} for USR GYH_T mileage'.format
                   (SP_object.Perm_GYH_Mileage) + bcolors.ENDC)
    except TypeError:
        # non integer entries, whitespace and blank values will not work with %
        pass
    
def __check_against_accomp_status__(SP_object, errors):
    if SP_object.Perm_GYH_Mileage != '' and SP_object.Perm_Accomp_Status not in ('US, VS'):
        print (bcolors.OKBLUE + 'SP {} {} gets GYH T - possibly wrong Accompanied Status {}'.format(SP_object.whois,
                                                                        SP_object.Assignment_Number,
                                                                        SP_object.Perm_Accomp_Status) + bcolors.ENDC)
    
    if SP_object.SFA_Occupied != '' and SP_object.Perm_Accomp_Status not in ('A'):
        print (bcolors.OKBLUE + 'SP {} {} has SFA charge - possibly wrong Accompanied Status {}'.format(SP_object.whois,
                                                                        SP_object.Assignment_Number,
                                                                        SP_object.Perm_Accomp_Status) + bcolors.ENDC)     
    
def __check_pscat_sfa__(SP_object, errors):
    if SP_object.SFA_Occupied != '' and SP_object.Marital_Status in ('Category 5', 'Category 4', 'Category 3'):
        print (bcolors.OKBLUE + 'SP {} {} is PS Cat {} and has MQ Charges'.format(SP_object.whois,
                                                                        SP_object.Assignment_Number,
                                                                        SP_object.Marital_Status) + bcolors.ENDC)
        
    if SP_object.SFA_Occupied !='' and SP_object.Perm_GYH_Mileage != '':
        print (bcolors.OKBLUE + 'SP {} {} gets GYH T and occupies SFA?'.format(SP_object.whois,
                                                                        SP_object.Assignment_Number) + bcolors.ENDC)
def __check_acting_local__(SP_object, errors):
    if SP_object.Acting_Paid_Rank != '':
        print (bcolors.OKBLUE + 'SP {} {} is Acting Local {} and should be in Supervisors Log'.format(SP_object.whois,
                                                                        SP_object.Assignment_Number,
                                                                        SP_object.Acting_Paid_Rank) + bcolors.ENDC)
def __check_fixed_values__(SP_object, errors):
    SP_object_dict = SP_object.__dict__
    if SP_object.whois == ('TRIUMPH', 'OFFICER OF THE DAY|1560669'):
        pass
    else:

        if SP_object.Temp_Allowance_Location in ('ASSLQU', 'INTRANSIT', 'GBR'):
                print(bcolors.OKBLUE + '--- ASSESS {} {} should be in the LANDED LOG'.format
                      (SP_object.whois, SP_object.Assignment_Number) + bcolors.ENDC)
            # allow for multiple organisations with Hasler.

        if SP_object.Organization not in FIX_VALUES_ORGANISATIONS:
            print(bcolors.OKBLUE + 'Organisation for Service Person: ', SP_object.whois, 'is: ',
                  SP_object.Organization, 'should be one of: ', str(FIX_VALUES_ORGANISATIONS) + bcolors.ENDC)


        for key in SP_object_dict:

            # determine the correct map to use
            # Fixed values imported from CLU_FIXED_VALUES for ease of reading/modication
            if SP_object.Grade in FIX_VALUES_JUNIOR_RATES_RANKS:
                
                if key in ('Perm_SLA_Charged', 'Perm_SLA_Occupied'):
                    pass
                
                elif key in FIX_VALUES_JR and SP_object_dict[key] != FIX_VALUES_JR[key]:
                    print (bcolors.OKBLUE + key,' for Service Person: ',  SP_object.whois, 'is: ',
                           SP_object_dict[key], 'should be: ', FIX_VALUES_JR[key] + bcolors.ENDC)

            elif SP_object.Grade in FIX_VALUES_SENIOR_RATES_RANKS:
                
                if key in ('Perm_SLA_Charged', 'Perm_SLA_Occupied'):
                    pass
                
                elif key in FIX_VALUES_SR:
                    if SP_object_dict[key] != FIX_VALUES_SR[key]:
                        print (bcolors.OKBLUE, key,' for Service Person: ',  SP_object.whois, 'is: ',
                               SP_object_dict[key], 'should be: ', FIX_VALUES_SR[key] + bcolors.ENDC)
           
            elif SP_object.Grade in FIX_VALUES_JUNIOR_GRUNTERS_RANKS:
                
                if key in ('Perm_SLA_Charged', 'Perm_SLA_Occupied'):
                    pass
                elif key in FIX_VALUES_GRUNTER_JO:
                    if SP_object_dict[key] != FIX_VALUES_GRUNTER_JO[key]:
                        print (bcolors.OKBLUE + key,' for Service Person: ',  SP_object.whois, 'is: ',
                               SP_object_dict[key], 'should be: ', FIX_VALUES_GRUNTER_JO[key] + bcolors.ENDC)
            else:
                
                if key in ('Perm_SLA_Charged', 'Perm_SLA_Occupied'):
                    pass
                
                elif key in FIX_VALUES_GRUNTER_SO:
                    if SP_object_dict[key] != FIX_VALUES_GRUNTER_SO[key]:
                        print (bcolors.OKBLUE + key,' for Service Person: ',  SP_object.whois, 'is: ',
                               SP_object_dict[key], 'should be: ', FIX_VALUES_GRUNTER_SO[key] + bcolors.ENDC)



def __get_warrants__(sp_object, END_OF_YEAR=1):
    leave_year_end = datetime.datetime(2017, 4, 1)
    # CATCH errors for non_fav dates (stub accounts etc)
    try:
        int_time = int(sp_object.FAV_Date)
    except ValueError:
        print ('no FAD date found for {}'.format(sp_object.whois))

    # stupid excel date integer formats run from 01-01-1900
    year_zero = datetime.datetime(1899, 12, 30)
    warrants = 0

    # if end of year, we for the twelve month period (leave year end - 1 year, and one period of 36 days
    if END_OF_YEAR == 1:
        running_time = leave_year_end - datetime.timedelta(days=366) + datetime.timedelta(days=36)
    # for new joiners, we need to go from the start of entitlement.  This should really be SP.startdate
    else:
        running_time = datetime.datetime.today() + datetime.timedelta(days=36)
    # test if inttime got set.
    try:
        int_time
        fav_date = year_zero + datetime.timedelta(days=int_time)
        
        while running_time < leave_year_end and running_time < fav_date:
            warrants += 1
            running_time += datetime.timedelta(days=36)

    except NameError:
        pass
    
    if END_OF_YEAR == 1:
        print ('has {} warrants to leave year ending {}'.format(warrants, leave_year_end))
    else:
        print ('has {} warrants to from today'.format(warrants, leave_year_end))

def __check_against_ALW__(SP_object, SP_allow_db, errors):
    '''
    :param SP_object: service person object
    :return: process of errors against the AP database object
    '''
    # we get one SP at a time, but all the allowance database.  We need to match just one of the allowance database
    # lines for each SP
    caught_flag = 0
    if SP_object.whois == ('TRIUMPH', 'OFFICER OF THE DAY|1560669'):
        pass
    else:
        # loop through the whole SP_allow_db to match a record by service number with the single SP object
        for x in range(len(SP_allow_db)):
            # cut to 8 chars to allow for -2 service numbers
            if str(SP_allow_db[x].Service_No)[:8] == str(SP_object.Assignment_Number)[:8]:
                print('Matched {} to {} in allowance DB'.format(SP_allow_db[x].Service_No, SP_object.Assignment_Number))
                caught_flag = 1
                # if we have a match we can pass the single SP_allow object, and SP object and error recorded to
                # The ALW_interpreter fuction to do the error checking.
                ALW_interpreter.compare(SP_allow_db[x], SP_object, errors)

        if caught_flag == 0:
            caught_error = 'ERROR: cannot match ' + str(SP_object.whois) + 'to allowance database entry!'
            errors.held_errors(caught_error)
