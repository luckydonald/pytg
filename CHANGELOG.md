
#TODO: update this.

## official cli support ##
Unupdated CLI? That is a thing of the past!
> It was fun to develop that json bridge by myself though, and It hurts a bit too left that behind :cry:.
> But: I learned a lot about C and git on that journy, and are letting my experience with json flow back into the original cli.
> Everybody will profit from this.

```pytg.*```, ```examples/```
- sending and receiving now uses the same port.   
	- changed tg.Telegram() parameters:
	```port_receive```, ```port_send``` are unified to ```port```:
	
	```python
	tg.Telegram(port=4458)  # sending and receiving now uses the same port.
	```

pytg.sender.Sender:

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