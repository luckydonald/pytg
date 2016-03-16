## Examples
There are some example in this folder.

- `command_send_message.py`: Simplest way to just send a message.
    - If you don't need to receive messages.
- `command_who_am_i`: A simple example printing infos about yourself
    - get the **@username** etc.
- `command_dialog_list.py`: Simpler example printing the list of chats you have.
    - Shows how to execute commands like `dialog_list` on the CLI.
- `bot_dump.py`:  A small bot printing the `msg` message object.
    - So you can see yourself how messages look like.    
- `bot_ping.py`:   A simple bot reacting to messages.
    - like the dump bot, but it responds to a `ping` with a `pong`.
- `bot_source_of_reply`: When replying to any message with `#top`, the bot will show you the origin of that reply.
    - This demonstrates how you could use `message_get` command and the `reply_id` information.
- `bot_with_context`: Talk to a bot, not only a simple command.
    - Demonstrates how to build converations with the use of generators and the `yield` statement.


