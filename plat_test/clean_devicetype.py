import requests
import time

import threading




HOST = 'http://api.thingscloud.ir/srv/iot'
TOKEN = 'f05fd34f27484ec997c5809b24b8b404'
THREAD_COUNT = 5

_header = dict(userToken = TOKEN, timeStamp=str(time.time()))



# Get list of devicetypes
res = requests.get(HOST + '/devicetype', headers=_header, params=dict(pageSize=1000))


assert res.status_code == 200


devicetype_list = res.json()['data']['deviceTypes']

print("Number of available devicetype= ", len(devicetype_list))

# Try deleting all device types

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out


def t_delete_devicetypes(ids):
    thread_name = threading.current_thread().name
    print("Thread is started! ", thread_name)
    for x in ids:
        devicetype_id = x['id']

        print("Try deleting by {}: {} ".format(thread_name, devicetype_id))

        res = requests.delete(HOST + '/devicetype/'+devicetype_id, headers=_header)

        if res.status_code==200:
            print("Result {} {} {} ".format(thread_name, res.json()['message']['statusCode'], res.elapsed))
        else:
            print("Error in {} code={}".format(thread_name, res.status_code))




parts = chunkIt(devicetype_list, THREAD_COUNT)

tlist = []
i = 1
for c in parts:
    name = "T-{}".format(i)
    x = threading.Thread(target=t_delete_devicetypes, args=(c,), name=name)
    tlist.append(x)
    x.start()
    i=i+1
    


for x in tlist:
    x.join()





