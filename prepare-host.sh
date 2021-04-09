#! /bin/bash

sudo apt update -y
sudo upgrade -y

sudo apt install python3 python3-pip -y

pip3 install yfinance pandas matplotlib technical_indicators_lib
