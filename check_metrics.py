"""Telemetry Probe Expiry Monitor.

PURPOSE:
The purpose of this module is to:
1. Monitor telemetry probe YAML files for expired probes
2. Send a slack notification for (soon-to-be) expired probes

"""
import re
import yaml
import urllib.request
import configparser

from date_checker import soon_expiring


CONFIG_INI = 'check_metrics.ini'
PAYLOAD_JSON = 'slack-payload.json'
WARN_THRESHOLD_DAYS = 7
expired_already = []
expiring_soon = []


METRICS_FILENAME = 'metrics.yaml'


def filestream(filename):
    with open(filename, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f'YAML error: {exc}')


def is_date_format(date_input):
    pattern_str = r'^\d{4}-\d{2}-\d{2}$'
     
    if re.match(pattern_str, date_input):
        return True 
    else:
        return False


#def projects(config):
#    # traverse all projects one-by-one
#    print(config.sections())
#    print(x)
#    for section in config.sections():
#        print(section)
#        
#        for item in config.items(section):
#            print(item)


def project(CONFIG_INI, project_name):
    """ Given a project name, download telemetry yaml, return warn window """

    config = configparser.ConfigParser()
    #c = config.read(CONFIG_INI)
    config.read('check_metrics.ini')

    # pull data from a single project
    url = config.get(project_name, 'file')
    warn = config.get(project_name, 'WARN_THRESHOLD_DAYS')

    # download metrics yaml file
    urllib.request.urlretrieve(url, METRICS_FILENAME)
    return warn


def output_format(metric):
    tmp = metric.replace("']['", ".")
    return tmp.replace("'","").replace("]", "").replace("[", "")


def output_json_row(name_probe, date_expire, days):
   
    prefix = '{ "type": "section", "text": { "type": "mrkdwn", "text": ' 
    suffix = ' } },'
    if int(days) == 0:
        row = f"{name_probe} - expiration: {date_expire} (today)"
    elif int(days) < 0:
        days = abs(days)
        row = f"{name_probe} - expiration: {date_expire} ({days} days ago)"
    else:
        row = f"{name_probe} - expiration: {date_expire} (in {days} days)"
    return f'{prefix} "{row}" {suffix} \n'

def create_probe_lists(metrics, prefix=''):

    if isinstance(metrics, dict):
        for k, v2 in metrics.items():
            p2 = "{}['{}']".format(prefix, k)
            create_probe_lists(v2, p2)

    elif isinstance(metrics, list):
        for i, v2 in enumerate(metrics):
            p2 = "{}[{}]".format(prefix, i)
            create_probe_lists(v2, p2)
    else:
        result = str(metrics)
        tmp = []
        if 'expires' in prefix:
            if is_date_format(result):
                exp = soon_expiring(result, WARN_THRESHOLD_DAYS)
                if exp:
                    #print(f'WARN_THRESHOLD_DAYS: {WARN_THRESHOLD_DAYS}: {prefix}: {result}, {exp}')
                    #tmp = [prefix, result]
                    tmp = [prefix, result, exp]
                    if exp <=0:
                        expired_already.append(tmp)
                    elif (exp > 0 and exp <= WARN_THRESHOLD_DAYS):
                        expiring_soon.append(tmp)
                    else:
                        print('not expiring!')
                        

def generate_payload(expired_already, expiring_soon):
    
    payload = ""
    payload += 'header\n '

    for item in expired_already:
        name_probe = output_format(item[0])
        date_expire = item[1] 
        days = item[2]
        payload +=  output_json_row(name_probe, date_expire, days)

    payload += '\n   middle  \n'

    for item in expiring_soon:
        name_probe = output_format(item[0])
        date_expire = item[1] 
        days = soon_expiring(item[1], warn_threshold_days=WARN_THRESHOLD_DAYS)
        payload += output_json_row(name_probe, date_expire, days)

    payload += 'footer'

    with open(PAYLOAD_JSON, 'a+') as f:
        f.write(payload)

def main():
    project(CONFIG_INI, 'focus-ios') 
    #project(CONFIG_INI, 'firefox-android') 
    metrics = filestream(METRICS_FILENAME)
    create_probe_lists(metrics)
    generate_payload(expired_already, expiring_soon)


    import pprint
    print('======EXPIRED=====')
    #pprint.pprint(expired_already)
    print("")
    print('======EXPIRING=====')
    #pprint.pprint(expiring_soon)

    

if __name__ == '__main__':
    main()
