#!/usr/bin/env bash

#build executable for three network
sed s/NAME_OF_NETWORK/three/ < webtext_main.py > webtext_main_temp.py 
pyinstaller webtext_main_temp.py --onefile -n three --hidden-import three --clean --distpath ../

#build executable for eir network
sed s/NAME_OF_NETWORK/eir/ < webtext_main.py > webtext_main_temp.py 
pyinstaller webtext_main_temp.py --onefile -n eir --hidden-import eir --clean --distpath ../

rm webtext_main_temp.py
rm -rf __pycache__
rm -rf build
rm *.spec