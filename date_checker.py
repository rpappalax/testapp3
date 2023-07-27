import datetime


def soon_expiring(exp_date, exp_warning_days=60):
    # setup dates
    expiration_date = datetime.datetime.strptime(exp_date, '%Y-%m-%d')
    today = datetime.datetime.today()

    # compute difference
    ndays = (expiration_date -  today).days

    # print output
    #print(f'DAYS TIL EXPIRATION: {ndays}')
    if ndays <= exp_warning_days:
        return True 
    else:
        return False


if __name__ == '__main__':

    expiration_date = '2023-08-06'
    result = soon_expiring(expiration_date)
    print(result)

