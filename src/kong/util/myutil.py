#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import sys
import time
import json
import hashlib
import base64
import hmac

debug = False

def log(name,message):
  print(name, ": ", message)

if os.getenv("DEBUG"): debug = True

if debug:
  log("DEBUG", "On")


def base64_encode(data):
  if type(data) == str:
    v = base64.encodestring(data.encode())
  else:
    v = base64.encodestring(data)
  if debug:
    log("base64_encode",v)
  return v

def base64_decode(data):
  v = base64.decodestring(data)
  if debug:
    log("base64_decode", v)
  return v

def md5(data):
  if data:
      v = hashlib.md5(data.encode())
  else:
      v = hashlib.md5("".encode())
  v =  v.digest()
  if debug:
    log("md5", v)
  return v

def hmac_signature(algorithm, secret, message):
  algs = {'md5'   : hashlib.md5,  
          'sha1'  : hashlib.sha1,
          'sha224': hashlib.sha224,
          'sha256': hashlib.sha256,
          'sha384': hashlib.sha384,
          'sha512': hashlib.sha512 }

  a = algorithm.split('-')[1]
  if a in algs:
     alg = algs[a]
  else:
     return None

  v = hmac.new(secret.encode(), message.encode(), alg)
  v = v.digest()
  v = base64_encode(v)[:-1]   # strip trailing \n
  if debug:
    log("hmac_signature", v)
  return v

def gmt_time(data):
  vf = '%a, %d %b %Y %H:%M:%S GMT'
  v = time.strftime(vf,data)
  if debug:
    log("gmt_time", v)
  return v          