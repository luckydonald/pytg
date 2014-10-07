## PyTG

A Python package that wraps around [Telegram messenger CLI](https://github.com/vysheng/tg).

### Installation

PyTG requires a patched copy of Telegram messenger CLI to make message parsing feasible. To install the patched Telegram messenger CLI:

Clone GitHub Repository

    $ git clone https://bitbucket.org/luckydonald/tg-for-pytg2.git && cd tg-for-pytg2
        
or download and extract zip **//TODO**

    $ wget 404.zip -O tg-for-pytg2.zip 
    $ tar xzf tg-for-pytg2.zip && cd tg-for-pytg2

Then, run

    $ ./configure

or

    $ ./configure --disable-liblua

if you don't want Lua support.

Next, run

    $ make

Telegram messenger CLI has its own dependencies. See [luckydonald/tg-for-pytg2](https://bitbucket.org/luckydonald/tg-for-pytg2) for details.

Once you build successfully, try to run

    $ ./bin/telegram-cli

Register your client, if required. Please note that PyTG does not support client registration yet.

Now you are ready to install PyTG2

Clone PyTG 2 Repository

    $ git clone https://bitbucket.org/luckydonald/pytg2.git && cd pytg2 && sudo python setup.py install
        
or download and extract zip **TODO**

    $ wget .zip -O pytg2.zip
    $ tar xzf pytg2.zip && cd pytg2 && python setup.py install