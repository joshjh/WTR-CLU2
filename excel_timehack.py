import datetime

def excel_timehack(excel_date_integer):
    """ This function takes a excel date integer and will return python datetime objects"""
    try:
        year_zero = datetime.datetime(1899, 12, 30)
        dt = year_zero + datetime.timedelta(days=int(excel_date_integer))
        return dt
    except ValueError as e:
        print('got bad date passed: ', excel_date_integer)

