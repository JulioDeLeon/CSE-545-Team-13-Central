#!/bin/bash

apt-get -y --ignore-missing install $(cat packages.list)
