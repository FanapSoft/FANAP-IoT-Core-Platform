import requests

HOST = 'http://localhost:5000'

USERNAME = 'TESTUSER'





# Get list of users
res = requests.get(HOST + '/users')

if res.status_code != 200:
    print("Error in getting user-list code={}".format(res.status_code))
    print(res.body)
    exit(-1)

resp_body = res.json()

for user_info in resp_body['users']:
    if user_info['name']==USERNAME:
        print('User {} exists! Token="{}"'.format(USERNAME, user_info['token']))
        exit(0)




res = requests.put(HOST + '/users/add', json=dict(name=USERNAME))

if res.status_code != 200:
    print("Error in adding new user ({}) error_code={}".format(USERNAME,res.status_code))
    exit(-1)

resp_body = res.json()

print('User {} added!. Token="{}"'.format(USERNAME, resp_body['token']))