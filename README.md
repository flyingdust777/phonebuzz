# phonebuzz
A quick phonebuzz implementation using twilio and django

# To Play
just go to http://893f543c.ngrok.io/fizzy/ to receive a call
or
call (415) 649-3308 directly to play

# To Set Up Locally

1) Clone the repo
2) Make sure you have django and twilio installed. I have included my anaconda environement (environment.yml), so feel free to use that. Otherwise, you can easily install these libraries through pip. 
3) Edit global variables (account_sid, auth_token, originNumber, and targetURL) near the top of views.py in `phonebuzz/lendup_challenge/fizzbuzz/fizzy`
4) launch the local server using `python manage.py runserver` from `phonebuzz/lendup_challenge/fizzbuzz/`
5) host your local development environment on the web. I used ngrok for this. 
6) Play! (hopefully)
