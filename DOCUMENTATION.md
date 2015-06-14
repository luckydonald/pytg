# Table of Contents
1. [Sending Messages](#sending-messages)
2. [Message Related](#message-related)
3. [peer](#peer)
4. [user](#user)
5. [contacts](#contacts)
6. [group chats](#group-chats)
7. [secret chats](#secret-chats)
8. [own profile](#own-profile)
9. [system](#system)
10. [diversa](#diversa)

#Sender (assuming the sender is an instance of pytg.sender.Sender)

### Sending Messages
| Telgram command (\* means optional) | Expected return parser | Timout (in seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| Sender.msg(peer, text) | success_fail | 60.0 | Sends text message to peer |
| Sender.send_msg(peer, text) | success_fail | 60.0 | Sends text message to peer (alias to msg)|
| Sender.send_text(peer, text) | success_fail | 60.0 | Sends text message to peer (alias to msg)|
| Sender.send_audio(peer, file) | success_fail | 120.0 |  Sends audio message to peer|
| Sender.send_typing(peer) | success_fail | None | Shows everyone else "User is typing" |
| Sender.send_typing_abort(peer) | success_fail | None | Stop showing you are typing |
| Sender.send_photo(peer, file, caption) | success_fail | 120.0 | Send a photo to a peer |
| Sender.send_video(peer, file, caption) | success_fail | 120.0 | Send a video to a peer |
| Sender.send_document(peer, file) | success_fail | 120.0 | Send a document to a peer |
| Sender.send_file(peer, file) | success_fail | 120.0 | Send a file (same as document) to a peer |
| Sender.send_location(peer, latitude, longitude) | success_fail | None | Send a geo location to a peer (lat and long are doubles) |
| Sender.send_contact(peer, phone, first_name, last_name) | something | 60.0 | Sends contact (not necessary telegram user) to a peer |
| Sender.send_text_from_file(peer, file) | success_fail | 60.0 | Reads a file and uses "send_text() (which is an alias to msg)" to send the text content to a peer |
| Sender.fwd(peer, msg_id) | success_fail | None | Forwards message to peer. Forward to secret chats is forbidden |
| Sender.fwd_media(peer, msg_id) | success_fail | None | Forwards message media to peer. Forward to secret chats is forbidden. Result slightly differs from fwd |
| Sender.reply_text(msg_id, text) | success_fail | None | Sends text reply to message |
| Sender.reply_audio(msg_id,file) | success_fail | 120.0 | Sends audio reply to peer |
| Sender.reply_contact(msg_id, phone, first_name, last_name) | success_fail | 120.0 | Sends contact reply (not necessary telegram user) to a peer |
| Sender.reply_document(msg_id, file) | success_fail | None | Sends document reply to peer |
| Sender.reply_file(msg_id, file) | success_fail | 120.0 | Sends file (same as document) reply to peer |
| Sender.reply_location(msg_id, latitude, longitude) | success_fail | None | Sends geo reply location |
| Sender.reply_photo(msg_id, file, caption) | success_fail | 120.0 | Sends photo reply to peer |
| Sender.reply_video(msg_id, file, caption) | success_fail | 120.0 | Sends video reply to peer |
| Sender.broadcast_text(user, text) | success_fail | 60.0 | Sends text to several users at once |

### Message Related
| Telgram command (\* means optional) | Expected return parser | Timout (in seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| Sender.load_audio(msg_id) | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| Sender.load_chat_photo(chat) | success_fail | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| Sender.load_file(msg_id) | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| Sender.load_file_thumb(msg_id) | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| Sender.load_document(msg_id) | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| Sender.load_document_thumb(msg_id) | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| Sender.load_photo(msg_id) | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| Sender.load_video(msg_id) | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |
| Sender.load_video_thumb(msg_id) | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |

### peer
| Telgram command (\* means optional) | Expected return parser | Timout (in seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| Sender.mark_read(peer) | success_fail | None | Marks messages with peer as read |
| Sender.history(user, limit\*, offset\*) | something | None | Prints messages with this peer (most recent message lower). Also marks messages as read |


### user
| Telgram command (\* means optional) | Expected return parser | Timout (in seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| Sender.user_info(user) | something | None |  |
| Sender.load_user_photo(user) | something | 120.0 | Downloads file to downloads dirs. Prints file name after download end |

### contacts
| Telgram command (\* means optional) | Expected return parser | Timout (in seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| Sender.contact_add(phone, first_name, last_name) | something | None | Tries to add user to contact list |
| Sender.contact_add_by_card(card) | success_fail | None | Gets user by card and prints it name. You can then send messages to him as usual #todo: add args type |
| Sender.contact_rename(user, first_name, last_name) | something | None | Renames contact #returns the new name |
| Sender.contact_delete(user) | success_fail | None | Deletes contact from contact list |
| Sender.contacts_list() | success_fail | None | Prints contact list |
| Sender.contacts_search(user_name, limit\*) | success_fail | None | Searches contacts by username |

### group chats
| Telgram command (\* means optional) | Expected return parser | Timout (in seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| Sender.chat_info(chat) | something | None | Prints info about chat (id, members, admin, etc.) |
| Sender.chat_set_photo(chat, file) | success_fail | 120.0 | Sets chat photo. Photo will be cropped to square |
| Sender.chat_add_user(chat, user, msgs_to_forward\*) | something | 60.0 | Adds user to chat. Sends him last msgs-to-forward message from this chat. Default 100 |
| Sender.chat_del_user(chat, user) | success_fail | None | Deletes user from chat |
| Sender.chat_rename(chat, new_name) | success_fail | None | Renames chat |
| Sender.create_group_chat(name, user) | success_fail | None | Creates group chat with users |
| Sender.import_chat_link(hash) | success_fail | None | Joins to chat by link |
| Sender.export_chat_link(chat) | success_fail | None | Prints chat link that can be used to join to chat |

### secret chats
| Telgram command (\* means optional) | Expected return parser | Timout (in seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| Sender.create_secret_chat(user) | success_fail | None | Starts creation of secret chat |
| Sender.accept_secret_chat(secret_chat) | success_fail | None | Accept a secret chat |
| Sender.set_ttl(secret_chat) | success_fail | None | Sets secret chat ttl. Client itself ignores ttl |
| Sender.visualize_key(secret_chat) | success_fail | None | Prints visualization of encryption key (first 16 bytes sha1 of it in fact) |

### own profile
| Telgram command (\* means optional) | Expected return parser | Timout (in seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| Sender.set_profile_name(first_name, last_name) | something | 60.0 | Sets profile name. |
| Sender.set_username(name) | success_fail | None | Sets username. |
| Sender.set_profile_photo(file) | something | 120.0 | Sets profile photo. Photo will be cropped to square |
| Sender.status_online | success_fail | None | Sets status as online |
| Sender.status_offline() | success_fail | None | Sets status as offline|
| Sender.export_card() | success_fail | None | Prints card that can be imported by another user with import_card method |

### system
| Telgram command (\* means optional) | Expected return parser | Timout (in seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| Sender.quit() | response_fails | None | Quits immediately |
| Sender.safe_quit() | response_fails | None | Waits for all queries to end, then quits |
| Sender.main_session() | success_fail | None | Sends updates to this connection (or terminal). Useful only with listening socket |
| Sender.dialog_list(limit\* default: 100, offset\* default: 100) | List() | None | List of last conversations |
| Sender.set_password(hint\* default: "empty") | success_fail | None | Sets password |

### diversa
| Telgram command (\* means optional) | Expected return parser | Timout (in seconds) | Description |
| ------------------ | ---------------------- | ------------------------ | ----------- |
| Sender.raw(command) | raw | 120.0 | just send custom shit to the cli. Use, if there are no fitting functions, because I didn't update
| Sender.cli_help() | raw | None | Prints the help. (Needed for pytg itself!) |
