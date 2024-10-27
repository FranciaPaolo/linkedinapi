# Linkedin Api
This is a Python experiment to access the Linkedin Official Api
https://www.linkedin.com/developers/apps?appStatus=active




## How to - step by step

### Setup the App
Go to https://developer.linkedin.com/

* Select "Create app"
* You will need to create a Linkedin Page (selecting Company, 0-1 employees, ...)
* Add the authorized redirect URLs for your app, in our case because we don't have a real webapp to integrate with Linkedin but simply some python test code we use the following: 
    * https://oauth.pstmn.io/v1/callback
* In the Products "request access" for "Sign In with LinkedIn using OpenID Connect"


![alt text](<./screen/dev_auth.png>)

Setup the "credentials.json" file, filling the values:
* client_id, from the Linkedin App page (from the Auth tab)
* client_secret, from the Linkedin App page (from the Auth tab)
* redirect_uri, from the Linkedin App page (from the Auth tab)


### Run the code

* Step 1, get the **access code** (look at the method get_accessCode)
  * If the "access_code" is empty in the credentials.json, it get it from the browser link
  * The browser link is something like this (replacing the placeholders): https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=openid%20email%20profile
  * You can run open the link directly in the browser
  * You will be redirected to https://oauth.pstmn.io/v1/callback?code=abs
  * Here you need to copy the query string parameter "code" that is the access code
  * Reference flow is exaplaned here: https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow?tabs=HTTPS1

* Step 2, get the **access token** (look at the method get_accessToken)
  * It's a post, application/x-www-form-urlencoded, with the following parameters, it's possible to call it using Postman
    ```
    {    
        "grant_type": "authorization_code",    
        "code": accessCode,    
        "client_id": client_id,
        "client_secret": client_secret,    
        "redirect_uri": redirect_uri
    }
    ```
  * In the response you will get a json with the field "access_token"

* Step 3, finally we can call the Api to get the user "info" (look at the method get_me)
  * It's a Get to https://api.linkedin.com/v2/userinfo
  * Headers are in this way
  ```
  {"Authorization": "Bearer {access_token}"}
  ```


## Open points

* It's not easy to read the documentation, sometimes it seems not updated
* I was not able to get the list of my connections from the Api. I found this reference but I'm receiving some errors https://learn.microsoft.com/en-us/linkedin/shared/integrations/people/connections-api