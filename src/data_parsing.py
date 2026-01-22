import requests
import json
import re
import os
from bs4 import BeautifulSoup

'''
    ToDo : Handle no requirements data in steam page of some games
'''

def get_html_file(data, name):

    with open(f"{name}_reqs.html", 'w') as f:
        print(data, file=f)

def get_test_json(data):

    with open("testdata.json", "w") as f:
        json.dump(data, f, indent=4)

def get_parsed_data(name):
    
    HTMLFILE = open(f'{name}_reqs.html', 'r')
    reqs = HTMLFILE.read()
    S = BeautifulSoup(reqs, 'html.parser')
    linux_parsed_data = (S.ul.text)

    split_data = linux_parsed_data.split(':')   

    return split_data 


def get_game_data(appid):
    url = f"https://store.steampowered.com/api/appdetails/?appids={appid}&l=english"
    res = requests.get(url)
    data = res.json()
 
    return data[str(appid)]["data"]

def parser(data):

    get_test_json(data) #for user reference

    linux_reqs = data['linux_requirements']['minimum']
    pc_reqs = data['pc_requirements']['minimum']

    get_html_file(linux_reqs, 'linux')
    get_html_file(pc_reqs, 'pc')
    
    print("Using linux requirements data.")

    split_data = get_parsed_data('linux')

    data_list = []

    if len(split_data) < 3: #no linux reqs there
        
        print("Using pc requirements data.")
        split_data = get_parsed_data('pc')

    if len(split_data) < 3: #no reqs present at all

        print("No requirements data available.")
        return

    for i in range(len(split_data)):
        if 'Processor' in split_data[i]:
            data_list.append(split_data[i+1])
        if 'Memory' in split_data[i]:
            data_list.append(split_data[i+1])
        if 'Graphics' in split_data[i]:
            data_list.append(split_data[i+1])
        if 'Storage' in split_data[i]:
            data_list.append(split_data[i+1])

    user_memory = re.search(r"\d+", data_list[1]).group()
    user_storage = re.search(r"\d+", data_list[3]).group()

    user_system_spec_dict = {
        'Processor' : data_list[0],
        'Memory' : user_memory,
        'Graphics' : data_list[2],
        'Storage' : user_storage
    }

    for x,y in user_system_spec_dict.items():
        print(f"{x}\t{y}")

stuff = get_game_data(578080)
parser(stuff)

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

    

