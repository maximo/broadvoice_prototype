# author: Rui Maximo

import json
import os
# https://stackabuse.com/reading-and-writing-xml-files-in-python/
import xml.etree.ElementTree as ET

import requests
from app import app
from flask import Response, request

# application name
print("name: {0}".format(__name__.split('.')[0]))


class BroadVoice:
    def __init__(self):
        self.auth=(os.environ['API_KEY'], '')
        self.moh = 'broadvoice' # TODO: set url for music on hold
        # flask web service base url
        self.callback = os.environ['NGROK_CALLBACK']
        self.xbp_headers = {'Accept': 'application/json',
                            'Content-Type': 'application/json'}

        # tenant in-memory database (TESTING)
        self.tenants = {}
        # add tenants
        self.tenants['+13852100789'] = 'tenant1'

        # track active calls
        self.active_calls = {}
    # end function

    def ivr_play_audio(self, url, loop_count):
        resp = ET.Element('Response')
        audio = ET.Element(resp, 'Play')
        audio.set('loop', loop_count)
        audio.text = url
        return ET.tostring(resp)
    # end function

    def ivr_speak(self, message):
        resp = ET.Element('Response')
        say = ET.Element(resp, 'Say')
        say.text = message
        return ET.tostring(resp)
    # end function

    def ivr_hangup(self, message):
        resp = ET.Element('Response')
        say = ET.Element(resp, 'Say')
        say.text = message
        ET.Element(resp, 'Hangup')
        return ET.tostring(resp)
    # end function

    def conference(self, name, mute = False, record = False):
        room = 'room-' + name
        print("conference name: {}".format(room))

        resp = ET.Element('Response')
        dial = ET.SubElement(resp, 'Dial')
        conf = ET.SubElement(dial, 'Conference')
        if mute == True:
            conf.set('muted', 'true')
        if record == True:
            conf.set('record', 'record-from-start')
        else: 
            conf.set('record', 'do-not-record')
        conf.set('beep', 'false') # do not play beep when joining/exiting
        conf.set('musicOnHoldUrl', self.moh)
        conf.text = room 
        return ET.tostring(resp)
    # end function

    def ivr(self, message):
        resp = ET.Element('Response')
        gather = ET.SubElement(resp, 'Gather')
        gather.set('action', self.callback + 'ivr')
        gather.set('method', "POST")
        say = ET.SubElement(gather, 'Say')
        say.text = message
        return ET.tostring(resp)
    # end function

    def call(self, ext, phone):
        print("call")
        payload = {'from': ext, # must be configured in Broadvoice dashboard: 401
                    'to': phone,
                    'display_number': phone,
                    'display_name': 'customer'
                }
        result = requests.post('https://api.xbp.io/v1/calls',
                auth=self.auth,
                data=json.dumps({**payload}),
                headers=self.xbp_headers
            )
        resp = json.loads(result.content)
        print(resp)
        callid = resp['call_uuid']
        self.active_calls[callid] = ext
        return result
    # end function

    def hold(self, callid):
        print("call on hold")
        return self.conference(callid)
    # end function
        
    def unhold(self, callid):
        print("call unhold")
        dest = self.active_calls[callid]
        print("destination: {}".format(dest))
        return self.transfer(dest)
    # end function
        
    def transfer(self, callid, dest):
        print("call transfer")
        payload = {'destination': dest}
        result = requests.put('https://api.xbp.io/v1/calls/{}'.format(
                callid
            ),
            auth=self.auth,
            data=json.dumps({**payload}),
            headers=self.xbp_headers
        )
        resp = json.loads(result.content)
        print(resp)
        return result
    # end function

    def hangup(self, callid):
        print("call hangup")
        payload = {}
        result = requests.delete('https://api.xbp.io/v1/calls/{}'.format(
                callid
            ),
            auth=self.auth,
            data=json.dumps({**payload}),
            headers=self.xbp_headers
        )
        resp = json.loads(result.content)
        print(resp)
        return result
    # end function
# end class


provider = BroadVoice()

@app.before_request
def log_before_request():
    print('-------------------------------------------------------------------')
# end function

@app.after_request
def log_after_request(response):
    print('-------------------------------------------------------------------')
    return response
# end function

@app.route('/', methods=['GET', 'POST'])
def index():
    print("caller name: {}".format(request.form['CallerName']))
    print("call id: {}".format(request.form['CallId']))
    print("account id: {}".format(request.form['AccountId']))
    print("location id: {}".format(request.form['LocationId']))
    print("from: {}".format(request.form['From']))
    print("to: {}".format(request.form['To']))
    print("direction: {}".format(request.form['Direction']))
    
    output = provider.conference(request.form['From'])
    print("room: {}".format(output))
    return Response(output, mimetype='text/xml')
# end function

@app.route('/call/<extension>/<phone>', methods=['GET'])
def call(extension, phone):
    print("ext: {}".format(extension)) # extension should be 401 (sandbox)
    print("phone: {}".format(phone))
    resp = provider.call(extension, phone)
    print(resp)
    return Response(resp, mimetype='application/json')
# end function

@app.route('/transfer/<callid>/<dest>', methods=['GET'])
def transfer(callid, dest):
    print("callId: {}".format(callid))
    print("destination: {}".format(dest))
    resp = provider.transfer(callid, dest)
    print(resp)
    return Response(resp, mimetype='application/json')
# end function

@app.route('/hold/<callid>', methods=['GET'])
def hold(callid):
    print("callId: {}".format(callid))
    resp = provider.hold(callid)
    print(resp)
    return Response(resp, mimetype='application/json')
# end function

@app.route('/unhold/<callid>', methods=['GET'])
def unhold(callid):
    print("callId: {}".format(callid))
    resp = provider.unhold(callid)
    print(resp)
    return Response(resp, mimetype='application/json')
# end function

@app.route('/hangup/<callid>', methods=['GET'])
def hangup(callid):
    print("callId: {}".format(callid))
    resp = provider.hangup(callid)
    print(resp)
    return Response(resp, mimetype='application/json')
# end function

@app.route('/ivr', methods=['POST'])
def ivr():
    digits = request.form['Digits']
    print("digits: {0}".format(digits))

    # alternatively use the CallId instead of the caller's phone number
    caller = request.form['From']

    if digits == '1':
        output = CreateResponse("sales-{}".format(caller))
    if digits == '2':
        output = CreateResponse("support-{}".format(caller))
    else:
        output = provider.ivr("for sales please press 1, for support press 2.",
                            ivr_callback)

    return Response(output, mimetype='text/xml')
# end function
