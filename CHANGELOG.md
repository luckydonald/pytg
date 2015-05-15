
#TODO: update this.

## official cli support ##
Unupdated CLI? That is a thing of the past!
> It was fun to develop that json bridge by myself though, and It hurts a bit too left that behind :cry:.
> But: I learned a lot about C and git on that journy, and are letting my experience with json flow back into the original cli.
> Everybody will profit from this.


##### *```pytg.*```,```examples/```* #####
- sending and receiving now uses the same port.   
	- changed tg.Telegram() parameters:
	```port_receive```, ```port_send``` are unified to ```port```:
	
	```python
	tg.Telegram(port=4458)  # sending and receiving now uses the same port.
	```
- sender and receiver both alter the resulting message dict:
	- Renaming "from", "to" and "out" because reserved word in python/not intuitive.
		- ```from``` -> ```sender``` (Reserved word in python)
		- ```to``` -> ```receiver```
		- ```out``` -> ```own``` (out is not intuitive as not mandatory this cli has send the message but the account did.)
	- Added "peer" attribute:
		- ```peer``` is where you mostly want to reply to. It will be the group where the message got send, or the user if it is a private message.
	- Deleting "print_name" in peers, adding "cmd" and "name" instead.
		- ```cmd``` is the unique identifier string which will not change. (exception: secret chats might change)
		- ```name``` is a display name. Either the first name or, if not set, the username.
	

##### *```pytg.sender.Sender```* #####
- all commands now raises an exception if the connection (i.e. the connecting) to the cli failed after given number of retries.
- all commands now have a ```retry_connect=<value>``` parameter (as ```**kwargs```).
	```retry_connect=2``` means 3 tries, first try + 2 retries. This is the *default setting*.
	```retry_connect=0```, ```retry_connect=False``` and ```retry_connect=None``` will not retry,
	```retry_connect=True``` or ```retry_connect= -1``` means to retry infinite times. (this was the default before.)

- ```send_photo()```: added optional attribute ```caption``` (unicode_string) (max length: 140) to ```send_photo```.
```
#send_photo <peer> <file> [caption]
sender.send_photo(peer, file)
sender.send_photo(peer, file, caption)
sender.send_photo("user#1234", "/path/to/image.png")
sender.send_photo("user#1234", "/path/to/image.png", "This is a image")
```
- ```send_video()```same goes with ```send_video```: added ```caption``` unicode_string (max length: 140),
	else it will fail.