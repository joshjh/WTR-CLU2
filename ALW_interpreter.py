__author__ = 'josh'

''' Runner for allowance database matching, called by USR_analyse'''
import re
from CLU_FIXED_VALUES import *


def compare(allow_obj, sp_obj, errors):
    # compare allowance database GYH(M) to USR GYH(M)
    if allow_obj.GYH_T_Mileage_To_Nominated_Address == 'N/A':
        pass

    elif allow_obj.GYH_T_Mileage_To_Nominated_Address != sp_obj.Temp_GYH_Mileage:
        print('found mismatch between allowance DB GYH_T :{} and USR GYH_T {}'.format(allow_obj.GYH_T_Mileage_To_Nominated_Address,
                                                                                       sp_obj.Temp_GYH_Mileage))

    if allow_obj.Live_Onboard != 'YES' and sp_obj.Temp_SLA_Charged != '':
        print('does not have live onboard in ALWDB but Temp SLA is {}'.format(sp_obj.Temp_SLA_Charged))

    if allow_obj.Live_Onboard != 'NO' and sp_obj.Temp_SLA_Charged == '':
        print('does live onboard in ALWDB but Temp SLA is {}'.format(sp_obj.Temp_SLA_Charged))

    if allow_obj.Live_Onboard != 'NO':
        if sp_obj.Grade in FIX_VALUES_JUNIOR_RATES_RANKS and sp_obj.Temp_SLA_Charged != FIX_VALUES_JR['Temp_SLA_Charged']:
            print('temp SLA is {} should be {}'.format(sp_obj.Temp_SLA_Charged, FIX_VALUES_JR['Temp_SLA_Charged']))
        if sp_obj.Grade in FIX_VALUES_SENIOR_RATES_RANKS and sp_obj.Temp_SLA_Charged != FIX_VALUES_SR['Temp_SLA_Charged']:
            print('temp SLA is {} should be {}'.format(sp_obj.Temp_SLA_Charged, FIX_VALUES_SR['Temp_SLA_Charged']))
        if sp_obj.Grade in FIX_VALUES_JUNIOR_GRUNTERS_RANKS and sp_obj.Temp_SLA_Charged != FIX_VALUES_GRUNTER_JO['Temp_SLA_Charged']:
            print('temp SLA is {} should be {}'.format(sp_obj.Temp_SLA_Charged, FIX_VALUES_GRUNTER_JO['Temp_SLA_Charged']))
        if sp_obj.Grade in FIX_VALUES_GRUNTER_SO and sp_obj.Temp_SLA_Charged != FIX_VALUES_GRUNTER_SO['Temp_SLA_Charged']:
            print('temp SLA is {} should be G4Z'.format(sp_obj.Temp_SLA_Charged, FIX_VALUES_GRUNTER_SO['Temp_SLA_Charged']))
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




