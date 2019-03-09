import os, sys
import hashlib
sys.path.insert(0, '/home/ubuntu/workspace/app')
from model import Model


def md5(s):
  m = hashlib.md5()
  m.update(s.encode())
  return m.hexdigest()


model = Model('popovicmilan','c9')
email = input('Email: ')
password = input('New password: ')
print(model.change_password(email,md5(password)))


