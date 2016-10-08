from kong.httpobj.myobject import Mybase

class Myoauth2(Mybase):
  """
  oauth2 Object
  """

  def __init__(self,method,url,headers,body):
    Mybase.__init__(self,method,url,headers,body)
    self.response_type = "code"
    self.grant_type = "authorization_code"

    self.baseurl = url
    self.authorize_path = "/oauth2/authorize"
    self.token_path = "/oauth2/token"

  def setclient_id(self,client_id):
    self.client_id = client_id

  def getclient_id(self):
    return self.client_id

  def setclient_secret(self,client_secret):
    self.client_secret = client_secret
   
  def getclient_secret(self):
    return self.client_secret

  def setscope(self,scope):
    self.scope = scope

  def getscope(self):
    return self.scope

  def setprovision_key(self, provision_key):
    self.provision_key = provision_key

  def getprovision_key(self):
    return self.provision_key

  def setauthenticated_userid(self, userid):
    self.authenticated_userid = userid

  def getauthenticated_userid(self):
    return self.authenticated_userid

  def getbaseurl(self):
    return self.baseurl

  def setbaseurl(self,baseurl):
    self.baseurl = baseurl