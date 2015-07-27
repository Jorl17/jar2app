#!/bin/bash
if [ -z "$1" ]
  then
    PREFIX=/usr/bin
  else
    PREFIX=$1
fi

mkdir $PREFIX/jar2app_basefiles
cp -r jar2app_basefiles/* $PREFIX/jar2app_basefiles
cp jar2app $PREFIX
chmod +x $PREFIX/jar2app

