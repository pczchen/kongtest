import gzip

f=open("data.txt","rb")

gz = gzip.GzipFile(fileobj=f) 

print(gz.read())