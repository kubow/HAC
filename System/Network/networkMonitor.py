import os
os.system('net view > conn.tmp')
f = open('conn.tmp', 'r')
f.readline();f.readline();f.readline()

conn = []
host = f.readline()
while host[0] == '\\':
    conn.append(host[2:host.find(' ')])
    host = f.readline()

print conn
f.close()   