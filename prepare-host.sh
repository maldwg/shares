#! /bin/bash

sudo apt update -y
sudo upgrade -y

sudo apt install python3 python3-pip -y

pip install yfinance pandas matplotlib technical_indicators_lib

git clone https://github.com/maldwg/shares.git