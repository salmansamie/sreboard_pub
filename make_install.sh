#!/usr/bin/env bash

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

xcode-select --install

brew install python3 git autoconf automake libtool nettle pkg-config gtk+3 gnome-icon-theme hicolor-icon-theme

brew update

export LIBTOOL=glibtool

git clone git@gitlab.service-now.com:salman.rahman/sreboard.git

cd sreboard && git clone git@gitlab.service-now.com:salman.rahman/stoken.git

cd stoken && bash autogen.sh

./configure && make && make check && make install

stoken import --file "$1" && cd ..

pip install upgrade pip

pip install pyinstaller

pyinstaller -F sreboard.py factors.py data.py board.cnf cord__attr.json banner.txt

cd dist/ && cp sreboard /usr/local/bin/


