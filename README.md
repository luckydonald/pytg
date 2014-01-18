## PyTG

A Python module that wraps around [Telegram messenger CLI](https://github.com/vysheng/tg).

### Installation

PyTG requires a patched copy of Telegram messenger CLI to make message parsing feasible. To install the patched Telegram messenger CLI:

Clone GitHub Repository

    $ git clone https://github.com/efaisal/tg.git && cd tg
        
or download and extract zip

    $ wget https://github.com/efaisal/tg/archive/master.zip -O tg.zip
    $ tar xzf tg.zip && cd tg

Then run

    $ ./configure

or

    $ ./configure --disable-liblua

if you don't want Lua support.

Next run

    $ make

Telegram messenger CLI has its own dependencies. See https://github.com/efaisal/tg for details.

Now you are ready to install PyTG

Clone GitHub Repository

    $ git clone https://github.com/vysheng/tg.git && cd tg
        
or download and extract zip

    $ wget https://github.com/efaisal/pytg/archive/master.zip -O pytg.zip
    $ tar xzf pytg.zip && cd pytg && python setup.py install

