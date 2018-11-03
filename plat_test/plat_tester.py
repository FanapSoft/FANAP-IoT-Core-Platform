import argparse
import requests
from multiprocessing.pool import Pool
import multiprocessing
import threading
import json
import csv


HOST = 'http://api.thingscloud.ir/srv/iot'

TOKEN = 'f05fd34f27484ec997c5809b24b8b404'


def process_args():
    parser = argparse.ArgumentParser(description='Interactive Tests')
    parser.add_argument('command',  choices=['add','delete','list', 'show'], help='Select type of test. ' 
    '"add": Add new devicetypes and store responses in file. '
    '"list": Compare devicetype-list with response file. '
    '"show": Compare devicetype-show content with resonse file. '
    '"delete-all: Delete all defined devicetypes. '
    
    )
    parser.add_argument('-t', metavar='token', dest='token', help='Overwrite access token', default=TOKEN)
    parser.add_argument('-H', metavar='host', dest='host', help='Determine HOST address default={}'.format(HOST), default=HOST)
    parser.add_argument('-c', metavar='cnt', dest='cnt', help='Test count for add', default=10, type=int)
    parser.add_argument('-prefix', metavar='prefix', dest='prefix', help='Name prefix for test operations', default='TEST')
    parser.add_argument('-T', metavar='thread-cnt', dest='thread', help='Thread count for concurrent process default=1', default=1, type=int)
    parser.add_argument('-f', metavar='file', dest='file', help='Target file for test default=out.csv', default='out.csv')
    args = parser.parse_args()

    return args

args = process_args()

def get_idname_dict_from_csv(filename):
    file_dict = {}
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            file_dict[row['id']]=row['name']
    return file_dict

class ApiAccess:
    def __init__(self, args):
        
        self._header = dict(userToken=args.token, timestamp='12')
        self._host = args.host
    

    def post(self, endpoint, params, body={}):
        return requests.post(self._host + endpoint, headers=self._header, params=params, json=body)

    def get(self, endpoint, params={}):
        return requests.get(self._host + endpoint, headers=self._header, params=params)


def capture_request(api, method, endpoint, result, params, **kwargs):
    process_name = multiprocessing.current_process().name


    if method=='POST':
        res = api.post(endpoint, params)
    elif method=='GET':
        res = api.get(endpoint, params)
    else:
        return 

    try:
        json_body = res.json()
    except:
        json_body = {}


    print('{}: {}'.format(process_name, res.status_code))

    result.append(
        dict(
            code = res.status_code,
            content = res.text,
            body = json_body,
            time = res.elapsed,
            process = process_name,
            **kwargs
        )
    )

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

def _worker_add_devicetypes(args, names):
    
    api = ApiAccess(args)

    result = []
    for n in names:
        params = dict(
            name = n,
            encryptionEnabled = True,
            attributeTypes = '[{"name":"impfield", "type":"String"}]',
        )

        capture_request(api, 'POST', '/devicetype', result, params, name=n)

    return result

def _worker_show_devicetypes(args, ids):
    api = ApiAccess(args)

    result = []

    for id in ids:

        capture_request(api,'GET', '/devicetype/'+id, result, {}, id=id)
    
    return result

def _get_devicetype_list(args):
    # Get list of devicetypes
    api = ApiAccess(args)

    res = api.get('/devicetype', params=dict(pageSize=1000))

    assert res.status_code == 200

    devicetype_list = res.json()['data']['deviceTypes']

    return devicetype_list

def run_list_check(args):
    print('Verify added devices')

    devicetype_list = _get_devicetype_list(args)

    rx_dict = {}
    for x in devicetype_list:
        rx_dict[x['id']]= x['name']
    

    file_dict = get_idname_dict_from_csv(args.file)

    # Verify lists
    list_ok = True
    for _id, _name in file_dict.items():
        if not _id in rx_dict:
            print("ID={} is not available in list".format(_id))
            list_ok = False
            continue
        
        if rx_dict[_id] != _name:
            print("ID={} name varies {}!={}".format(_id, _name, rx_dict[_id]))
            list_ok = False
    
    if list_ok:
        print("OK! All ids in file is present in devietype-list!")

def run_add(args):
    print('Add {} devicetypes...'.format(args.cnt))

    names = ['{}-{:03}'.format(args.prefix, i) for i in range(args.cnt)]

    parts = [(args, x) for x  in chunkIt(names, args.thread)]

    with Pool(processes=4) as pool:
        results = pool.starmap(_worker_add_devicetypes, parts)


        with open(args.file,'w',newline='') as csvfile:

            fields = ['id', 'name', 'time','process']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()

            for proc_result in results:
                for resp in proc_result:

                    if resp['code'] == 200:
                        
                        if not resp['body']['data']:
                            print("Error in content of response: ", str(resp))    
                        else:
                            writer.writerow(dict(
                                id = resp['body']['data']['id'],
                                name = resp['name'],
                                time = resp['time'].total_seconds(),
                                process = resp['process']
                            ))
            


    #print(results)

def run_show(args):
    print('Verify show for devicetypes')

    file_dict = get_idname_dict_from_csv(args.file)


    id_list = list(file_dict.keys())

    parts = [(args, x) for x  in chunkIt(id_list, args.thread)]

    with Pool(processes=4) as pool:
        results = pool.starmap(_worker_show_devicetypes, parts)

        all_ok = True
        cnt = 0
        for proc_result in results:
            for resp in proc_result:
                # Here check device show list

                if resp['code'] == 200:
                    content = resp['body']['data']
                    resp_id = content['id']

                    if not resp_id in id_list:
                        print("ID is not valid {}".format(resp_id))
                        all_ok = False
                        continue
                    
                    
                    if file_dict[resp_id] != content['name']:
                        print("Name is not valid id:{} name:{} exp_name:{}".format(
                            resp_id, content['name'], file_dict[resp_id]
                        ))
                        all_ok = False
                        continue
                    
                    attributeTypes = [{"name":"impfield", "type":"string"}]

                    if attributeTypes != content['attributeTypes']:
                        print("attributeTypes is not valid id:{} {} {}".format(resp_id, content['attributeTypes'], attributeTypes))
                        continue
                    cnt = cnt+1

        if all_ok:
            print("Devicetype-show compare is OK (len={})".format(cnt))            



cmd_dict = dict (
    add = run_add,
    list = run_list_check,
    show = run_show,
)

# Execute the command
cmd_dict[args.command](args)

