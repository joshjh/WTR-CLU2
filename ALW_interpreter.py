__author__ = 'josh'

''' Runner for allowance database matching, called by USR_analyse'''
import re
from CLU_FIXED_VALUES import *

def compare(allow_obj, sp_obj, errors):
    # compare allowance database GYH(M) to USR GYH(M)
    if allow_obj.GYH_T_Mileage_To_Nominated_Address == 'N/A':
        pass

    elif allow_obj.GYH_T_Mileage_To_Nominated_Address != sp_obj.Perm_GYH_Mileage:
        print(bcolors.WARNING + 'found mismatch between allowance DB GYH_T :{} and USR GYH_T {}'.format
              (allow_obj.GYH_T_Mileage_To_Nominated_Address, sp_obj.Perm_GYH_Mileage) + bcolors.ENDC)

    if allow_obj.Live_Onboard == 'No' and sp_obj.Perm_SLA_Charged != '':
        print(bcolors.WARNING + 'does not have live onboard in ALWDB but Perm SLA is {}'.format
              (sp_obj.Perm_SLA_Charged) + bcolors.ENDC)

    if allow_obj.Live_Onboard != 'No' and allow_obj.Live_Onboard != '' and sp_obj.Perm_SLA_Charged == '':
        print(bcolors.WARNING + 'does live onboard in ALWDB but Perm SLA is {}'.format(sp_obj.Perm_SLA_Charged)
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
    ps = allow_obj.Full_GYH_T_Address
    #this is a bit of a fucking mess at the moment, but should sort to the longest of several re matches,
    # which should be the full post code
    matches = []
    for x in POSTCODE_FORMATS:
        matches.append(re.findall(x, ps.replace(" ", ""))) # STRIP WHITESPACE BEFORE MATCHING

    match = (sorted(matches)[-1])
    if match:
        match.append(allow_obj.NAME)
        match.append(allow_obj.Service_No)
        match.append(allow_obj.GYH_T_Mileage_To_Nominated_Address)
        with open('output_postcodes.txt','a') as fileout:
            outline = match[0] + ':' + match[1] + ':' + str(match[2]) + ':' + str(match[3])
            fileout.write(outline)
            fileout.write('\n')
            fileout.close()
    ## some writing of postcode for miles to pick up seperately.




