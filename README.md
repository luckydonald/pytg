# **PyTg** 
#### Version [0.4.8](https://github.com/luckydonald/pytg/blob/master/CHANGELOG.md#changelog) ####
[![get it from PyPI](https://img.shields.io/pypi/v/pytg.svg)](https://pypi.python.org/pypi/pytg) [![PyPI](https://img.shields.io/pypi/dm/pytg.svg)](https://pypi.python.org/pypi/pytg/0.4.6/) [![Join the chat at https://gitter.im/luckydonald/pytg](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/luckydonald/pytg?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A Python package that communicates with the [Telegram messenger CLI](https://github.com/vysheng/tg), to send and receive messages and more. *Since January 2014*

[Telegram](https://telegram.org) is an Whatsapp like Instant messenger, with clients for virtually every device you use.

Works with Python  2.7 and 3    

> I really recommend to use Python 3, because of it's build in unicode support.
Python 2 uses ascii only bytestrings, causing much, **much trouble** when dealing with characters like öäüß or emojis. (Trust me, I've been there)     
~ luckydonald

## **Install**##
### Dependencies ###
 - Install the Telegram CLI (from @vysheng), follow the [official Instructions](https://github.com/vysheng/tg)

### Pytg ###
##### Install form PyPI [![on PyPI](https://img.shields.io/pypi/v/pytg.svg)](https://pypi.python.org/pypi/pytg)

```shell
pip install pytg
```    
To upgrade append the ```--upgrade``` flag.
 
##### Install from source

(Beta versions are in the [development branch](https://github.com/luckydonald/pytg/tree/development))    

 - a) Get the latest pytg code from github.    
    ```git clone https://github.com/luckydonald/pytg.git && cd pytg```     
 - b) To update already existing code, navigate to the root inside the pytg folder, then ```git pull```
 - Install
    ```sudo python setup.py install```
    - The dependency "[DictObject](https://github.com/luckydonald/DictObject)" should be installed automatically by this. If not, it is available on PyPI:    
     ```sudo pip install DictObject```
    - Same goes for "[luckydonaldUtils](https://github.com/luckydonald/luckydonald-utils)":    
     ```sudo pip install luckydonald-utils```
    
 Done.

## **Usage** ##

>***Note***: The examples files produce syntax errors for python 3.0 - 3.2, the pytg package itself is not affacted by this!    
> To fix, just remove the ```u``` in front of the strings: change ```u"foobar"``` to ```"foobar``` (see [issue #39](https://github.com/luckydonald/pytg/issues/39#issuecomment-129992777) and [Python 3.3 accepts ```u'unicode'``` syntax again](https://docs.python.org/3/whatsnew/3.3.html?highlight=unicode)). 

#### *Start* telegram ####

Create a Telegram Instance.
This will manage the CLI process, and registers the Sender and Receiver for you.

```python
from pytg import Telegram
tg = Telegram(
	telegram="/path/to/tg/bin/telegram-cli",
	pubkey_file="/path/to/tg/tg-server.pub")
receiver = tg.receiver
sender = tg.sender
```

If you don't want pytg to start the cli for you, start it yourself with ```--json -P 4458``` (port 4458).
You can then use the Receiver and/or the Sender like this: 


```python
from pytg.sender import Sender
from pytg.receiver import Receiver
receiver = Receiver(host="localhost", port=4458)
sender = Sender(host="localhost", port=4458)
```

#### *Send* a message ####

```python
sender.send_msg("username", "Hello World!")
# Easy huh?
```
    
#### *Receiving* messages ####

You need a function as main loop.
```python
@coroutine # from pytg.utils import coroutine
def main_loop():
	while not QUIT:
		msg = (yield) # it waits until it got a message, stored now in msg.
		print("Message: ", msg.text)
		# do more stuff here!
	#
#
```

Last step is to register that function:

```python
# start the Receiver, so we can get messages!
receiver.start()

# let "main_loop" get new message events.
# You can supply arguments here, like main_loop(foo, bar).
receiver.message(main_loop())
# now it will call the main_loop function and yield the new messages.
```

That's the basics. Have a look into the examples folder. For starters, I recommend:    
* dump.py - is usefull to see, how the messages look like.    
* ping.py - is usefull to see how to interact with pytg, send messages etc.

## Documentation
The ```Sender``` object features a rich build-in help, inside the python interpreter type:
```python
from pytg.sender import Sender
help(Sender)  # list all commands
help(Sender.get_self)  # get help for a specific command
``` 

Or you can have a look into [DOCUMENTATION.md](https://github.com/luckydonald/pytg/blob/master/DOCUMENTATION.md)


## Contribute
###### You can help!

* by [reporting issues](https://github.com/luckydonald/pytg/issues)
* by commiting patches/[pull requests](https://github.com/luckydonald/pytg/pulls)
* with testing
 
*Note: There is a version in the making, supporting the cli via socket (as before), the CLI via its build in python (aka. tgl) and brand new, the [Telegram bot api](https://github.com/luckydonald/pytgbot) as well.
Receiving messages is already possible with all three (even simultaneously).
Also it features neat classes for everything. Currently I lack the time to continue that.  
See the develop branch for that. Maybe you can help make that happen.*

## URL Changes ##
If you started with pytg after 2015, you can ignore this. If you cloned from `luckydonald/pytg`, you can ignore this.
Here is how to update your local git clone to this url when your old one was set to [https://github.com/efaisal/pytg.git`](https://github.com/efaisal) (before I started maintaining it in September 2014)
```shell
# navigate into the clone
cd pytg	 # not pytg/pytg!
# change to the new url
git remote set-url origin https://github.com/luckydonald/pytg.git
# download the changes
git pull
# don't forget to install the newest official cli: https://github.com/vysheng/tg
```
If that failes at some point, just Install it from scratch.

### Look at the examples
See some example scripts to start with.
They are in the [examples folder](https://github.com/luckydonald/pytg/tree/master/examples)    
* dump.py * is usefull to see, how the messages look like.    
* ping.py * is usefull to see how to interact with pytg, send messages etc.    
* dialog_list.py * shows you how to interact with the CLI and function returning stuff.
* 


Thanks!
