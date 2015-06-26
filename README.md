# **PyTg** #
#### Version 0.4.1 ####

A Python package that communicates with the [Telegram messenger CLI](https://github.com/vysheng/tg).    
(**Note:** This will soon updated to wrap around the cli's python interface, too, to have the same commands independent of how you connect with the cli.)
(Beta versions are in the [development branch](https://github.com/luckydonald/pytg/tree/development))

Works with Python  2.7 and 3    

> I really recommend to use Python 3, because of it's build in unicode support.
Python 2 uses ascii only bytestrings, causing much, much trouble when dealing with characters like öäüß or emojis. (Trust me, I've been there)     
~ luckydonald

## **Install**##
### Dependencies ###
 - Install the Telegram CLI (from @vysheng), follow the [official Instructions](https://github.com/vysheng/tg)
 - you need to either install with json or python. If you have both, that's even better.
 
### Pytg ###
 - a) Get the latest pytg code from github.
    ```shell
    git clone https://github.com/luckydonald/pytg.git && cd pytg
    ```
     
 - b) To update already existing code, navigate to the root inside the pytg folder, then ```git pull```
 - Install
    ```shell
    sudo python setup.py install 
    ```
    - The dependency "DictObject" should be installed automatically by this. If not, it is available on PyPI    
     ```sudo pip install DictObject```
    
 Done.

## **Usage** ##

### *Start* telegram ###

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

### *Send* a message ###

```python
sender.send_msg("username", "Hello World!")
# Easy huh?
```
    
### *Receiving* messages ###

You need a function as main loop.
```python
def main_loop():
	while not QUIT:
		msg = (yield) # it waits until it got a message, stored now in msg.
		if
		print("Message: ", msg.text)
		# do more stuff here!
	#
#
```

Last step is to register that function:

```python
receiver = pytg.interfaces.automatic.receiver.Receiver(port=4458)

# start the Receiver, so we can get messages!
receiver.start()

# let "main_loop" get new message events.
# You can supply arguments here, like main_loop(foo, bar).
receiver.register_event_loop(main_loop())
# now it will call the main_loop function and yield the new messages.
```

That's the basics. Have a look into the examples folder. For starters, I recommend:    
* dump.py * is usefull to see, how the messages look like.    
* ping.py * is usefull to see how to interact with pytg, send messages etc.


### Look at the examples
See some example scripts to start with.
They are in the [examples folder](https://github.com/luckydonald/pytg/tree/master/examples)    
* dump.py * is usefull to see, how the messages look like.    
* ping.py * is usefull to see how to interact with pytg, send messages etc.    
* dialog_list.py * shows you how to interact with the CLI and function returning stuff.    


### Contribute
You can help

* with testing
* by [reporting issues](https://github.com/luckydonald/pytg/issues)
* by commiting patches

Thanks!

## **URL Changes** or "How to update?"##
When you original used E A Faisal's version, you have to update your code.
A huge change for the original users: merges, new functions,
renames and and finally the changed url. Here is how to update your local git clone. If you have not used pytg before, just skip to the Install part.
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

