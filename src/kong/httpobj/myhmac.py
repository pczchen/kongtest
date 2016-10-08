from kong.httpobj.myobject import Mybase

class Myhmac(Mybase):
  """
  hmac Object
  """

  def __init__(self,method,url,headers,body):
    Mybase.__init__(self,method,url,headers,body)
    self.algorithm="hmac-sha1"

  def setalgorithm(self,algorithm):
    self.algorithm = algorithm

  def getalgorithm(self):
    return self.algorithm

  def setsecret(self,secret):
    self.secret = secret
   
  def getsecret(self):
    return self.secret

  def setusername(self,username):
    self.username = username

  def getusername(self):
    return self.username

  def setsigheaders(self, sigheaders):
    self.sigheaders = sigheaders

  def getheaders(self):
    return self.sigheaders