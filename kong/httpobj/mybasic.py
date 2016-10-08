from kong.httpobj.myobject import Mybase
class Mybasic(Mybase):
  """
  Basic Object
  """

  def __init__(self,method,url,headers,body):
    Mybase.__init__(self,method,url,headers,body)

  def setusername(self,username):
    self.username = username

  def getusername(self):
    return self.username

  def setpassword(self,password):
    self.password = password
   
  def getpassword(self):
    return self.password