# Documentation
(generated)
### `pytg.sender.Sender`

- `msg(peer, test)`: Sends text message to peer
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `test`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `send_msg(peer, test)`: Sends text message to peer
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `test`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `send_text(peer, test)`: Sends text message to peer
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `test`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `send_audio(peer, file)`: 
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `send_typing(peer)`: 
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `send_typing_abort(peer)`: 
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `send_photo(peer, file, caption)`: 
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
		- `caption`: *optional*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `send_video(peer, file, caption)`: 
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
		- `caption`: *optional*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `send_document(peer, file, caption)`: 
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
		- `caption`: *optional*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `send_file(peer, file)`: 
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `send_location(peer, latitude, longitude)`: 
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `latitude`: *mandatory*, needs a Double (type: `float`), and may not be repeated.
		- `longitude`: *mandatory*, needs a Double (type: `float`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `send_contact(peer, phone, first_name, last_name)`: ret: formated message
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `phone`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
		- `first_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
		- `last_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `send_text_from_file(peer, file)`: 
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `fwd(peer, msg_id)`: Forwards message to peer. Forward to secret chats is forbidden
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `fwd_media(peer, msg_id)`: Forwards message media to peer. Forward to secret chats is forbidden. Result slightly differs from fwd
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `reply(msg_id, text)`: Sends text reply to message
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
		- `text`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `reply_text(msg_id, text)`: Sends text reply to message
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
		- `text`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `reply_audio(msg_id, file)`: Sends audio to peer
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `reply_contact(msg_id, phone, first_name, last_name)`: Sends contact (not necessary telegram user)
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
		- `phone`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
		- `first_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
		- `last_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `reply_document(msg_id, file)`: Sends document to peer
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `reply_file(msg_id, file)`: Sends document to peer
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `reply_location(msg_id, latitude, longitude)`: Sends geo location
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
		- `latitude`: *mandatory*, needs a Double (type: `float`), and may not be repeated.
		- `longitude`: *mandatory*, needs a Double (type: `float`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `reply_photo(msg_id, file, caption)`: Sends photo to peer
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
		- `caption`: *optional*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `reply_video(msg_id, file, caption)`: Sends video to peer
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
		- `caption`: *optional*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `broadcast_text(user, text)`: Sends text to several users at once
	- Arguments:
		- `user`: *mandatory*, needs a User (type: `str`), and may  be repeated.
		- `text`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `message_delete(msg_id)`: Deletes message
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `message_get(msg_id)`: Get message by id
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `messages_search(peer, limit, from, to, offset, pattern)`: Search for pattern in messages from date from to date to (unixtime) in messages with peer (if peer not present, in all messages)
	- Arguments:
		- `peer`: *optional*, needs a Peer (type: `str`), and may not be repeated.
		- `limit`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
		- `from`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
		- `to`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
		- `offset`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
		- `pattern`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `load_audio(msg_id)`: Downloads file to downloads dirs. Prints file name after download end
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `load_chat_photo(chat)`: Downloads file to downloads dirs. Prints file name after download end
	- Arguments:
		- `chat`: *mandatory*, needs a Chat (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `load_file(msg_id)`: Downloads file to downloads dirs. Prints file name after download end
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `load_file_thumb(msg_id)`: Downloads file to downloads dirs. Prints file name after download end
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `load_document(msg_id)`: Downloads file to downloads dirs. Prints file name after download end
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `load_document_thumb(msg_id)`: Downloads file to downloads dirs. Prints file name after download end
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `load_photo(msg_id)`: Downloads file to downloads dirs. Prints file name after download end
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `load_video(msg_id)`: Downloads file to downloads dirs. Prints file name after download end
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `load_video_thumb(msg_id)`: Downloads file to downloads dirs. Prints file name after download end
	- Arguments:
		- `msg_id`: *mandatory*, needs a MsgId (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `mark_read(peer)`: Marks messages with peer as read
	- Arguments:
		- `peer`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `history(user, limit, offset)`: Prints messages with this peer (most recent message lower). Also marks messages as read
	- Arguments:
		- `user`: *mandatory*, needs a Peer (type: `str`), and may not be repeated.
		- `limit`: *optional*, needs a PositiveNumber (type: `int > 0`), and may not be repeated.
		- `offset`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `resolve_username(@username)`: Searches user by username
	- Arguments:
		- `@username`: *mandatory*, needs a Username (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `user_info(user)`: 
	- Arguments:
		- `user`: *mandatory*, needs a User (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `load_user_photo(user)`: Downloads file to downloads dirs. Prints file name after download end
	- Arguments:
		- `user`: *mandatory*, needs a User (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `get_self()`: get our user info
	- Arguments:
		No arguments.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.anything` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `whoami()`: get our user info
	- Arguments:
		No arguments.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.anything` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `contact_add(phone, first_name, last_name)`: Tries to add user to contact list
	- Arguments:
		- `phone`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
		- `first_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
		- `last_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.anything` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `contact_add_by_card(card)`: Gets user by card and prints it name. You can then send messages to him as usual #todo: add args type
	- Arguments:
		- `card`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `contact_rename(user, first_name, last_name)`: Renames contact #returns the new name
	- Arguments:
		- `user`: *mandatory*, needs a User (type: `str`), and may not be repeated.
		- `first_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
		- `last_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `contact_delete(user)`: Deletes contact from contact list
	- Arguments:
		- `user`: *mandatory*, needs a User (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `contacts_list()`: Prints contact list
	- Arguments:
		No arguments.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.List` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `contacts_search(user_name, limit)`: Searches contacts by username
	- Arguments:
		- `user_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
		- `limit`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `chat_info(chat)`: Prints info about chat (id, members, admin, etc.)
	- Arguments:
		- `chat`: *mandatory*, needs a Chat (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `chat_set_photo(chat, file)`: 
	- Arguments:
		- `chat`: *mandatory*, needs a Chat (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `chat_add_user(chat, user, msgs_to_forward)`: Adds user to chat. Sends him last msgs-to-forward message from this chat. Default 100
	- Arguments:
		- `chat`: *mandatory*, needs a Chat (type: `str`), and may not be repeated.
		- `user`: *mandatory*, needs a User (type: `str`), and may not be repeated.
		- `msgs_to_forward`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `chat_del_user(chat, user)`: Deletes user from chat
	- Arguments:
		- `chat`: *mandatory*, needs a Chat (type: `str`), and may not be repeated.
		- `user`: *mandatory*, needs a User (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `chat_rename(chat, new_name)`: Renames chat
	- Arguments:
		- `chat`: *mandatory*, needs a Chat (type: `str`), and may not be repeated.
		- `new_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `create_group_chat(name, user)`: Creates group chat with users
	- Arguments:
		- `name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
		- `user`: *mandatory*, needs a User (type: `str`), and may  be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `import_chat_link(hash)`: Joins to chat by link
	- Arguments:
		- `hash`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `export_chat_link(chat)`: Prints chat link that can be used to join to chat
	- Arguments:
		- `chat`: *mandatory*, needs a Chat (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `create_secret_chat(user)`: Starts creation of secret chat
	- Arguments:
		- `user`: *mandatory*, needs a User (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `accept_secret_chat(secret_chat)`: 
	- Arguments:
		- `secret_chat`: *mandatory*, needs a SecretChat (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `set_ttl(secret_chat)`: Sets secret chat ttl. Client itself ignores ttl
	- Arguments:
		- `secret_chat`: *mandatory*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `visualize_key(secret_chat)`: Prints visualization of encryption key (first 16 bytes sha1 of it in fact)
	- Arguments:
		- `secret_chat`: *mandatory*, needs a SecretChat (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `channel_get_admins(channel, limit, offset)`: Gets channel admins
	- Arguments:
		- `channel`: *mandatory*, needs a Channel (type: `str`), and may not be repeated.
		- `limit`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
		- `offset`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.List` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `channel_get_members(channel, limit, offset)`: Gets channel members
	- Arguments:
		- `channel`: *mandatory*, needs a Channel (type: `str`), and may not be repeated.
		- `limit`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
		- `offset`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.List` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `channel_info(channel)`: Prints info about channel (id, members, admin, etc.)
	- Arguments:
		- `channel`: *mandatory*, needs a Channel (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `channel_invite(channel, user)`: Invites user to channel
	- Arguments:
		- `channel`: *mandatory*, needs a Channel (type: `str`), and may not be repeated.
		- `user`: *mandatory*, needs a User (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `channel_join(channel)`: Joins to channel
	- Arguments:
		- `channel`: *mandatory*, needs a Channel (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `channel_kick(channel, user)`: Kicks user from channel
	- Arguments:
		- `channel`: *mandatory*, needs a Channel (type: `str`), and may not be repeated.
		- `user`: *mandatory*, needs a User (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `channel_leave(channel)`: Leaves from channel
	- Arguments:
		- `channel`: *mandatory*, needs a Channel (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `channel_list(limit, offset)`: List of last channels
	- Arguments:
		- `limit`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
		- `offset`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.List` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `channel_set_about(channel, about)`: Sets channel about info.
	- Arguments:
		- `channel`: *mandatory*, needs a Channel (type: `str`), and may not be repeated.
		- `about`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `channel_set_username(channel, name)`: Sets channel username info.
	- Arguments:
		- `channel`: *mandatory*, needs a Channel (type: `str`), and may not be repeated.
		- `name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `channel_set_photo(channel, file)`: Sets channel photo. Photo will be cropped to square
	- Arguments:
		- `channel`: *mandatory*, needs a Channel (type: `str`), and may not be repeated.
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `channel_rename(channel, new_name)`: Renames channel
	- Arguments:
		- `channel`: *mandatory*, needs a Channel (type: `str`), and may not be repeated.
		- `new_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `set_profile_name(first_name, last_name)`: Sets profile name.
	- Arguments:
		- `first_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
		- `last_name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `set_username(name)`: Sets username.
	- Arguments:
		- `name`: *mandatory*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `set_profile_photo(file)`: Sets profile photo. Photo will be cropped to square
	- Arguments:
		- `file`: *mandatory*, needs a FilePath (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.something` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `status_online()`: Sets status as online
	- Arguments:
		No arguments.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `status_offline()`: Sets status as offline
	- Arguments:
		No arguments.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `export_card()`: Prints card that can be imported by another user with import_card method
	- Arguments:
		No arguments.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `quit()`: Quits immediately
	- Arguments:
		No arguments.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.response_fails` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `safe_quit()`: Waits for all queries to end, then quits
	- Arguments:
		No arguments.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.response_fails` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `main_session()`: Sends updates to this connection (or terminal). Useful only with listening socket
	- Arguments:
		No arguments.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `dialog_list(limit, offset)`: List of last conversations
	- Arguments:
		- `limit`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
		- `offset`: *optional*, needs a NonNegativeNumber (type: `int >= 0`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.List` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `set_password(hint)`: Sets password
	- Arguments:
		- `hint`: *optional*, needs a UnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.success_fail` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `raw(command)`: just send custom shit to the cli. Use, if there are no fitting functions, because I didn't update.
	- Arguments:
		- `command`: *mandatory*, needs a UnescapedUnicodeString (type: `str`), and may not be repeated.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.raw` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.

- `cli_help()`: Prints the help. (Needed for pytg itself!)
	- Arguments:
		No arguments.
	- Keyword arguments:
		- `enable_preview`: *optional*, if the URL found in a message should have a preview. Default: False. (Will be ignored by the CLI with non-sending commands.)
		- `retry_connect`: *optional*, how often the initial connection should be retried. Default: 2. Negative number means infinite.
		- `retry_connect`: *optional*. How long, in seconds, we wait for the cli to answer the send command. Set to explicitly to `None` to use the global default timeout (`Sender.default_answer_timeout`) instead of the default timeout for the given command. To use the default timeout for that command omit this parameter. Default: default timeout for the given command
		- `reply_id`: *optional*, this command is kept for compatibility. Please use the reply commands! Default: None. (Will be ignored by the CLI with non-sending commands.)
	- Returns:
		the parsed result using `pytg.result_parser.raw` parser or raises an `pytg.exceptions.IllegalResponseExceptions`.