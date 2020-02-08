# Authentication

1. First, lets go through the web.
2. Next, lets check out the http header and see what thing special.
    ```     
    authz=b14361404c078ffd549c03db443c3fede2f3e534d73f78f77301ed97d4a436a9fd9db05ee8b325c0ad36438b43fec8510c204fc1c1edb21d0941c00e9e2c1ce2
    ```
    It's obviously that we should decrypt the code. The main question now is what tool should we need.
3. Then, I just past the code in Google and find out the meaning is "user" in the [website](https://hashtoolkit.com/reverse-sha512-hash/b14361404c078ffd549c03db443c3fede2f3e534d73f78f77301ed97d4a436a9fd9db05ee8b325c0ad36438b43fec8510c204fc1c1edb21d0941c00e9e2c1ce2). Now, we just have to encode it by the same [method](https://emn178.github.io/online-tools/sha512.html). 
4. The next thing what keyword we need to encrypt and get the flag such as "admin", "root", "superuser" and so on. I try one by one and find that "admin" is the keyword. Here is the payload after encrypt it. 
    ```
    c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec
    ```
    Just change the cookie value and refresh it and get the flag. Remember to change the website to the admin page.
5. Here is the flag : W3C{iaobjej4g}
