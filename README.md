# broadvoice Prototype

This is a prototype of a call controller using Broadvoice APIs in Python 3.7. There are 2 parts to it. 

There's a web service to receive signaling events from Broadvoice (i.e. incoming call, DMTF input, etc). This web service is developed using the Flask framework. The web routes are defined in the app/routes.py file.

To send signaling commands to Broadvoice (i.e transfer call, place call on hold with Moh, start recording, etc), the call.py file builds these requests using Broadvoice's REST APIs. This cli is not integrated with the web service.

To set the ngrok callback URL, modify the environment variable, NGROK_CALLBACK, in the .envrc file. This uses the [direnv utility](https://direnv.net). To install direnv, run the following command:

`npm install direnv`

# Configure callback URL

Use the following steps to configure the callback URL. This callback URL is called by Broadvoice when a signaling event occurs.

1. Sign-in to the [Broadvoice dashboard](https://portal.broadvoice.com/sign_in).
2. Navigate to **Settings** -> **Destinations** -> **Call Flow**.
3. click **Edit** on the Remote Call Flow entry.
4. Modify the **Response URL** with the ngrok URL as shown in the below screenshot.

![screenshot for where to configure the response URL to the Flask web service](https://github.com/maximo/broadvoice_prototype/blob/master/response_url.png)

# Broadvoice Documentation

1. https://github.com/xbpio/cpaas-docs/wiki 
2. http://developer.voipment.com/
3. https://github.com/xbpio/cpaas-docs/wiki/REST-API


__This project is under development__
