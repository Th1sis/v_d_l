
# coding: utf-8

# In[168]:


import json
import vk
import sys
import time
from pprint import pprint

def data_read(filepath):                                         #reading input json file function
    try:                                                         #checking if the file exists      
        with open(filepath) as data_file:                       
            try:                                                 # checking data format and avaiability 
                data = json.load(data_file)
                return data
            except ValueError:
                print('неверный формат данных или пустой файл')
                sys.exit()             
    except FileNotFoundError:
        print('указанного файла или директории не существует')
        sys.exit()
            
def split_ids(list_id, sublist_vol):                             # splitting list_ids for the request
    data_ids=[]
    n=sublist_vol                                                # volume of the slices
    vol=len(list_id)//n                                          # number of slices
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
        try:                                                      #check if list if ID's exists
            data_ids=split_ids(data["ID"], 1000)                  #setting maximum size of slices in the single request 
        except KeyError:                                          #vk_api has limitations up to 1000 id's per request  
            print('отсутствует поле ID в исходном файле')         
        

        try:
            session=vk.Session(access_token='b17628ecb17628ecb17628ec02b1294278bb176b17628eceb73d9a475ca00cb1e97dadb') #auth with 
            vk_api=vk.API(session)                                                                                     #app_accsess_tocken
            c=0
            requests_number_per_second=3                                                            #vk_api can execute up to 3 requests
            for lists in data_ids:                                                                  #per second for the app
                try:                                                                   #checking if exists the "fields" key
                    res=vk_api.users.get(user_ids=lists, fields=data["fields"])
                    c+=1
                    if c % requests_number_per_second == 0:
                        time.sleep(1)                                                  #wait time till next request to not exceed the 
                except KeyError:                                                       #request limitations
                    print('отсутствует поле fields в исходном файле')                
        except KeyError:                                                               #checking net status exception block
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


# In[178]:


get_ipython().system('python.exe C:\\\\Users\\Theseus\\Desktop\\Vk_data_loader.py D:\\\\t\\a.json')

