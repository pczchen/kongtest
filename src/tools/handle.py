import os, re

path = r"H:\www.elastic.co\guide\en\elasticsearch\reference\current"

r1 = re.compile("<script.+?>.+?</script>", re.M|re.S)
r2 = re.compile("<script.+?></script>",re.M|re.S)
r3 = re.compile("<link.+?>",re.M|re.S)
r4 = re.compile("<style.+?>.+?</style>",re.M|re.S)

i=0
for file in os.listdir(path):
    fn = path + "\\" + file
    if os.path.isdir(fn): continue
    i += 1
    print("processing file:"+str(i)+"\t"+ file)
    
    f = open(fn,"r", encoding="UTF-8")
    content = f.read()
    f.close()
    
    content=r4.sub("",content)
    
    f = open(fn,"w",encoding="UTF-8")
    f.write(content)
    f.close()
    
    
    
    