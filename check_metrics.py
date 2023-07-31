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
WARN_THRESHOLD_DAYS = 30
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


def print_dict(metrics, prefix=''):

    if isinstance(metrics, dict):
        for k, v2 in metrics.items():
            p2 = "{}['{}']".format(prefix, k)
            print_dict(v2, p2)

    elif isinstance(metrics, list):
        for i, v2 in enumerate(metrics):
            p2 = "{}[{}]".format(prefix, i)
            print_dict(v2, p2)
    else:
        result = str(metrics)
        tmp = []
        if 'expires' in prefix:
            if is_date_format(result):
                exp = soon_expiring(result, WARN_THRESHOLD_DAYS)
                if exp:
                    #print(f'WARN_THRESHOLD_DAYS: {WARN_THRESHOLD_DAYS}: {prefix}: {result}, {exp}')
                    tmp = [prefix, result]
                    if exp <=0:
                        expired_already.append(tmp)
                    elif (exp > 0 and exp <= WARN_THRESHOLD_DAYS):
                        expiring_soon.append(tmp)
                    else:
                        print('not expiring!')
                        



if __name__ == '__main__':

    project(CONFIG_INI, 'focus-ios') 
    # open yaml file contents
    metrics = filestream(METRICS_FILENAME)
    print_dict(metrics)

    print('======EXPIRED=====')
    print(expired_already)
    print("")
    print('======EXPIRING=====')
    print(expiring_soon)

