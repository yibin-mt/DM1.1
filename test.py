import sys
sys.path.append('./DM/')
sys.path.append('./DM/models/')
from DmClass import *

text = 'hi穆莎'
history = {'conversation':['','']}

dm  = DmClass()
dm.load_data(text, history, '1', -1)

ans, history, emotion = dm.response()
print(ans)
print(history)