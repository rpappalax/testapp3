import datetime


def soon_expiring(date_input, warn_threshold_days=60):
    """ Parse dates into 3 categories:
    1. Already expired - date_input <= today (i.e. before today)
    2. Soon expiring - date_input > today but <= the number of upcoming days to watch
    3. Not expiring - date_input > the number of upcoming days to watch
    """

    # format dates
    date_input_formatted = datetime.datetime.strptime(date_input, '%Y-%m-%d')
    today_formatted = datetime.datetime.today()

    # date differential as # of days to warning threshold
    differential_days = (date_input_formatted -  today_formatted).days

    return differential_days
    # print output
    #print(f'DAYS TIL EXPIRATION: {differential_days}')
    """
    if differential_days <= warn_threshold_days:
        return differential_days 
    else:
        return False
    """


if __name__ == '__main__':

    date_input_formatted = '2023-08-06'
    result = soon_expiring(date_input_formatted)
    print(result)

