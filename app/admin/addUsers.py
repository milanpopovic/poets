import os, sys
import hashlib
sys.path.insert(0, '/home/ubuntu/workspace/app')
from model import Model

def md5(s):
  m = hashlib.md5()
  m.update(s.encode())
  return m.hexdigest()

model = Model('popovicmilan','c9')

for i in range(5):
  name = input('Full name: ')
  if name == "": break
  email = input('Email: ')
  password = input('Password: ')
  admin=int(input('Admin (0,1): '))
  model.newUser(name,email,md5(password),admin)

for user in model.get_all_users():
  print(user)

