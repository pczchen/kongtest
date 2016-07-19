#!/usr/bin/env python
# -*- coding=utf-8 -*-

import kong.util.myutil as myutil
import urllib.request

def prepare_request(httpreq):

  v = myutil.base64_encode(httpreq.username+":"+httpreq.password)[:-1]
  httpreq.headers["Authorization"] = "Basic "+ v.decode()

def send_request(httpreq,debug):
  prepare_request(httpreq)
  if httpreq.body:
    req = urllib.request.Request(httpreq.url,httpreq.body.encode(),httpreq.headers)
  else:
    req = urllib.request.Request(httpreq.url,httpreq.body,httpreq.headers)
  
  res = None
 
  try:
    req.get_method = lambda: httpreq.method
    res = urllib.request.urlopen(req)
  
  except urllib.request.HTTPError as e:
    print ("Failed:", httpreq.url)
    if debug:
      print (e.code ,":", e.read())

  else:
    print ("Success:", httpreq.url)
    if debug:
      print (res.read())