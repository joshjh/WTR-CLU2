__author__ = 'josh'

''' Runner for allowance database matching, called by USR_analyse'''
import re
from CLU_FIXED_VALUES import *

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
    
    if allow_obj.Live_Onboard == '':
        print(bcolors.FAIL + 'Live Onboard Flag MISSING' + bcolors.ENDC)
    postcode_check(allow_obj, errors)

def postcode_check(allow_obj, errors):
    # pull out postcode from the allowance object, then run it through the Python Miles Module against the global postcode
    # PS is postcode pulled from GYH_T_address line in allowance object
    ps = allow_obj.Full_GYH_T_POSTCODE
    if str(ps) != '':
        
        line = str(allow_obj.NAME) + ':' + str(allow_obj.Service_No) + ':' + str(allow_obj.GYH_T_Mileage_To_Nominated_Address) + ':' + str(ps)
        with open('output_postcodes.txt','a') as fileout:
                fileout.write(line)
                fileout.write('\n')
                fileout.close()
    




