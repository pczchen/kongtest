from kong.httpobj.myobject import Mybase

class Mykey(Mybase):
  """
  key Object
  """

  def __init__(self,method,url,headers,body):
    Mybase.__init__(self,method,url,headers,body)
    self.apikey = "apikey"

  def setapikey(self,apikey):
    self.apikey = apikey

  def getapikey(self):
    return self.apikey

  def setapisecret(self,secret):
    self.apisecret = secret
   
  def getapisecret(self):
    return self.apisecret