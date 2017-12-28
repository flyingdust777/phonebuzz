from django.shortcuts import render

from threading import Thread
import time
# Create your views here.

from functools import wraps
from twilio.request_validator import RequestValidator
from django.views.decorators.http import require_POST

from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.rest import Client

import os

account_sid = "account_sid" #twilio account_sid
auth_token = "auth_token" #twilio auth_token
originNumber = "WHITELISTED PHONE NUMBER HERE" #EX: 6508522194
targetURL = "http://893f543c.ngrok.io" #put hosted url here
client = Client(account_sid, auth_token)


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(auth_token)

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.build_absolute_uri(),
            request.POST,
            request.META.get('HTTP_X_TWILIO_SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if
        # it's not
        if request_valid:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return decorated_function

@csrf_exempt
def index(request):
    #return HttpResponse("Hello, world. You're at the fizzy index.")
    # resp = VoiceResponse()
    # # gather = Gather(input='dtmf', finishOnKey='*')
    # number = request.POST.get('Digits')
    # if number is not None:
    # 	fizzString = ''
    # 	for x in range(1, int(number) + 1):
    # 		if x % 15 == 0:
    # 			fizzString += 'Fizzbuzz, '
    # 		elif x % 5 == 0:
    # 			fizzString += 'Buzz, '
    # 		elif x % 3 == 0:
    # 			fizzString += 'Fizz, '
    # 		else:
    # 			fizzString += str(x) + ', '
    # 	resp.say(fizzString)
    # 	return HttpResponse(str(resp), content_type='text/xml')
    # with resp.gather(input='dtmf',finishOnKey='*') as g:
    # 	g.say("Please enter a number to play followed by a star.")
    return render(request,'index.html')
    # return HttpResponse(str(resp), content_type='text/xml')

@csrf_exempt
def makeCall(request):
	phoneNumber = request.POST['telNo']
	delay = request.POST['delay']
	thread = Thread(target=newThread,args=(phoneNumber,delay, ))
	thread.start()

	return render(request,'index.html')

def newThread(phoneNumber,delay):
	time.sleep(int(delay))

	# [account_sid, auth_token, twilio_number] = open('config.txt','r').readlines()
	# account_sid = account_sid[0:len(account_sid) - 1]
	# auth_token = auth_token[0:len(auth_token)-1]
	# twilio_number = twilio_number[0:len(twilio_number)-1]

	# Make the call
	call = client.calls.create(
    to="+1" + str(phoneNumber),
    from_="+1" + str(originNumber),
    url=str(targetURL) + "/fizzy/handleCall") #target url for call to connect to


@require_POST
@csrf_exempt
@validate_twilio_request  #validates twilio function header
def handleCall(request):
	number = request.POST.get('Digits')
	resp = VoiceResponse()
	if number is not None:
		fizzString = ''
		for x in range(1, int(number) + 1):
			if x % 15 == 0:
				fizzString += 'Fizzbuzz, '
			elif x % 5 == 0:
				fizzString += 'Buzz, '
			elif x % 3 == 0:
				fizzString += 'Fizz, '
			else:
				fizzString += str(x) + ', '
		resp.say(fizzString)
		return HttpResponse(str(resp), content_type='text/xml')
	with resp.gather(input='dtmf',finishOnKey='*') as g:
		g.say("Please enter a number to play followed by a star.")
	return HttpResponse(str(resp), content_type='text/xml')

@require_POST
@csrf_exempt
@validate_twilio_request  	#allows the user to still call twilio number directly to play the game
def phase1(request):
    resp = VoiceResponse()
    number = request.POST.get('Digits')
    if number is not None:
    	fizzString = ''
    	for x in range(1, int(number) + 1):
    		if x % 15 == 0:
    			fizzString += 'Fizzbuzz, '
    		elif x % 5 == 0:
    			fizzString += 'Buzz, '
    		elif x % 3 == 0:
    			fizzString += 'Fizz, '
    		else:
    			fizzString += str(x) + ', '
    	resp.say(fizzString)
    	return HttpResponse(str(resp), content_type='text/xml')
    with resp.gather(input='dtmf',finishOnKey='*') as g:
    	g.say("Please enter a number to play followed by a star.")
    return HttpResponse(str(resp), content_type='text/xml')


