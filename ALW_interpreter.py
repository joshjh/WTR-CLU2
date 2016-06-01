__author__ = 'josh'

''' Runner for allowance database matching, called by USR_analyse'''
import re
import miles

from CLU_FIXED_VALUES import *
from excel_timehack import excel_timehack
from datetime import datetime
from datetime import timedelta

def compare(allow_obj, sp_obj, errors):
    # compare allowance database GYH(M) to USR GYH(M)
    if allow_obj.GYH_T_Mileage_To_Nominated_Address in ('N/A', 'N', 'No'):
        pass

    elif allow_obj.GYH_T_Mileage_To_Nominated_Address != sp_obj.Perm_GYH_Mileage:
        print(bcolors.FAIL + 'found mismatch between allowance DB GYH_T :{} and USR GYH_T {}'.format
              (allow_obj.GYH_T_Mileage_To_Nominated_Address, sp_obj.Perm_GYH_Mileage) + bcolors.ENDC)
    
    # if division by 10 gives a remainder, the gyh(t) mileage was not rounded
    try:
        if allow_obj.GYH_T_Mileage_To_Nominated_Address%10 != 0:
            print(bcolors.FAIL + 'incorrect rounding: {} for allowance DB GYH_T mileage'.format
              (allow_obj.GYH_T_Mileage_To_Nominated_Address) + bcolors.ENDC)
    except TypeError as e:
        pass

    if allow_obj.Live_Onboard == 'No' and sp_obj.Perm_SLA_Charged != '':
        print(bcolors.FAIL + 'does not have live onboard in ALWDB but Perm SLA is {}'.format
              (sp_obj.Perm_SLA_Charged) + bcolors.ENDC)

    if allow_obj.Live_Onboard not in ('No', 'N') and allow_obj.Live_Onboard != '' and sp_obj.Perm_SLA_Charged == '':
        print(bcolors.FAIL + 'does live onboard in ALWDB but Perm SLA is {}'.format(sp_obj.Perm_SLA_Charged)
                                                                                     + bcolors.ENDC)

    if allow_obj.Live_Onboard == 'Yes':
        if sp_obj.Grade in FIX_VALUES_JUNIOR_RATES_RANKS and sp_obj.Perm_SLA_Charged != FIX_VALUES_JR['Perm_SLA_Charged']:
            print(bcolors.OKBLUE + 'Perm SLA is {} should be {}'.format(sp_obj.Perm_SLA_Charged, FIX_VALUES_JR['Perm_SLA_Charged'])
                                                                    + bcolors.ENDC)
        if sp_obj.Grade in FIX_VALUES_SENIOR_RATES_RANKS and sp_obj.Perm_SLA_Charged != FIX_VALUES_SR['Perm_SLA_Charged']:
            print(bcolors.OKBLUE + 'Perm SLA is {} should be {}'.format(sp_obj.Perm_SLA_Charged, FIX_VALUES_SR['Perm_SLA_Charged'])
                                                                     + bcolors.ENDC)
        if sp_obj.Grade in FIX_VALUES_JUNIOR_GRUNTERS_RANKS and sp_obj.Perm_SLA_Charged != FIX_VALUES_GRUNTER_JO['Perm_SLA_Charged']:
            print(bcolors.OKBLUE + 'Perm SLA is {} should be {}'.format(sp_obj.Perm_SLA_Charged, FIX_VALUES_GRUNTER_JO['Perm_SLA_Charged'])
                                                                    + bcolors.ENDC)
        if sp_obj.Grade in FIX_VALUES_GRUNTER_SO and sp_obj.Perm_SLA_Charged != FIX_VALUES_GRUNTER_SO['Perm_SLA_Charged']:
            print(bcolors.OKBLUE + 'Perm SLA is {} should be G4Z'.format(sp_obj.Perm_SLA_Charged, FIX_VALUES_GRUNTER_SO['Perm_SLA_Charged'],
                                                                    + bcolors.ENDC))
    
    if allow_obj.Live_Onboard not in ('Y', 'N'):
        print(bcolors.FAIL + 'Live Onboard Flag MISSING or corrupt/invalid' + bcolors.ENDC)
    # print(allow_obj.__dict__)

    try:
        int(allow_obj.Annual_GYH_T_and_HDT_Documention_Check)
        doc_check_anniversary = excel_timehack(allow_obj.Annual_GYH_T_and_HDT_Documention_Check)
        today = datetime.today()
        if doc_check_anniversary < today - timedelta(days=365):
            print(bcolors.FAIL + 'OOD annual GYH/HTD check' + bcolors.ENDC)

    except ValueError:
        print(bcolors.FAIL + 'annual GYH/HTD check date not set' + bcolors.ENDC)

    postcode_check(allow_obj, errors)

def postcode_check(allow_obj, errors):
    # pull out postcode from the allowance object, then run it through the Python Miles Module against the global postcode
    # PS is postcode pulled from GYH_T_address line in allowance object
    ps = allow_obj.Full_GYH_T_POSTCODE
    if not str(ps).upper() in ('', 'NA', 'N/A', 'N'):
        try:
            gmaps_distance = round(miles.get_mileage('PL22BG', ps), -1) # return rounded mileage
            print(bcolors.OKGREEN + ' matched GMAPS: {} to ALLOWDB {}'.format(gmaps_distance,
                                                        allow_obj.GYH_T_Mileage_To_Nominated_Address) + bcolors.ENDC)
            if gmaps_distance < 5:
                print(bcolors.FAIL + 'GYH Mileage Rounding FAIL' + bcolors.ENDC)
            else:
                if allow_obj.GYH_T_Mileage_To_Nominated_Address != gmaps_distance:
                    print(bcolors.FAIL + 'GMAPS mileage {} != allowance db mileage {}'.format(gmaps_distance,
                                                        allow_obj.GYH_T_Mileage_To_Nominated_Address)+ bcolors.ENDC)
        except TypeError:  # TypeError is returned when miles.get_mileage drops out on postcode check
            pass

    




