# **PyTG2** #
(Python 2.7 and 3)

A Python package that wraps around (a patched version of) the  [Telegram messenger CLI](https://github.com/vysheng/tg).
The original version does not support some required features.
I really recommend to use Python 3, because of it's build in unicode support.
Python 2 uses ascii only bytestrings, causing much trouble when dealing with characters like öäüß or emojis.


## **Installation**
You have to install the patched telegram cli and pytg2.
This manual covers the installation of both. Lets begin with the python library: 

### 1. Install PyTG2 ###
Now you are ready to install PyTG2   
 
Install the future. (for Compatibility to both python 2.7 and 3)

    $ sudo pip install future

Clone PyTG 2 Repository

    $ git clone https://bitbucket.org/luckydonald/pytg2.git && cd pytg2 && sudo python setup.py install
 
      
### 2. Install Patched Telegram CLI
PyTG requires a [patched version](https://bitbucket.org/luckydonald/tg-for-pytg2) of Telegram messenger CLI to make message parsing feasible.
 If you already did install the patched cli, you are done. Horray!    
To install the patched Telegram messenger CLI ([luckydonald/tg-for-pytg2](https://bitbucket.org/luckydonald/tg-for-pytg2)):

Clone GitHub Repository

    $ git clone https://bitbucket.org/luckydonald/tg-for-pytg2.git && cd tg-for-pytg2
        
Then, run

    $ ./configure

or

    $ ./configure --disable-liblua

if you don't want Lua support.

Next, run

    $ make

Telegram messenger CLI has its own dependencies. See [luckydonald/tg-for-pytg2](https://bitbucket.org/luckydonald/tg-for-pytg2) for details.

Once you build successfully, try to run

    $ ./bin/telegram-cli

Register your client, if required. Please note that PyTG2 does not support client registration yet.

### 3. Eat a cookie.
Thats optional.  
You're Done with the installation!

### 4. Look at the examples
See some example scripts to start with.
They are in the [examples folder](https://bitbucket.org/luckydonald/pytg2/src)