# **PyTG2** #
#### Version 0.4.0 ####

A Python package that communicates with the [Telegram messenger CLI](https://github.com/vysheng/tg).

Works with Python  2.7 and 3    

> I really recommend to use Python 3, because of it's build in unicode support.
Python 2 uses ascii only bytestrings, causing much trouble when dealing with characters like öäüß or emojis.    
~ luckydonald

## **Install**##

 1. Install the Telegram CLI (from @vysheng), follow the [official Instructions](https://github.com/vysheng/tg)
 2. Get the latest code from github.    
    
    ```
    $ git clone https://github.com/luckydonald/pytg2.git && cd pytg2
    ```
    
 3. Install
    
    ```python
    $ sudo python setup.py install 
    ```
    
 Done.

## **Usage** ##

### How to *start* it up ###
```python

```
Create a Telegram Instance. 
This will manage the CLI process, and registers the Sender and Receiver for you.

```python
tg = pytg2.Telegram(
	telegram="/path/to/telejson/bin/telegram-cli",
	pubkey_file="/path/to/telejson/tg-server.pub")
receiver = tg.receiver
sender = tg.sender
```

If you don't want pytg2 to start the cli for you, start it yourself with ```--json -P 4458``` (port 4458).
You can then use the Receiver and/or the Sender like this: 


```python
from pytg2.sender import Sender
from pytg2.receiver import Receiver
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
@coroutine # from pytg2.utils import coroutine
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

	# add "example_function" function as message listener. You can supply arguments here, like main_loop(foo, bar).
	receiver.message(main_loop())  # now it will call the main_loop and yield the new messages.
	
```

That's the basics. Have a look into the examples folder. For starters, I recommend:    
* dump.py * is usefull to see, how the messages look like.    
* ping.py * is usefull to see how to interact with pytg, send messages etc.



## **New in Version 0.4.0**
No need for telejson any more, you can now run with the offical telegram-cli!
Connecting to the cli for sending will now surrender after given retrys, and not loop forever.
Also added a CHANGELOG file.


## New in Version 0.3.1
Updates for telejson beta compatibility.
This version never got offically released before the telejson fork got replaced by vysheng's native json implementation.
 
## **New in Version 0.3.0**
Pytg2 got overhauled to version 0.3.0, which will restructure heavily,
BUT will decrease the CPU usage to around nothing.
While the old versions need to parse the cli output directly, resuling in easy ways to exploit it, now it is safe, using json internal.
Without the parsing we don't have to poll for new output ("Hey, got anything yet? And yet? And yet? ...") but just block until we got new output.
The retrieval of new messaged is multitheaded, so you won't lose any messages if you do heavy and/or long operations between messages.

Also a nice new feature is an automatic download of files. (more about this, as soon as I get time to edit this...)



### Look at the examples
See some example scripts to start with.
They are in the [examples folder](https://github.com/luckydonald/pytg2/tree/master/examples)    
* dump.py * is usefull to see, how the messages look like.    
* ping.py * is usefull to see how to interact with pytg, send messages etc.    
* dialog_list.py * shows you how to interact with the CLI and function returning stuff.    


### Contribute
You can help

* with testing
* by [reporting issues](https://github.com/luckydonald/pytg2/issues)
* by commiting patches

Thanks!
