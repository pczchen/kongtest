#!/usr/bin/env python
#-*- coding=utf-8 -*-

import os
import sys
import re

from kong.httpobj.mybasic import Mybasic
from kong.httpobj.mykey   import Mykey
from kong.httpobj.myhmac  import Myhmac
from kong.httpobj.myoauth2 import Myoauth2

import kong.httpreq.mybasic as basic_req
import kong.httpreq.mykey   as key_req
import kong.httpreq.myhmac  as hmac_req
import kong.httpreq.myoauth2 as oauth2_req


def parse_file(fn):
    processing = False
    processing_body = False
    processing_head = False
    k = ""
    headers={}
    obj=None
    f = open(fn,"r")
    for line in f.readlines():
      
      line = line.strip()
      
      if line.startswith("#"): continue

      if line.startswith("kind="):
         if processing:
            obj.setheaders(headers)
            yield k, obj
         processing = True
         processing_head = True
         headers = {}
         processing_body = False
  
         fields = line.split(" ")
         k,v = fields[0].split("=")
         
         k = v.lower()
         if k == "basic":
            obj  = Mybasic(None,None,None,None)
            obj.setusername(fields[1].split("=")[1])
            obj.setpassword(fields[2].split("=")[1])
         elif k == "key":
            obj  = Mykey(None,None,None,None)
            obj.setapikey(fields[1].split("=")[1])
            obj.setapisecret(fields[2].split("=")[1])
         elif k == "hmac":
            obj  = Myhmac(None,None,None,None)
            obj.setusername(fields[1].split("=")[1])
            obj.setalgorithm(fields[2].split("=")[1])
            obj.setsecret(fields[3].split("=")[1])
            obj.setsigheaders(fields[4].split("=")[1].replace(","," "))
         elif k == "oauth2":
            obj  = Myoauth2(None,None,None,None)
            obj.setclient_id(fields[1].split("=")[1])
            obj.setclient_secret(fields[2].split("=")[1])
            obj.setprovision_key(fields[3].split("=")[1])
            obj.setauthenticated_userid(fields[4].split("=")[1])
            obj.setscope(fields[5].split("=")[1].replace(","," "))            
            obj.setbaseurl(fields[6].split("=")[1])
         else:
            yield None,None
     
 
      elif line == "":
        if processing:
           processing_body = True              
 
      else:
        if processing_body:
           obj.setbody(line)
        elif processing_head:
           m,u = re.split("\s+",line)
           obj.setmethod(m.upper())
           obj.seturl(u)
           processing_head = False
        else:
           h,v = line.split(":")
           h = h.strip().lower()
           v = v.strip()
           headers[h]=v

    if processing:
       obj.setheaders(headers)
       yield k, obj
       

def test_connect(fn,debug):
    for kind, obj in parse_file(fn):

      if kind == "basic":
         basic_req.send_request(obj,debug)
      elif kind == "key":
         key_req.send_request(obj,debug)
      elif kind == "hmac":
         hmac_req.send_request(obj,debug)
      elif kind == "oauth2":
         oauth2_req.send_request(obj,debug)
      
def test_ping(debug):
    test_connect("mytemplate.seq",debug)

def main():
   debug = None
   if os.getenv("DEBUG"):
      debug = True

   if len(sys.argv) < 2:
      print("Usage: " + sys.argv[0] + "  file")
   else:
      test_connect(sys.argv[1],debug)

if __name__ == "__main__":
   main()   
               