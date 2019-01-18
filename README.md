# broadvoice Prototype
This is a prototype of a call controller using Broadvoice APIs in Python 3.7. There are 2 parts to it. 

There's a web service to receive signaling events from Broadvoice (i.e. incoming call, DMTF input, etc). This web service is developed using the Flask framework. The web routes are defined in the app/routes.py file.

To send signaling commands to Broadvoice (i.e transfer call, place call on hold with Moh, start recording, etc), the call.py file builds these requests using Broadvoice's REST APIs. This cli is not integrated with the web service.

To set the ngrok callback URL, modify the environment variable, NGROK_CALLBACK, in the .envrc file. This uses the direnv utility, which you can download from https://direnv.net. To install direnv, run the following command:

`npm install direnv`


This project is under development
