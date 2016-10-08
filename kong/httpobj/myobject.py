class Mybase:
  """
    Mybase Object
  """

  def __init__(self,method,url,headers,body):
    self.method = method
    self.url = url
    self.headers = headers
    self.body = body

  def setmethod(self, method):
    if self.method != method:
       self.method = method

  def getmethod(self):
    return self.method

  def seturl(self,url):
    if self.url != url:
       self.url = url

  def geturl(self):
    return self.url

  def setheaders(self,headers):
    self.headers = headers

  def getheaders(self):
    return self.headers

  def setheader(self,h,v):
    self.headers[h] = v

  def getheader(self,h):
    return self.headers[h]

  def setbody(self,body):
    self.body = body

  def getbody(self):
    return self.body