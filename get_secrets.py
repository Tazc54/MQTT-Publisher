import json

#create a function that reads the secrets.json and returns the username and password
def get_secrets():
    with open('secrets.json') as f:
        data = json.load(f)
        username = data['username']
        password = data['password']
    return username, password

# a function that gets the host from the secrets.json
def get_host():
    with open('secrets.json') as f:
        data = json.load(f)
        host = data['host']
    return host