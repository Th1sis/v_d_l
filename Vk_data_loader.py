
# coding: utf-8

# In[148]:


import json
import vk
import sys
import time
from pprint import pprint

def data_read(filepath):
    try:
        with open(filepath) as data_file:
            try:
                data = json.load(data_file)
                return data
            except ValueError:
                print('неверный формат данных или пустой файл')
                sys.exit()             
    except FileNotFoundError:
        print('указанного файла или директории не существует')
        sys.exit()
            
def split_ids(list_id, sublist_vol):
    data_ids=[]
    n=sublist_vol
    vol=len(list_id)//n
    pprint(vol)
    pprint(list_id)
    for i in range(vol):
        if i==0:
            data_ids.append(list_id[0:n])
            pprint(data_ids)
        else:
            data_ids.append(list_id[i*n:(i+1)*n])
            pprint(data_ids)
    data_ids.append(list_id[vol*n:])
    pprint(data_ids)
    return data_ids

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('не задан путь к файлу входных данных формата .json')
    elif len(sys.argv) > 2:
        print('слишком много параметров. Требуется указать название скрипта и путь к файлу входных данных формата .json')
    else:
        data=data_read(sys.argv[1])
        data_ids=split_ids(data["ID"], 1000)

    try:
        session=vk.Session(access_token='b17628ecb17628ecb17628ec02b1294278bb176b17628eceb73d9a475ca00cb1e97dadb')
        vk_api=vk.API(session)
        c=0
        for lists in data_ids:
            res=vk_api.users.get(user_ids=lists, fields=data["fields"])
            pprint(res)
            c+=1
            if c % 3 == 0:
                time.sleep(1)
    except OSError:
            pprint('прервано интернет- соединение')
        

