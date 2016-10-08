import sys


def messy_decode(fn, encoding):
    f = open(fn, "r", encoding="latin-1")
    lines = f.readlines()
    count = len(lines)
    for i in range(count):
        lines[i] = lines[i].encode("latin-1")
    
    for i in range(count):
        lines[i] = lines[i].decode(encoding)
        
    print(lines)
    
messy_decode("test.txt", "utf-8")


