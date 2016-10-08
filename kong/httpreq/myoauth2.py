#!/usr/bin/env python
# -*- coding=utf-8 -*-

import kong.util.myutil as myutil
import urllib.request
import json 
import httplib2, ssl

def process_authorize(httpreq, debug):
  url = httpreq.baseurl + httpreq.authorize_path
  method = 'POST'
  
  data = "client_id="+httpreq.client_id+"&" + \
         "response_type="+httpreq.response_type+"&" + \
         "provision_key="+httpreq.provision_key+"&" + \
         "authenticated_userid="+httpreq.authenticated_userid+"&" + \
         "scope="+httpreq.scope
  res = None
  ctx = ssl._create_unverified_context()
  req = urllib.request.Request(url,data.encode(), {})

  try:
    req.get_method = lambda: method
    res = urllib.request.urlopen(req, context=ctx)

  except urllib.request.HTTPError  as e:
    print ("Failed:", url)
    if debug:
      print (e.code ,":", e.read())
    return None
  else:
    msg = res.read()
    cj = json.loads(msg.decode())
    code = cj["redirect_uri"].split("?code=")[1]
    print ("Success:", url,code)
    if debug:
      print (msg)
    return code

def process_token(httpreq, debug, code):
  url = httpreq.baseurl + httpreq.token_path
  method = 'POST'

  data = "client_id="+httpreq.client_id+"&" + \
         "client_secret="+httpreq.client_secret+"&" + \
         "code="+code+"&" + \
         "grant_type="+httpreq.grant_type

  res = None
  ctx = ssl._create_unverified_context()
  req = urllib.request.Request(url,data.encode(), {})

  try:
    req.get_method = lambda: method
    res = urllib.request.urlopen(req, context=ctx)

  except urllib.request.HTTPError as e:
    print ("Failed:", url)
    if debug:
      print (e.code ,":", e.read())
    return None
  else:
    msg = res.read()
    cj = json.loads(msg.decode())
    print ("Success:" , url,cj["access_token"])
    if debug:
      print (msg)
    return cj["access_token"]


def send_request(httpreq,debug):
  code = process_authorize(httpreq, debug)
  if code == None:
     print ("Failed:" , httpreq.url)
     return 

  access_token = process_token(httpreq, debug, code)
  if access_token == None:
     print ("Failed:" , httpreq.url)
     return

  httpreq.headers["Authorization"] = "Bearer "+access_token
  if httpreq.body:
    req = urllib.request.Request(httpreq.url,httpreq.body.encode(),httpreq.headers)
  else:
    req = urllib.request.Request(httpreq.url,httpreq.body,httpreq.headers)

  res = None
  
  try:
    #req.get_method = lambda: httpreq.method
    #res = urllib.request.urlopen(req)
    http = httplib2.Http(".cache", ca_certs = None, disable_ssl_certificate_validation = True)
    res, content = http.request(httpreq.url, httpreq.method, body=httpreq.body, headers=httpreq.headers)


  #except urllib2.HTTPError, e:
  except httplib2.HttpLib2Error as e:
    print ("Failed:", httpreq.url)
    print (e.code ,":", e.read())

  else:
    print ("Success:", httpreq.url)
    #if debug:
      #print res.read()
    print (res,"\n",content)             