# **PyTG2** #
Python 3 (and 2.7)

A Python package that communicates with (a patched version of) the Telegram messenger CLI.
The [original version](https://github.com/vysheng/tg) does not support some required features.    


> I really recommend to use Python 3, because of it's build in unicode support.
Python 2 uses ascii only bytestrings, causing much trouble when dealing with characters like öäüß or emojis.
~ luckydonald

## **New in Version 0.3.0**
Pytg2 got overhauled to version 0.3.0, which will restructure heavily,
BUT will decrease the CPU usage to around nothing.
While the old versions need to parse the cli output directly, resuling in easy ways to exploit it, now it is safe, using json internal.
Without the parsing we don't have to poll for new output ("Hey, got anything yet? And yet? And yet? ...") but just block until we got new output.
The retrieval of new messaged is multitheaded, so you won't lose any messages if you do heavy and/or long operations between messages.

Also a nice new feature is an automatic download of files. (more about this, as soon as I get time to edit this...)
Please note, the array resulting in

## **Installation**
You have to install the patched telegram cli and pytg2.
This manual covers the installation of both. Lets begin with the python library: 

### 1. Install PyTG2 ###

THIS IS NOT UPDATED YET!!!
 THIS WILL NOT WORK!
  DON'T INSTALL YET
   thanks.



Install the future. (for Compatibility to both python 2.7 and 3)

    $ sudo pip install future

Clone PyTG 2 Repository

    $ git clone --recursive https://bitbucket.org/luckydonald/pytg2.git && cd pytg2 && sudo python setup.py install
 
      
### 2. Install Patched Telegram CLI
PyTG requires a [patched version](https://bitbucket.org/luckydonald/tg-for-pytg2) of Telegram messenger CLI to make message parsing feasible.
 If you already did install the patched cli, you are done. Horray!    
To install the patched Telegram messenger CLI ([luckydonald/tg-for-pytg2](https://bitbucket.org/luckydonald/tg-for-pytg2)):

Clone GitHub Repository

    $ git clone --recursive https://bitbucket.org/luckydonald/tg-for-pytg2.git && cd tg-for-pytg2
        
Then, run

    $ ./configure --disable-liblua

(You probably don't want Lua support.)

Next, run

    $ make

Telegram messenger CLI has its own dependencies. See [luckydonald/tg-for-pytg2](https://bitbucket.org/luckydonald/tg-for-pytg2) for details.

Once you build successfully, try to run

    $ ./bin/telegram-cli

Register your client, if required. Please note that PyTG2 does not support client registration yet.

### 3. Eat a cookie.
Thats actually optional.  
You're Done with the installation! [Yay.](http://flutteryay.com/)

### 4. Look at the examples
See some example scripts to start with.
They are in the [examples folder](https://bitbucket.org/luckydonald/pytg2/src)    
* dump.py* is usefull to see, how the messages look like.
* ping.py* is usefull to see how to interact with pytg, send messages etc.
* dialog_list.py* shows you how to interact with the CLI and function returning stuff.


### 5. Contribute
You can help

* by [reporting issues](https://bitbucket.org/luckydonald/pytg2/issues)
* by commiting patches
* with testing

Thanks!