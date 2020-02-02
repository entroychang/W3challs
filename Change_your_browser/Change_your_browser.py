from requests import *

url = 'http://change-browser.hax.w3challs.com/'
headers = {
    'User-Agent' : 'W3Challs_browser'
}
r = get(url , headers=headers)
pos = r.text.find('W3C{')
while(True):
    print(r.text[pos] , end='')
    if (r.text[pos] == '}'):
        print()
        break
    pos += 1