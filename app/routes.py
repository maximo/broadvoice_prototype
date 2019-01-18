# author: Rui Maximo

import os
# https://stackabuse.com/reading-and-writing-xml-files-in-python/
import xml.etree.ElementTree as ET

from app import app
from flask import Response, request

# application name
print("name: {0}".format(__name__.split('.')[0]))

# flask web service base url
callback = "SPECIFY THE NGROK URL"

# tenant in-memory database (TESTING)
tenants = {}
# add tenants
tenants['+13852100789'] = 'tenant1'

@app.before_request
def log_before_request():
    print('-------------------------------------------------------------------')
    print('Headers:\n', request.headers)
    print('Body: {0}\n'.format(request.form))
# end function


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("caller name: {0}".format(request.form['CallerName']))
        print("caller: {0}".format(request.form['From']))
        print("call id: {0}".format(request.form['CallId']))
    
    if request.method == 'GET':
        return "Broadvoice callback service"

    output = BuildConference(request.form['From'])
    return Response(output, mimetype='text/xml')
# end function


@app.route('/ivr', methods=['POST'])
def ivr():
    ivr_callback = callback + "ivr"

    digits = request.form['Digits']
    print("digits: {0}".format(digits))

    # alternatively use the CallId instead of the caller's phone number
    caller = request.form['From']

    if digits == '1':
        output = CreateResponse("sales-{0}".format(caller))
    if digits == '2':
        output = CreateResponse("support-{0}".format(caller))
    else:
        output = BuildIVR("for sales please press 1, for support press 2.",
                            ivr_callback)

    return Response(output, mimetype='text/xml')
# end function

def BuildConference(name):
    print("conference name: {0}".format(name))

    resp = ET.Element('Response')
    dial = ET.SubElement(resp, 'Dial')
    conf = ET.SubElement(dial, 'Conference')
    conf.text = name
    return ET.tostring(resp)
# end function

def BuildIVR(message, callback):
    resp = ET.Element('Response')
    gather = ET.SubElement(resp, 'Gather')
    gather.set('action', callback)
    gather.set('method', "POST")
    say = ET.SubElement(gather, 'Say')
    say.text = message
    return ET.tostring(resp)
# end function
