import os
from os.path import normpath, join

import requests
import yaml
from bs4 import BeautifulSoup
from retrying import retry

_common_config_path = normpath(join(os.getcwd(), "configs/common.yaml"))
_department_config_path = normpath(join(os.getcwd(), "configs/department.yaml"))
_mns_config_path = normpath(join(os.getcwd(), "configs/mns.yaml"))


def load_yaml(file) -> yaml:
    with open(file, 'r') as yaml_file:
        try:
            return yaml.safe_load(yaml_file)
        except Exception as e:
            print("Error While Loading the Yaml File:", file, "\n Error Details:", e)


class Config:
    def __init__(self):
        raise NotImplementedError

    common = load_yaml(_common_config_path)
    department = load_yaml(_department_config_path)
    mns = load_yaml(_mns_config_path)


@retry(stop_max_attempt_number=6, wait_random_min=1000, wait_random_max=2000)
def get_html_soup(url):
    req = requests.get(url=url)
    if req.status_code == 200:
        return BeautifulSoup(req.content, features=Config.common['bs4_parser'])
    else:
        print("Error while accessing site data!\nSite Address:", url, "\nStatus Code:", req.status_code)
        raise ConnectionError
