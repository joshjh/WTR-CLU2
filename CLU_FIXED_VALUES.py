__author__ = 'josh'
# What should be::
FIX_POSTCODE = 'G848HL'
POSTCODE_FORMATS = ['\w\w\d\w\d\w\w', '\w\d\w\d\w\w', '\w\d\d\w\w', '\w\d\d\d\w\w', '\w\w\d\d\w\w', '\w\w\d\d\d\w\w', '\w\w\d\d\w\w']

FIX_VALUES_JR = {'Temp_Allowance_Reason': 'T13', 'Change_of_IBD_Reason': '', 'Perm_Allowance_Reason': 'P02', 'Gender': 'Male',
               'Type': 'Employee.Available for Assignment',  'PAYD/_LOS12/_GYH(S)': 'YNN',
              'Temp_Allowance_Location': 'UKNBP', 
               'Location': 'HMS TRIUMPH',  
               'Status': 'Active Assignment', 'Perm_GYH_Mileage': '', 'Field_or_Shipboard': 'N',
               'Temp_Accomp_Status': '', 'Nationality': 'British',
               'Perm_Allowance_Location': 'UKBPD', 'Organization': 'HMS TRIUMPH', 'Perm_HTD_Location': '',
               'Addressable_Rank': '', 'Temp_HTD_Location': '', 'Perm_SLA_Charged': '',
               'Perm_Field_or_Shipboard': 'N', 'Temp_SLA_Charged': 'G4Z', 'Temp_SLA_Occupied': 'G4Z',
               'Perm_SLA_Occupied': ''}

FIX_VALUES_SR = {'Temp_Allowance_Reason': 'T13', 'Change_of_IBD_Reason': '', 'Perm_Allowance_Reason': 'P02', 'Gender': 'Male',
               'Type': 'Employee.Available for Assignment',  'PAYD/_LOS12/_GYH(S)': 'YNN',
              'Temp_Allowance_Location': 'UKNBP', 
               'Location': 'HMS TRIUMPH', 
               'Status': 'Active Assignment', 'Perm_GYH_Mileage': '', 'Field_or_Shipboard': 'N',
               'Temp_Accomp_Status': '', 'Nationality': 'British',
               'Perm_Allowance_Location': 'UKBPD', 'Organization': 'HMS TRIUMPH', 'Perm_HTD_Location': '',
               'Addressable_Rank': '', 'Temp_HTD_Location': '', 'Perm_SLA_Charged': '',
               'Perm_Field_or_Shipboard': 'N', 'Temp_SLA_Charged': 'G2S', 'Temp_SLA_Occupied': 'G2S',
               'Perm_SLA_Occupied': ''}

FIX_VALUES_GRUNTER_JO = {'Temp_Allowance_Reason': 'T13', 'Change_of_IBD_Reason': '', 'Perm_Allowance_Reason': 'P02', 'Gender': 'Male',
               'Type': 'Employee.Available for Assignment',  'PAYD/_LOS12/_GYH(S)': 'YNN',
              'Temp_Allowance_Location': 'UKNBP', 
              'Location': 'HMS TRIUMPH', 
               'Status': 'Active Assignment', 'Perm_GYH_Mileage': '', 'Field_or_Shipboard': 'N',
               'Temp_Accomp_Status': '', 'Nationality': 'British',
               'Perm_Allowance_Location': 'UKBPD', 'Organization': 'HMS TRIUMPH', 'Perm_HTD_Location': '',
               'Addressable_Rank': '', 'Temp_HTD_Location': '', 'Perm_SLA_Charged': '',
               'Perm_Field_or_Shipboard': 'N', 'Temp_SLA_Charged': 'G2JO', 'Temp_SLA_Occupied': 'G2JO',
               'Perm_SLA_Occupied': ''}

FIX_VALUES_GRUNTER_SO = {'Temp_Allowance_Reason': 'T13', 'Change_of_IBD_Reason': '', 'Perm_Allowance_Reason': 'P02', 'Gender': 'Male',
               'Type': 'Employee.Available for Assignment',  'PAYD/_LOS12/_GYH(S)': 'YNN',
              'Temp_Allowance_Location': 'UKNBP', 
               'Location': 'HMS TRIUMPH', 
               'Status': 'Active Assignment', 'Perm_GYH_Mileage': '', 'Field_or_Shipboard': 'N',
               'Temp_Accomp_Status': '', 'Nationality': 'British',
               'Perm_Allowance_Location': 'UKBPD', 'Organization': 'HMS TRIUMPH', 'Perm_HTD_Location': '',
               'Addressable_Rank': '', 'Temp_HTD_Location': '', 'Perm_SLA_Charged': '',
               'Perm_Field_or_Shipboard': 'N', 'Temp_SLA_Charged': 'G2SO', 'Temp_SLA_Occupied': 'G2SO',
               'Perm_SLA_Occupied': ''}
FIX_VALUES_JUNIOR_RATES_RANKS = ('OR2|OR Main|01', 'OR4|OR Main|01', 'OR2|OR Main|02', 'OR4|OR Main|02')

FIX_VALUES_SENIOR_RATES_RANKS = ('OR6|OR Main|01', 'OR7|OR Main|01', 'OR8|OR Main|01', 'OR9|OR Main|01, OR6|OR Main|02',
                                     'OR7|OR Main|02', 'OR8|OR Main|02', 'OR9|OR Main|02', 'OR9|OR Main|01')
FIX_VALUES_JUNIOR_GRUNTERS_RANKS = ('OF1|OF Main|01', 'OF2|OF Main|01', 'OF1|OF Main|02', 'OF2|OF Main|02')

# appraisals
FIX_VALUES_ABS = ''
FIX_VALUES_LH = ''
FIX_VALUES_PO = ''
FIX_VALUES_CPO = ''