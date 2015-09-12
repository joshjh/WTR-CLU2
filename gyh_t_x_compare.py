__author__ = 'josh'

from CLU_FIXED_VALUES import POSTCODE_FORMATS
import re

def run(SP_allow_db, sp_gyh_t_db, errors):
    # main statements in the program called from main
    # sp_gyt_t_db is a list of SP objects

    for x in range(len(sp_gyh_t_db)):
        gyh_sno = str(sp_gyh_t_db[x].Service_Number)[:8]
        caught_flag = 0

        for y in range(len(SP_allow_db)):

            if gyh_sno == str(SP_allow_db[y].Service_No)[:8]:
                caught_flag = 1
                compare_match(sp_gyh_t_db[x], SP_allow_db[y], errors)

        if caught_flag == 0:
            caught_error = 'GYH_T_X_COMPARE: could not match object ' + str(sp_gyh_t_db[x].whois) + ' To allowdb'
            errors.held_errors(caught_error)

def compare_match(gyh_object, allow_object, errors):
    # check mileages are the same
    if float(gyh_object.Temporary_GYH_Mileage) != allow_object.GYH_T_Mileage_To_Nominated_Address:
        print ('GYH_T_X_COMPARE: mileage does not match ', gyh_object.Temporary_GYH_Mileage,
               allow_object.GYH_T_Mileage_To_Nominated_Address, allow_object.whois)

    ps = allow_object.Full_GYH_T_Address
    ps2 = gyh_object.Post_Code.replace(' ', '') #knock out whitespace from JPA Postcode
    matches = []
    for x in POSTCODE_FORMATS:
        matches.append(re.findall(x, ps.replace(" ", ""))) # STRIP WHITESPACE BEFORE MATCHING

    match = (sorted(matches)[-1])
    if match:
        matched_postcode = 0

        for x in match:

            if x in ps2:
                print ('matched {} postcodes {} and {}'.format(allow_object.whois, ps, ps2))
                matched_postcode = 1

    if matched_postcode == 0:
        caught_error = 'GYH_T_X_COMPARE: could not match postcodes for {} {} {}'.format(str(allow_object.whois),ps,
                                                                                   ps2)
        errors.held_errors(caught_error)

