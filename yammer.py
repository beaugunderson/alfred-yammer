#!/usr/bin/env python
# -*- coding: utf-8 -*-

import oauth2 as oauth
import sys
import urllib
import urlparse

# You'll need to enter these after creating an application on Yammer
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

TOKEN_STORE = "yammer.token"

REQUEST_TOKEN_URL = 'https://www.yammer.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://www.yammer.com/oauth/access_token'

AUTH_URL = 'https://www.yammer.com/oauth/authorize'

auth_key = ''
auth_secret = ''

try:
    f = open(TOKEN_STORE)

    lines = f.readlines()

    f.close()

    auth_key = lines[0].rstrip('\n')
    auth_secret = lines[1].rstrip('\n')

    print "access token: key '%s', secret '%s'" % (auth_key, auth_secret)
except IOError:
    print 'Had problems reading file: ' + TOKEN_STORE

if (auth_key == ''):
    consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    client = oauth.Client(consumer)

    resp, content = client.request(REQUEST_TOKEN_URL, "GET")

    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])

    request_token = dict(urlparse.parse_qsl(content))

    print "Request Token:"
    print
    print "oauth_token = %s" % request_token['oauth_token']
    print "oauth_token_secret = %s" % request_token['oauth_token_secret']
    print
    print "Go to the following link in your browser:"
    print "%s?oauth_token=%s" % (AUTH_URL, request_token['oauth_token'])

    oauth_verifier = raw_input('What is the PIN? ')

    token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])

    token.set_verifier(oauth_verifier)

    client = oauth.Client(consumer, token)

    resp, content = client.request(ACCESS_TOKEN_URL, "POST")

    access_token = dict(urlparse.parse_qsl(content))

    print "access token = %s" % access_token['oauth_token']
    print "access secret = %s" % access_token['oauth_token_secret']

    token = access_token['oauth_token'] + "\n" + access_token['oauth_token_secret'] + "\n"

    auth_key = access_token['oauth_token']
    auth_secret = access_token['oauth_token_secret']

    f = open(TOKEN_STORE, 'w')

    f.writelines(token)

    f.close()

token = oauth.Token(key=auth_key, secret=auth_secret)
consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)

client = oauth.Client(consumer, token)

GROUP_ID = "company"

url = 'https://www.yammer.com/api/v1/messages'

body = ' '.join(sys.argv[1:])

if not body:
    print "No body, exiting"

    sys.exit()

print "Sending '%s'" % body

parameters = urllib.urlencode({ "body": body })

resp, content = client.request(url, 'POST', parameters)

print "Status: " + resp['status']
