#!/usr/bin/env python
#-*- coding=UTF-8 -*-
import re
ppath="h:\\\\temp\\\\"

import os

regx = re.compile("S04E\d\d")
for file in os.listdir(ppath):   
    r = regx.search(file)
    if r:
       newfile = r.group(0) + ".mp4"
       os.rename(ppath+file,ppath+newfile)

     
    #newfile = file.split('.')[0]
    #newfile = newfile + ".mp4"
    #os.renames(ppath+file, ppath+newfile)

