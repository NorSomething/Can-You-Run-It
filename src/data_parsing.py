import requests
import json
import re
import os
from bs4 import BeautifulSoup

def get_html_file(data):

    with open("reqs.html", 'w') as f:
        print(data, file=f)


def get_game_data(appid):
    url = f"https://store.steampowered.com/api/appdetails/?appids={appid}&l=english"
    res = requests.get(url)
    data = res.json()
 
    return data[str(appid)]["data"]

def parser(data):

    linux_reqs = data['linux_requirements']['minimum']
    get_html_file(linux_reqs)

    HTMLFILE = open('reqs.html', 'r')
    reqs = HTMLFILE.read()
    S = BeautifulSoup(reqs, 'html.parser')
    parsed_data = (S.ul.text).split()

    cpu_specs_needed = ""

    print(parsed_data)


    print(cpu_specs_needed)






data = get_game_data(730)
parser(data)

def spec_getter():

    mem_address = "/proc/meminfo"
    cpu_address = "/proc/cpuinfo"

    core_count = 0

    with open(mem_address, 'r') as f:
        ram_total = f.readline().split()[1]
        #print(ram_total)

    with open(cpu_address, 'r') as f:
        data = f.readlines()

        for i in data:
            if 'processor' in i:
                core_count += 1

        cpu_model = data[4]

        print(core_count)
        cpu_model_list = (cpu_model.split()[3::])

        model = ""

        for i in cpu_model_list:
            model+=i+" "

        cpu_model = model

        print(cpu_model)

    #capturing result
    storage_data = os.popen('df').read()
    storage_remainging = (int(storage_data.split()[10])/(1024))/(1024)
    print(storage_remainging)

    

