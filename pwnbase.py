import sys
import socket
import telnetlib 
import time
from struct import pack

def recvuntil(sock, txt):
  d = ""
  while d.find(txt) == -1:
    try:
      dnow = sock.recv(1)
      if len(dnow) == 0:
        print("-=(warning)=- recvuntil() failed at recv")
        print("Last received data:")
        print(d)
        return False
    except socket.error as msg:
      print("-=(warning)=- recvuntil() failed:", msg)
      print("Last received data:")
      print(d)     
      return False
    d += dnow
  return d

def recvall(sock, n):
  d = ""
  while len(d) != n:
    try:
      dnow = sock.recv(n - len(d))
      if len(dnow) == 0:
        print("-=(warning)=- recvuntil() failed at recv")
        print("Last received data:")
        print(d)        
        return False
    except socket.error as msg:
      print("-=(warning)=- recvuntil() failed:", msg)
      print("Last received data:")
      print(d)      
      return False
    d += dnow
  return d

# Proxy object for sockets.
class gsocket(object):
  def __init__(self, *p):
    self._sock = socket.socket(*p)

  def __getattr__(self, name):
    return getattr(self._sock, name)

  def recvall(self, n):
    return recvall(self._sock, n)

  def recvuntil(self, txt):
    return recvuntil(self._sock, txt)  

# Base for any of my ROPs.
def db(v):
  return pack("<B", v)

def dw(v):
  return pack("<H", v)

def dd(v):
  return pack("<I", v)

def dq(v):
  return pack("<Q", v)

def go():  
  global HOST
  global PORT
  s = gsocket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))
  
  # Put your code here
     
  s.sendall("start\n")

  while(s.recvuntil("Progress ")):
    q = s.recvuntil("\n")
    q = q[7:-1]
    print(q)
    if q.find("print"):
      q2 = q.split(";")
      q = q2[0]
    if q.find("x"):
      q = q.replace("x","*")
    print(eval(q))
    s.sendall(`eval(q)`+"\n")
  # Interactive sockets.
  t = telnetlib.Telnet()
  t.sock = s
  t.interact()

  # Python console.
  # Note: you might need to modify ReceiverClass if you want
  #       to parse incoming packets.
  #ReceiverClass(s).start()
  #dct = locals()
  #for k in globals().keys():
  #  if k not in dct:
  #    dct[k] = globals()[k]
  #code.InteractiveConsole(dct).interact()

  s.close()

HOST = '206.189.93.101'
PORT = 4343
go()
