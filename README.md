# broadvoice Prototype

This is a prototype of a call controller using Broadvoice APIs in Python 3.7. There are 2 parts to it. 

There's a web service to receive signaling events from Broadvoice (i.e. incoming call, DMTF input, etc). This web service is developed using the Flask framework. The web routes are defined in the app/routes.py file.

To send signaling commands to Broadvoice (i.e transfer call, place call on hold with Moh, start recording, etc), the call.py file builds these requests using Broadvoice's REST APIs. This cli is not integrated with the web service.

To set the ngrok callback URL, modify the environment variable, NGROK_CALLBACK, in the .envrc file. This uses the [direnv utility](https://direnv.net). To install direnv, run the following command:

`npm install direnv`

# Configure Ngrok

To expose the flask web service external, use ngrok
# Configure callback URL

For Broadvoice to send signaling events to your Flask web service, it needs the URL to the Flask web service running locally exposed externally by ngrok. Use the following steps to configure this callback URL. The callback URL is called by Broadvoice when a signaling event occurs.

1. Sign-in to the [Broadvoice dashboard](https://portal.broadvoice.com/sign_in).
2. Navigate to **Settings** -> **Destinations** -> **Call Flow**.
3. click **Edit** on the Remote Call Flow entry.
4. Modify the **Response URL** with the ngrok URL as shown in the below screenshot.

![screenshot for where to configure the response URL to the Flask web service](https://github.com/maximo/broadvoice_prototype/blob/master/response_url.png)

# Create Python Virtual Environment

Flask runs in a Python3 virtual environment. To create this virtual environment, run the following command:

`python3 -m venv venv`

This create a virtual environment named `venv`. You can change this name to your liking.

# Run Web Service

Before starting the web service, activate the virtual environment (created in the previous section) by running the following command:

`source venv/bin/activate`

Next, configure the file, .envrc, to specify the ngrok URL in the environment variable `NGROK_CALLBACK`.

To start the Flask web service, open a terminal window, navigate to this folder, and run the following command:

`flask run`


# Broadvoice Documentation

1. https://github.com/xbpio/cpaas-docs/wiki 
2. http://developer.voipment.com/
3. https://github.com/xbpio/cpaas-docs/wiki/REST-API


__This project is under development__
