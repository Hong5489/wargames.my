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
  #s = gsocket(socket.AF_INET, socket.SOCK_STREAM)
  #s.connect((HOST, PORT))
  
  # Put your code here
  def pad(message):
    if len(message) % 16 != 0:
        message = message + '0'*(16 - len(message)%16 )
    return message
  padding = 16
  i = 0
  flag = "picoCTF{"
  text = 'ode is: '
  charcter = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
  while(i != 8):
    for c in charcter:
      s = gsocket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((HOST,PORT))
      payload = (text+flag+c).rjust(11+padding,'a') + 'a'*(padding-8-i)
      s.sendall(payload+'\n')
      s.recvuntil("Please enter your situation report: ")
      output =  s.recvuntil("\n")[:-1]
      if output[128:160]==output[224:256]:
        flag += c
        text = text[1:]
        i += 1
        print flag
        s.close()
      message = """Agent,\nGreetings. My situation report is as follows:\n{0}\nMy agent identifying code is: {1}.\nDown with the Soviets,\n006\n""".format( payload, 'F'*38 )
      message = pad(message)
      for j in range(0,len(message)-padding-1,padding):
        print message[j:j+padding].replace('\n','N')
  # padding = 16
  # def pad(message):
  #   if len(message) % 16 != 0:
  #       message = message + '0'*(16 - len(message)%16 )
  #   return message
  # payload = "code is: picoCTF".rjust(11+padding,'a') + 'a'*(padding-6)
  # s.sendall(payload + "\n")
  # s.recvuntil("Please enter your situation report: ")
  # output = s.recvuntil('\n')[:-1]
  # for i in range(0,len(output)-(padding*2)-1,padding*2):
  #   print output[i:i+padding*2], i,i+padding*2

  
  # message = """Agent,\nGreetings. My situation report is as follows:\n{0}\nMy agent identifying code is: {1}.\nDown with the Soviets,\n006\n""".format( payload, 'F'*38 )
  # message = pad(message)
  # for i in range(0,len(message)-padding-1,padding):
  #   print message[i:i+padding].replace('\n','N')


  #Interactive sockets.
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

HOST = '2018shell1.picoctf.com'
PORT = 33893
go()
