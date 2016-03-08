| **Content** |   |
| --- | --- |
| [Sender](#sender) | ```pytg.sender.Sender``` |
| [Exceptions](#exceptions) | ```pytg.exceptions.*``` |

## Sender
| Command group subsection |
| --- |
| *[Getting a Sender instance](#getting-a-sender-instance)* |
| *[```default_answer_timeout```](#default_answer_timeout)* |
| [sending](#sending-messages) | 
| [messages](#message-related) | 
| [peer](#peer-related) | 
| [user](#user-related) | 
| [contacts](#contact-related) | 
| [group chats](#group-chat-related) | 
| [secret chats](#secret-chat-related) | 
| [own profile](#own-profile-related) | 
| [system](#system-related) | 
| [diversa](#diversa) |

### Getting a Sender instance
###### The following tables assumes that ```sender``` is a instance of ```pytg.sender.Sender()```
```python
from pytg.sender import Sender
sender = Sender("localhost", 4458)  # or other address/port.
```
### ```default_answer_timeout```

If the timeout in the command table below is set to ```None```,
the command waits the default timeout specified in ```Sender.default_answer_timeout```, which is ```1.0``` seconds per default. 
You can change it in your sender instance:

```python
sender = Sender( ... )
sender.default_answer_timeout = 2  # in seconds
```

You may change the timeout of any command with supplying ```result_timeout=<seconds>``` in the call.
Also you can surround it with a try block, excepting a [```NoResponse```](#noresponse) if you like to ignore timeouts.


### sending messages
| Telgram command<br>(\* means optional) | Expected return parser | Timout<br>(seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| ```sender.msg(```peer```,``` text```)``` | success_fail | 60.0 | Sends text message to peer |
| ```sender.send_msg(```peer```,``` text```)``` | success_fail | 60.0 | Sends text message to peer (alias to msg)|
| ```sender.send_text(```peer```,``` text```)``` | success_fail | 60.0 | Sends text message to peer (alias to msg)|
| ```sender.send_audio(```peer```,``` file```)``` | success_fail | 120.0 |  Sends audio message to peer|
| ```sender.send_typing(```peer```)``` | success_fail | [None](#default_answer_timeout) | Shows everyone else "User is typing" |
| ```sender.send_typing_abort(```peer```)``` | success_fail | [None](#default_answer_timeout) | Stop showing you are typing |
| ```sender.send_photo(```peer```,``` file```,``` caption```)``` | success_fail | 120.0 | Send a photo to a peer |
| ```sender.send_video(```peer```,``` file```,``` caption```)``` | success_fail | 120.0 | Send a video to a peer |
| ```sender.send_document(```peer```,``` file```)``` | success_fail | 120.0 | Send a document to a peer |
| ```sender.send_file(```peer```,``` file```)``` | success_fail | 120.0 | Send a file to a peer. The CLI tries to guess the filetype. |
| ```sender.send_location(```peer```,``` latitude```,``` longitude```)``` | success_fail | [None](#default_answer_timeout) | Send a geo location to a peer (lat and long are floats) |
| ```sender.send_contact(```peer```,``` phone```,``` first_name```,``` last_name```)``` | something | 60.0 | Sends contact (not necessary telegram user) to a peer. phone, first_name, last_name are strings |
| ```sender.send_text_from_file(```peer```,``` file```)``` | success_fail | 60.0 | Reads a file and uses "send_text() (which is an alias to msg)" to send the text content to a peer |
| ```sender.fwd(```peer```,``` msg_id```)``` | success_fail | [None](#default_answer_timeout) | Forwards message to peer. Forward to secret chats is forbidden |
| ```sender.fwd_media(```peer```,``` msg_id```)``` | success_fail | [None](#default_answer_timeout) | Forwards message media to peer. Forward to secret chats is forbidden. Result slightly differs from fwd |
| ```sender.reply_text(```msg_id```,``` text```)``` | success_fail | [None](#default_answer_timeout) | Sends text reply to message |
| ```sender.reply_audio(```msg_id```,``` file```)``` | success_fail | 120.0 | Sends audio reply to peer |
| ```sender.reply_contact(```msg_id```,``` phone```,``` first_name```,``` last_name```)``` | success_fail | 120.0 | Sends contact reply (not necessary telegram user) to a peer |
| ```sender.reply_document(```msg_id```,``` file```)``` | success_fail | [None](#default_answer_timeout) | Sends document reply to peer |
| ```sender.reply_file(```msg_id```,``` file```)``` | success_fail | 120.0 | Sends file (same as document) reply to peer |
| ```sender.reply_location(```msg_id```,``` latitude```,``` longitude```)``` | success_fail | [None](#default_answer_timeout) | Sends geo reply location |
| ```sender.reply_photo(```msg_id```,``` file```,``` caption```)``` | success_fail | 120.0 | Sends photo reply to peer |
| ```sender.reply_video(```msg_id```,``` file```,``` caption```)``` | success_fail | 120.0 | Sends video reply to peer |
| ```sender.broadcast_text(```user```,``` text```)``` | success_fail | 60.0 | Sends text to several users at once |

### message related
| Telgram command<br>(\* means optional) | Expected return parser | Timout<br>(seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| ```sender.load_audio(```msg_id```)``` | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| ```sender.load_chat_photo(```chat```)``` | success_fail | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| ```sender.load_file(```msg_id```)``` | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| ```sender.load_file_thumb(```msg_id```)``` | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| ```sender.load_document(```msg_id```)``` | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| ```sender.load_document_thumb(```msg_id```)``` | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| ```sender.load_photo(```msg_id```)``` | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| ```sender.load_video(```msg_id```)``` | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| ```sender.load_video_thumb(```msg_id```)``` | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |

### peer related
| Telgram command<br>(\* means optional) | Expected return parser | Timout<br>(seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| ```sender.mark_read(```peer```)``` | success_fail | [None](#default_answer_timeout) | Marks messages with peer as read |
| ```sender.history(```user```,``` *limit*\*```,``` *offset*\*```)``` | something | [None](#default_answer_timeout) | Prints messages with this peer (most recent message lower). Also marks messages as read |


### user related
| Telgram command<br>(\* means optional) | Expected return parser | Timout<br>(seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| ```sender.user_info(```user```)``` | something | [None](#default_answer_timeout) |  |
| ```sender.load_user_photo(```user```)``` | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |

### contact related
| Telgram command<br>(\* means optional) | Expected return parser | Timout<br>(seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| ```sender.contact_add(```phone```,``` first_name```,``` last_name```)``` | something | [None](#default_answer_timeout) | Tries to add user to contact list |
| ```sender.contact_add_by_card(```card```)``` | success_fail | [None](#default_answer_timeout) | Gets user by card and prints it name. You can then send messages to him as usual #todo: add args type |
| ```sender.contact_rename(```user```,``` first_name```,``` last_name```)``` | something | [None](#default_answer_timeout) | Renames contact #returns the new name |
| ```sender.contact_delete(```user```)``` | success_fail | [None](#default_answer_timeout) | Deletes contact from contact list |
| ```sender.contacts_list()``` | success_fail | [None](#default_answer_timeout) | Prints contact list |
| ```sender.contacts_search(```user_name```,``` *limit*\*```)``` | success_fail | [None](#default_answer_timeout) | Searches contacts by username |

### group chat related
| Telgram command<br>(\* means optional) | Expected return parser | Timout<br>(seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| ```sender.chat_info(```chat```)``` | something | [None](#default_answer_timeout) | Prints info about chat (id, members, admin, etc.) |
| ```sender.chat_set_photo(```chat```,``` file```)``` | success_fail | 120.0 | Sets chat photo. Photo will be cropped to square |
| ```sender.chat_add_user(```chat```,``` user```,``` *msgs_to_forward*\*```)``` | something | 60.0 | Adds user to chat. Sends him last msgs-to-forward message from this chat. Default 100 |
| ```sender.chat_del_user(```chat```,``` user```)``` | success_fail | [None](#default_answer_timeout) | Deletes user from chat |
| ```sender.chat_rename(```chat```,``` new_name```)``` | success_fail | [None](#default_answer_timeout) | Renames chat |
| ```sender.create_group_chat(```name```,``` user```)``` | success_fail | [None](#default_answer_timeout) | Creates group chat with users |
| ```sender.import_chat_link(```hash```)``` | success_fail | [None](#default_answer_timeout) | Joins to chat by link |
| ```sender.export_chat_link(```chat```)``` | success_fail | [None](#default_answer_timeout) | Prints chat link that can be used to join to chat |

### secret chat related
| Telgram command<br>(\* means optional) | Expected return parser | Timout<br>(seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| ```sender.create_secret_chat(```user```)``` | success_fail | [None](#default_answer_timeout) | Starts creation of secret chat |
| ```sender.accept_secret_chat(```secret_chat```)``` | success_fail | [None](#default_answer_timeout) | Accept a secret chat |
| ```sender.set_ttl(```secret_chat```)``` | success_fail | [None](#default_answer_timeout) | Sets secret chat ttl. Client itself ignores ttl |
| ```sender.visualize_key(```secret_chat```)``` | success_fail | [None](#default_answer_timeout) | Prints visualization of encryption key (first 16 bytes sha1 of it in fact) |

### own profile related
| Telgram command<br>(\* means optional) | Expected return parser | Timout<br>(seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| ```sender.set_profile_name(```first_name```,``` last_name```)``` | something | 60.0 | Sets profile name. |
| ```sender.set_username(```name```)``` | success_fail | [None](#default_answer_timeout) | Sets username. |
| ```sender.set_profile_photo(```file```)``` | something | 120.0 | Sets profile photo. Photo will be cropped to square |
| ```sender.status_online()``` | success_fail | [None](#default_answer_timeout) | Sets status as online |
| ```sender.status_offline()``` | success_fail | [None](#default_answer_timeout) | Sets status as offline|
| ```sender.export_card()``` | success_fail | [None](#default_answer_timeout) | Prints card that can be imported by another user with import_card method |

### system related
| Telgram command<br>(\* means optional) | Expected return parser | Timout<br>(seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| ```sender.quit()``` | response_fails | [None](#default_answer_timeout) | Quits immediately |
| ```sender.safe_quit()``` | response_fails | [None](#default_answer_timeout) | Waits for all queries to end, then quits |
| ```sender.main_session()``` | success_fail | [None](#default_answer_timeout) | Sends updates to this connection (or terminal). Useful only with listening socket |
| ```sender.dialog_list(```*limit*\* default: 100```,``` *offset*\* default: 100```)``` | List() | [None](#default_answer_timeout) | List of last conversations |
| sender.set_password(*hint*\* default: "empty") | success_fail | [None](#default_answer_timeout) | Sets password |

### diversa
| Telgram command<br>(\* means optional) | Expected return parser | Timout<br>(seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| ```sender.raw(```command```)``` | raw | 120.0 | just send custom shit to the cli. Use, if there are no fitting functions, because I didn't update
| ```sender.cli_help()``` | raw | [None](#default_answer_timeout) | Prints the help. (Needed for pytg itself!) |

## Exceptions

They are at ```pytg.exceptions```

### NoResponse:
This Exception means the CLI didn't send any response to that command in time.
Most commonly that happens with the ```status_online``` command, but still only occasionally.
You may change the timeout of any command with supplying ```result_timeout=<seconds>``` in the call.

```python
try:
    sender.status_online(result_timeout=5)  # wait up to 5 seconds
except NoResponse:  # from pytg.exceptions import NoResponse
    print("CLI did not responded in time")
```
