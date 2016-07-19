#!/usr/bin/env python
# -*- coding=utf-8 -*-

import kong.util.myutil as myutil
import urllib.request
import time

def process_date(httpreq, debug, signature_string):
  if "date" in httpreq.headers:
    v = httpreq.headers["date"]
  else:
    v = myutil.gmt_time(time.gmtime())
    httpreq.headers["date"] = v
    
  if signature_string == None:
    signature_string = "date: " + v
  else:
    signature_string = signature_string + "\ndate: " + v

  return signature_string

def process_contentmd5(httpreq, debug, signature_string):
  if "content-md5" in httpreq.headers:
    v = httpreq.headers["content-md5"]
  else:
    cmd5 = myutil.md5(httpreq.body)
    v = myutil.base64_encode(cmd5)[:-1]
    httpreq.headers["content-md5"] = v

  if signature_string == None:
    signature_string = "content-md5: " + v
  else:
    signature_string = signature_string + "\ncontent-md5: " + v.decode()

  return signature_string


def prepare_request(httpreq,debug):
  signature_string = None

  for h in httpreq.sigheaders.split(" "):
    h = h.lower()
    if h == "date":
      signature_string = process_date(httpreq,debug,signature_string) 
    elif h == "content-md5":
      signature_string = process_contentmd5(httpreq, debug, signature_string)
    else:
      if signature_string == None:
        signature_string = h + ": " + httpreq.headers[h]
      else:
        signature_string = signature_string + "\n" + h + ": " + httpreq.headers[h]

  v = myutil.hmac_signature(httpreq.algorithm, httpreq.secret, signature_string)
  httpreq.headers["authorization"] = 'hmac accesskey="'+ httpreq.username + '", ' + \
                                     'algorithm="' + httpreq.algorithm + '", ' + \
                                     'headers="' + httpreq.sigheaders + '", ' + \
                                     'signature="' + v.decode() + '"' 


def send_request(httpreq,debug):
  prepare_request(httpreq,debug)

  if debug: myutil.log("headers",httpreq.headers)
   
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
      v = res.read()
      hs = res.info()
      if "Content-Encoding" in hs:
          import gzip
          from  io import BytesIO, StringIO
          datas = StringIO(v.decode("latin-1"))
          datab = BytesIO(v)
          gz = gzip.GzipFile(mode="rb", fileobj=datab)
          v = gz.read()

      print (v)   
      print (v.decode("utf-8"))     