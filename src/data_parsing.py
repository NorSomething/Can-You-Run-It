import requests
import json
import re
import os
from bs4 import BeautifulSoup

'''
    ToDo : Handle no requirements data in steam page of some games
           CPU comparison fix
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
        
        print("Linux reqs not found, Using pc requirements data.")
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

    game_memory = re.search(r"\d+", data_list[1]).group()
    game_storage = re.search(r"\d+", data_list[3]).group()
    game_intel_processor = re.search(r"i\d+", data_list[0]).group()

    # game_system_req_dict = {
    #     'Processor' : game_thread_count,
    #     'Memory' : game_memory,
    #     'Graphics' : data_list[2],
    #     'Storage' : game_storage
    # }

    if 'i3' in game_intel_processor:
        game_thread_count = 4
    if 'i5' in game_intel_processor:
       game_thread_count = 8
    if 'i7' in game_intel_processor:
        game_thread_count = 16


    game_system_req_dict = {
        'Processor' : game_thread_count,
        'Memory' : game_memory,
        'Graphics' : data_list[2],
        'Storage' : game_storage
    }

    return game_system_req_dict


def spec_getter():

    mem_address = "/proc/meminfo"
    cpu_address = "/proc/cpuinfo"

    thread_count = 0

    with open(mem_address, 'r') as f:
        ram_total = f.readline().split()[1]
        #print(ram_total)

    with open(cpu_address, 'r') as f:
        data = f.readlines()

        for i in data:
            if 'processor' in i:
                thread_count += 1

        cpu_model = data[4]

        cpu_model_list = (cpu_model.split()[3::])

        model = ""

        for i in cpu_model_list:
            model+=i+" "

        cpu_model = model

    #capturing result
    storage_data = os.popen('df').read()
    storage_remainging = (int(storage_data.split()[10])/(1024))/(1024)
    ram_total = (int(ram_total)/1024)/1024

    user_system_spec_dict = {
        'Processor thread count' : thread_count,
        'Memory' :  ram_total,
        'Graphics' : 'wip',
        'Storage' : storage_remainging
    }

    return user_system_spec_dict
    

def comparator(appid):

    #steam_game_id = int(input("Enter steam game app id : "))
    steam_game_id = int(appid) #for testing

    stuff = get_game_data(steam_game_id)

    user_system_spec_dict = spec_getter()
    game_system_req_dict = parser(stuff)

    print("Your specs : ")

    for x,y in user_system_spec_dict.items():
        print(f"{x} : {y}")

    print("Game's Specs : ")

    for x,y in game_system_req_dict.items():
        print(f"{x} : {y}")

    processor_flag = False
    ram_flag = False
    storage_flag = False 

    can_run_flag = False
    bottleneck_list = []

    if int(user_system_spec_dict['Processor thread count']) >= int(game_system_req_dict['Processor']):
        processor_flag = True 
    if int(user_system_spec_dict['Memory']) >= int(game_system_req_dict['Memory']):
        ram_flag = True 
    if int(user_system_spec_dict['Storage']) >= int(game_system_req_dict['Storage']):
        storage_flag = True

    if processor_flag and ram_flag and storage_flag:
        #print("You can run this game!")
        can_run_flag = True
    
    if not processor_flag:
        # print("You have a processor bottleneck.")
        bottleneck_list.append('Processor Bottleneck.')

    if not ram_flag:
        #print("You do not have enough ram.")
        bottleneck_list.append("Ram Bottleneck.")
    if not storage_flag:
        #print("You do not have enough storage left for this game.")
        bottleneck_list.append("Storage Bottleneck")

    return user_system_spec_dict, game_system_req_dict, can_run_flag, bottleneck_list

def final_checker(appid):
    
    stuff = comparator(appid)
    

    final_dict = {
        'user_specs' : stuff[0],
        'game_specs' : stuff[1],
        'can run' : stuff[2],
        'bottlenecks' : stuff[3]
    }

    return final_dict




