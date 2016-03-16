## Examples
There are some example in this folder.

- [command_send_message](https://github.com/luckydonald/pytg/blob/master/examples/command_send_message.py): Simplest way to just send a message.
    
- [command_who_am_i](https://github.com/luckydonald/pytg/blob/master/examples/command_who_am_i.py): A simple example printing infos about yourself
    - get the **@username** etc.
    
- [command_dialog_list](https://github.com/luckydonald/pytg/blob/master/examples/command_dialog_list.py): Simpler example printing the list of chats you have.
    - Shows how to execute commands like `dialog_list` on the CLI.
    
- [bot_dump](https://github.com/luckydonald/pytg/blob/master/examples/bot_dump.py):  A small bot printing the `msg` message object.
    - So you can see yourself how messages look like.    
    
- [bot_ping](https://github.com/luckydonald/pytg/blob/master/examples/bot_ping.py):  A simple bot reacting to messages.
    - like the dump bot, but it responds to a `ping` with a `pong`.
    
- [bot_source_of_reply](https://github.com/luckydonald/pytg/blob/master/examples/bot_source_of_reply.py): When replying to any message with `#top`, the bot will show you the origin of that reply.
    - This demonstrates how you could use `message_get` command and the `reply_id` information.

- [bot_with_context](https://github.com/luckydonald/pytg/blob/master/examples/bot_with_context.py): Talk to a bot, not only a simple command.
    - Demonstrates how to build converations with the use of generators and the `yield` statement.


