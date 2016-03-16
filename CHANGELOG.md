#Changelog

## Version 0.4.10: (Not released yet) ##
- Added optional caption argument to `send_document("user", "filepath" [, "caption"])`
- Improved automated docstrings on functions `help(...)` a bit.
- Added automatic generation of documentation. `pytg.sender.create_automatic_documentation(filename="DOCUMENTATION.md")` creates a markdown formatted file. This uses roughly the same generation process as the automatic docstrings.
- Also added some missing documentation for some errors. [#69](https://github.com/luckydonald/pytg/issues/69)
- The old documentation can be found at `DOCUMENTATION_manual.md`
- Added a example to demonstrate how to build converations with the use of generators and the `yield` statement.

## Version 0.4.9: ##
- Fixes `AssertionError` with secret chats. [#74](https://github.com/luckydonald/pytg/issues/74)

## Version 0.4.8: ##
- Renamed the argumen type `File` to `FilePath` to be more clear about it beeing a string. (Relates to [#67](https://github.com/luckydonald/pytg/issues/67))
- Now the new `FailException` (subclasses `IllegalResponseException`) will be raised if the CLI reports a error.
- Fixed `Username` Argument becoming `None`
- `ResultParser` classes (not instances) will be instanciated automatically.

## Version 0.4.7: ##
- Fixed `Sender.message_get` not accepting the new permanent id's. [#66](https://github.com/luckydonald/pytg/issues/66)
- Added Example `source_of_reply.py` involving `Sender.message_get` to find the first message of a stack of replies.

## Version 0.4.6: ##
- Added `Sender.channel_rename`, and supergroup fixes from [PR #61](https://github.com/luckydonald/pytg/pull/61). Thanks [@huiyiqun](https://github.com/huiyiqun)
- Added `Sender.reply`, the previous `Sender.reply_text` became an alias of that. (ea43060c3f53a3f947fd73cd624c85a412804408)
- Added `Sender.resolve_username` [#63](https://github.com/luckydonald/pytg/issues/63) (34ffb3fd15e8e322873c679b74293c3c184284d3)
- Started using [PEP 8 formatting](https://www.python.org/dev/peps/pep-0008/) which addresses [#59](https://github.com/luckydonald/pytg/pull/59)
- Started using [PEP 396](https://www.python.org/dev/peps/pep-0396/) to include `__version__`

## Version 0.4.5: ##
- Fixed ```Sender.contacts_search()```. [#51](https://github.com/luckydonald/pytg/issues/51)

## Version 0.4.4: ##
- Fixed ```No handlers could be found for logger "pytg.sender"``` with Python 2. [#33](https://github.com/luckydonald/pytg/issues/33)

## Version 0.4.3: ##
- Fixed ```pip install``` dependencies bug. [#55](https://github.com/luckydonald/pytg/issues/55)

## Version 0.4.2: ##
- Added ```result_timeout``` kwarg for all ```Sender``` functions. [#49](https://github.com/luckydonald/pytg/pull/49),[#48](https://github.com/luckydonald/pytg/pull/48). Thanks [@the-glu](https://github.com/the-glu)
- Added first channel support [#47](https://github.com/luckydonald/pytg/pull/47). Thanks [@spoetnik](https://github.com/spoetnik)
- Added to [PyPI](https://pypi.python.org/pypi/pytg).
- Will not make such strange version numbers again.

## Version 0.4.1e: ##
- Fixed result parsing of ```Sender.contact_add(...)``` [#35](https://github.com/luckydonald/pytg/pull/53). Thanks [@spikeekips](https://github.com/spikeekips)
- Added ```Sender.get_self()``` to  [#35](https://github.com/luckydonald/pytg/pull/53). Thanks [@spikeekips](https://github.com/spikeekips)

## Version 0.4.1d: ##
- Bug Fix: Unicode error on Python 3.0 - 3.2 [issue #39](https://github.com/luckydonald/pytg/issues/39), also exported the encoding functions to a sepreate package called ```luckydonaldUtils``` (```pip install luckydonald-utils```).
- Bug Fix: Result_parser method for the chat_add_user command. Thanks @juanprq 
- Bug Fix: Exception on calling sender.contacts_list(). Thanks @vonabarak 

## Version 0.4.1c: ##
- Bug Fix: encoding.to_binary and to_unicode now transform other datatypes (like int) into that type as well.  Fixes [issue #32](https://github.com/luckydonald/pytg/issues/32), and that closes [issue 31](https://github.com/luckydonald/pytg/issues/31)

## Version 0.4.1b: ##
- added ```Receiver.queued_messages()```, showing how many messages are waiting in the queue.

## Version 0.4.1a: ##
- fixed ```Sender``` not working with python 2. ([issue #26](https://github.com/luckydonald/pytg/issues/26), thanks @Meisolsson.)

## Version 0.4.1``` ```:  

**Big rename**:     
`pytg2` -> `pytg`    
Thats it.

## Version 0.4.1: ##
It is named ```"pytg"``` again. Hooray!
[@luckydonald](https://github.com/luckydonald) took over maintainence.

- For documentation, you can just use python's `help()` function:
    ```python
    help(pytg.sender.Sender)
    ```
- added reply and preview capabilities.    
- added commands.    


## Version 0.4.0: ##
official cli support.
CLI fork not updated? That is a problem of the past!

No need for telejson any more, you can now run with the offical telegram-cli!
Connecting to the cli for sending will now surrender after given retrys, and not loop forever.
Also added a CHANGELOG file.

> It was fun to develop that json bridge by myself though, and It hurts a bit too left that behind... :cry:
> But: I learned a lot about C and git on that journy, and I can let my experience with json flow back into the original cli.
> Everybody will profit from this.

- ```pytg.Telegram```, ```pytg.sender.Sender```, ```pytg.receiver.Receiver``` 
	- sending and receiving now uses the same port.   
		- changed tg.Telegram() parameters: ```port_receive```, ```port_send``` are unified to ```port```:
			```python
			tg.Telegram(port=4458)  # sending and receiving now uses the same port.
			```
	- Sender and Receiver both alter the resulting message dict (versus the json output):
		- ```from``` -> ```sender``` (Reserved word in python)
		- ```to``` -> ```receiver```
		- ```out``` -> ```own``` (out is not intuitive as not mandatory this cli has send the message but the account did.)
		- ```peer``` [added] This is where you most likly want to reply to.
			It will be the group where the message got send, or the user if it is a private message.
		- ~~```print_name```~~ **removed** use "cmd" and "name" instead.
		- + ```cmd``` the unique identifier string which will not change. (exception: secret chats might be replaced by a new one)
		- + ```name``` is a display name. Either the first name or, if not set, the username.
		

- ```pytg.sender.Sender```
	- **all commands** can now raise an exception if the connection (i.e. the connecting) to the cli failed after given number of retries. You should try to restart the cli.
	- **all commands** now have a ```retry_connect=<value>``` parameter (as ```**kwargs```).
		```retry_connect=2``` means 3 tries, first try + 2 retries. This is the *default setting*.
		```retry_connect=0```, ```retry_connect=False``` and ```retry_connect=None``` will not retry,
		```retry_connect=True``` or ```retry_connect= -1``` means to retry infinite times. (this was the default before.)
		```python
		sender.send_msg("luckydonald", "test message", retry_connect= 10
		```
	
	- ```send_photo()```: added optional attribute ```caption``` (string, max length: 140).    
	
	- ```send_video()```: added optional```caption``` parameter (max length: 140).    
		Example:    
		```python
		#send_photo <peer> <file> [caption]
		sender.send_photo(peer, file)
		sender.send_photo(peer, file, caption)
		sender.send_photo("user#1234", "/path/to/image.png")
		sender.send_photo("user#1234", "/path/to/image.png", "This is a image")
		```

## Version 0.3.1:
Updates for telejson beta compatibility.
This version never got offically released before the telejson fork got replaced by vysheng's native json implementation.
In the end that was way better.
 
## **Version 0.3.0:**
*Pytg2* (since `v0.4.1` called *pytg* again) got overhauled to version `0.3.0`, which restructures heavily,
BUT will decrease the CPU usage to around nothing.
While the old versions need to parse the cli output directly, resuling in easy ways to exploit it, now it is safe, using json internal.
You need the modified telejson-cli for that to work. 
Without the parsing we don't have to poll for new output ("Hey, got anything yet? And yet? And yet? ...") but just block until we got new output.
The retrieval of new messaged is multitheaded, so you won't lose any messages if you do heavy and/or long operations between messages.

Also a nice new feature is an automatic download of files. (more about this, as soon as I get time to edit this...)

## Version 0.2.2:
updated commands to reflect CLI changes, moved exceptions, better error output

In Detail:

- added the new commands to pytg:
    - `send_typing(peer)`
    - `set_profile_name(first_name, last_name=None)`
    - `set_username(username)`
    - `set_profile_photo(path)`
    - `create_group_chat(chat_topic, user1, user2, user3, ... )`
    - `chat_set_name(chat, new_name)  as mirror to rename_chat(chat, new_name)`
    - `rename_chat(chat, new_name)`
    - `search(pattern, peer=None, limit=None, from_unixtime=None, to_unixtime=None, offset=None)`
- Moved exceptions into errors.py file to have them all in one place.
- If a message type of telegram is not supported, it will now tell you with an message.

(since commit `bb2a631`)

## Version 0.2.1:
- Renamed indexes of the messages arrays!
    - `uid` > `userid`
    - `gid` > `groupid`
    - `cmduser` > `usercmd`
    - `cmdgroup` > `groupcmd`
- improved print_message_data (for messages) regex.
- and did some code cleanup.

Did I mention:

- Fuck Yeah, got the f`**`k encoding working!!!
- fixed `'\'` crashing bot.
- fixed encoding like `'äöü'.

(Changelog restored from commit [`888ebf`](https://github.com/luckydonald/pytg/commit/888ebf85cc0bbe216aa729569de6b0eb881294ee))


## Version 0.2:
[@luckydonald](https://github.com/luckydonald) started working on a fork.
(first commit [`ea331e`](https://github.com/luckydonald/pytg/commit/ea331eb71cdf1bad481893d8516768217446e07e), called version 0.2 since [`722361`](https://github.com/luckydonald/pytg/commit/722361307a547a312e7bd4b9daa46a7c104d3c60))

## Version 0.1
Somewhere around commit [072c5f](https://github.com/luckydonald/pytg/commit/072c5f67c4164948ae255cac704709432511b667)

## Version 0 - The beginning
Back in January 2014, [@efaisal](https://github.com/efaisal) started working on pytg. 
The Telgram-CLI was brand new, and there was no way to interact with it programatically like you could much later with lua or json. Until [then](https://github.com/luckydonald/pytg/commit/8c62dc4a35ef4ff2b81f4c0801f5448374fccaa1) there was not a single bot in telegam. 
There was no talking. There was no smiling. *-sigh-* There were only rocks. [quote reference](http://mlp.wikia.com/wiki/Transcripts/The_Cutie_Mark_Chronicles)
