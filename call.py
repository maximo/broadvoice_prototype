#!/usr/bin/env python3

import requests, time

r = requests.post('http://requestbin.fullcontact.com/u3r3y6u3', data={"ts":time.time()})
print(r.status_code)
print(r.content)
