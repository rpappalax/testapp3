import re
import yaml

from date_checker import soon_expiring


EXP_WARNING_DAYS = 60


def filestream(filename):
	with open(filename, "r") as stream:
		try:
			return yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			print(exc)


def is_date(date_input):
    pattern_str = r'^\d{4}-\d{2}-\d{2}$'
     
    if re.match(pattern_str, date_input):
        return True 
    else:
        return False 


def print_dict(v, prefix=''):
    if isinstance(v, dict):
        for k, v2 in v.items():
            p2 = "{}['{}']".format(prefix, k)
            print_dict(v2, p2)

    elif isinstance(v, list):
        for i, v2 in enumerate(v):
            p2 = "{}[{}]".format(prefix, i)
            print_dict(v2, p2)
    else:
        result = str(v)
        #print('{} = {}'.format(prefix, result))
        if 'expires' in prefix:
            print('=====================')
            print(f'{prefix}: {result}')
            if is_date(result):
                exp = soon_expiring(result, EXP_WARNING_DAYS)
                print(f'EXPIRED IN {EXP_WARNING_DAYS} DAYS?: {exp}')
            else: 
                print(f'NEVER EXPIRES')


if __name__ == '__main__':

    metrics = filestream('metrics.yaml')
    print_dict(metrics)
