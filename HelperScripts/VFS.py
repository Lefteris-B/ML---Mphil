#the spiffs file system is automatically mounted to the /flash directory when booting. 
#The user only needs to pass in the "/flash" directory name as a parameter when using
# the os interface to access the file system .

import uos

print("files:", uos.listdir("/flash"))

with open("/flash/test.txt", "w") as f:
    f.write("hello text")

print("files:", uos.listdir("/flash"))

with open("/flash/test.txt", "r") as f:
    content = f.read()

print("read:", content)
