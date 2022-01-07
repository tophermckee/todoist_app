import requests, time, json, pprint, base64, datetime

pp = pprint.PrettyPrinter(indent=2)

def update_creds_file(credentials_file, json_object):
    with open(credentials_file, 'w', encoding='utf-8') as f:
        json.dump(json_object, f, ensure_ascii=False, indent=4)
        f.close()

def get_todoist_auth_token():
    url = f"https://todoist.com/oauth/authorize?client_id={credentials['todoist_client_id']}&scope=data:read&state=12345678"

    print(f"Use the link below to authorize Todoist:\n{url}")

    auth_token_raw = input("Copy/paste the URL below.\n")

    credentials['todoist_auth_token'] = auth_token_raw[auth_token_raw.index("code") + 5 : auth_token_raw.index("&state=")]

    update_creds_file(credentials_file='creds.json', json_object=credentials)

def get_todoist_access_token():
    with open('creds.json') as file:
        credentials = json.load(file)

    access_token = requests.post(
        url="https://todoist.com/oauth/access_token",
        params={
            "client_id": credentials['todoist_client_id'],
            "client_secret": credentials['todoist_client_secret'],
            "code": credentials['todoist_auth_token'],
            'grant_type': 'authorization_code'
        }
    ).json()

    pp.pprint(access_token)

def get_active_tasks():
    output = []

    task_response = requests.get(
        url="https://api.todoist.com/rest/v1/tasks",
        headers={
            'Authorization': f"Bearer {credentials['todoist_access_token']}",
            'Content-Type': "application/json",
        }
    ).json()

    for item in task_response:
        if 'due' in item.keys():
            if item['due']['date'] == datetime.datetime.today().strftime('%Y-%m-%d'):
                output.append(item)
                
    return output

if __name__ == "__main__":
    with open('creds.json') as file:
        credentials = json.load(file)

    if 'todoist_auth_token' not in credentials.keys():
        get_todoist_auth_token()

    with open('creds.json') as file:
        credentials = json.load(file)

    with open('creds.json') as file:
        credentials = json.load(file)
    
    pp.pprint(get_active_tasks())
    

