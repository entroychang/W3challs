# Temporal attack

1. First, lets go through the website.
2. Then, we look up the [source code](http://temporal.hax.w3challs.com/php_portal_administration.php) below and we will know what to do : 
    ```
    // TODO : change the password below choosing a more complex one (! dictionnary word)
   // but it *must* contain only lowercase alphabetical characters
    ```
    As we can see, we have to fill up a 9 characters password with only 26 alphabet. 
3. So, how we know that the word is correct or not. Lets look the source code here : 
    ```
    usleep(150000);
    ```
    ```
    $time1 = microtime(true);
    ```
    ```
    $time2 = microtime(true);
    ```
    ```
    $res = ceil(($time2-$time1) * 1000);
    ```
    If we guess the right charactor, $res will become larger. 
4. I use python to help guessing the password.
5. Here is the flag : jkmnaziwx
