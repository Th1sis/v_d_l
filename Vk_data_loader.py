
# coding: utf-8

# In[156]:


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
    for i in range(vol):
        if i==0:
            data_ids.append(list_id[0:n])
        else:
            data_ids.append(list_id[i*n:(i+1)*n])
    data_ids.append(list_id[vol*n:])
    return data_ids

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('не задан путь к файлу входных данных формата .json')
    elif len(sys.argv) > 2:
        print('слишком много параметров. Требуется указать название скрипта и путь к файлу входных данных формата .json')
    else:
        data=data_read(sys.argv[1])
        try:
            data_ids=split_ids(data["ID"], 1000)
        except KeyError:
            print('отсутствует поле ID в исходном файле')
        

        try:
            session=vk.Session(access_token='b17628ecb17628ecb17628ec02b1294278bb176b17628eceb73d9a475ca00cb1e97dadb')
            vk_api=vk.API(session)
            c=0
            requests_number_per_second=3
            for lists in data_ids:
                try:
                    res=vk_api.users.get(user_ids=lists, fields=data["fields"])
                    pprint(res)
                    c+=1
                    if c % requests_number_per_second == 0:
                        time.sleep(1)
                except KeyError:
                    print('отсутствует поле fields в исходном файле')                
        except KeyError:
            pprint('отсутствует поле fields в исходном файле')
            sys.exit() 
        except ConnectionAbortedError:
            pprint('сервис разорвал соединение')
            sys.exit() 
        except ConnectionRefusedError:
            pprint('в попытке соединения отказано')
            sys.exit() 
        except BrokenPipeError:
            pprint('ошибка соединения')
            sys.exit() 
        except ConnectionResetError:
            pprint('соединение сброшено')
            sys.exit() 
        except OSError:
            pprint('отсутствует интернет-соединение')
            sys.exit()        

