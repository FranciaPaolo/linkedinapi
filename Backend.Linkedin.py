import requests
import json
from datetime import datetime
import webbrowser
from urllib.parse import parse_qs, urlparse    


def read_creds(filename):
    with open(filename) as f:    
        credentials = json.load(f)    
        return credentials

def open_url(url):    
    print(url)    
    webbrowser.open(url)

def parse_redirect_uri(redirect_response):    
    url = urlparse(redirect_response)    
    url = parse_qs(url.query)    
    return url["code"][0]

def save_creds(filename, data):    
    data = json.dumps(data, indent=4, default=str)    
    with open(filename, "w") as f:    
        f.write(data)

def headers(access_token):    
    headers = {       
        "Authorization": f"Bearer {access_token}",       
        "cache-control": "no-cache",       
        "X-Restli-Protocol-Version": "2.0.0",       
        }    
    return headers
    
def get_accessCode(client_id, redirect_uri):

    scope="openid%20email%20profile"
    browser_url=f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    open_url(browser_url)    
    redirect_response = input("Paste the full redirect URL here:")    
    auth_code = parse_redirect_uri(redirect_response)
    return auth_code

def get_accessToken(accessCode, client_id, client_secret, redirect_uri):
    
    params = {    
        "grant_type": "authorization_code",    
        "code": accessCode,    
        "client_id": client_id,
        "client_secret": client_secret,    
        "redirect_uri": redirect_uri
        }    
    print(params)
    
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response = requests.post("https://www.linkedin.com/oauth/v2/accessToken", data=params, headers=headers)
    json_data = json.loads(response.text)

    print(f"""Access Token Response from  https://www.linkedin.com/oauth/v2/accessToken\n
           {response.text}
           """)
    
    print(json_data)
    
    return json_data["access_token"]


def get_me(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    print(headers)
    response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
    
    print(f"""Me Response from  https://api.linkedin.com/v2/userinfo\n
           {response.text}
           """)


def get_connections(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    print(headers)
    response = requests.get("https://api.linkedin.com/v2/connections?q=viewer&start=0&count=50", headers=headers)
    
    print(f"""Connections Response from  https://api.linkedin.com/v2/connections\n
           {response.text}
           """)


# Step1)
# Here he we get the access_code in the browser ####################################################################################
print("step 1) open browser to get the access code")
credentials = read_creds("credentials.json")

if(not credentials["access_code"]):

    input_response = input("Do you want to proceed getting the access_code? [yes|any other text will means no]")
    if(input_response=="yes"):
        credentials["access_code"] = get_accessCode(credentials["client_id"],credentials["redirect_uri"])
        credentials["access_code_created"]=datetime.now()
        print(credentials)
        save_creds("credentials.json",credentials)
    else:
        print("ok let's stop here")
        exit()
else:
    print("skip getting access_code, it's already in the credentials")

# Step2)
# Here he we get the access_token using the Api ####################################################################################
print("\n\nstep 2) get the access token, it expires in 40 seconds")
if(not credentials["access_token"]):
    input_response = input("Do you want to proceed getting the access_code? [yes|any other text will means no]")
    if(input_response=="yes"):
        credentials["access_token"] = get_accessToken(credentials["access_code"], credentials["client_id"], credentials["client_secret"], credentials["redirect_uri"])
        credentials["access_token_created"]=datetime.now()
        print(credentials)
        save_creds("credentials.json",credentials)
    else:
        print("ok let's stop here")
        exit()
else:
    print("skip getting access_token, it's already in the credentials")

# Step3)
# Here he we call the "info" Api ####################################################################################
print("\n\nstep 3) call the my profile api")
input_response = input("Do you want to proceed getting the me api? [yes|any other text will means no]")
if(input_response=="yes"):
    get_me(credentials["access_token"])
else:
    print("ok let's stop here")
    exit()

# Step4)
# Here he we call the "connection" Api ####################################################################################
# !!!!Unfortunately it's not working (it seems that the the scope is not correct)
print("\n\nstep 4) call the connections api")
input_response = input("Do you want to proceed getting the connections api? [yes|any other text will means no]")
if(input_response=="yes"):
    get_connections(credentials["access_token"])
else:
    print("ok let's stop here")
    exit()
