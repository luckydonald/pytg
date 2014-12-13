# **PyTG2** #
(Python 2.7 and 3)

A Python package that wraps around (a patched version of) the Telegram messenger CLI .
The [original version](https://github.com/vysheng/tg) does not support some required features.    


> I really recommend to use Python 3, because of it's build in unicode support.
Python 2 uses ascii only bytestrings, causing much trouble when dealing with characters like öäüß or emojis.    
~ luckydonald

## **New in Version 0.2.2**

### The message array object ###
When using the tg.message() pipeline and storing the message like ```msg = (yield)```

    msg.peer: Peer.GROUP or Peer.USER
    msg.user: Peer object containing the user
    msg.group: Peer object containing the group chat or None, if not GROUP message.
    msg.reply: Peer object containing the group chat or the user chat object if not GROUP message.


### The Peer object ###
When using one of the peer objects of the message array object.    
This can be one on three: ```msg.reply```, ```msg.user```, ```msg.group```    
Please note, ```group``` can be ```None```.    
We will assume ```user = msg.user``` for the example:

    user.type = Peer.GROUP or Peer.USER
    user.cmd = "chat#123" or "user#456" (peer identifier + hashtag + id)   Safe way to address a message
    user.name = "Random Chat #1" or "I am a User."
    user.id = 123 (a number)
    user.namecmd = "Random_Chat_@1" or "I_am_a_User."    (username with '_' for spaces and '@' instead of '#')
                                                   This is the deprecated way of addressing user/groups
   
   

### tl;dr ###

    To anwer to an message in the same chat as the received message, use the data of msg.reply .     
    To get the sender peer string   use .cmd on an Peer object.  E.g. msg.reply.cmd    
    To identify a user              use msg.user.id    
    To get the user/chatroom name   use msg.user.name or msg.group.name    

------------------------------------

## **Installation**
You have to install the patched telegram cli and pytg2.
This manual covers the installation of both. Lets begin with the python library: 

### 1. Install PyTG2 ###
 
Install the future. (for Compatibility to both python 2.7 and 3)

    $ sudo pip install future

Clone PyTG 2 Repository

    $ git clone https://bitbucket.org/luckydonald/pytg2.git && cd pytg2 && sudo python setup.py install
 
      
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
You're Done with the installation!

### 4. Look at the examples
See some example scripts to start with.
They are in the [examples folder](https://bitbucket.org/luckydonald/pytg2/src)    
* pingbot.py* is usefull to see how to interact with pytg, send messages etc.     
* dump.py is* usefull to see, how the messages look like.  
   
### 5. Contribute
You can help

* by [reporting issues](https://bitbucket.org/luckydonald/pytg2/issues)
* by commiting patches
* with testing

Thanks!