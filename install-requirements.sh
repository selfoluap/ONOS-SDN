#!/bin/bash

#install requirements
sudo apt-get update
sudo apt-get install curl
sudo apt-get install openjdk-11-jdk
sudo apt-get install maven


#install onos-admin-tools
curl -sS --fail https://repo1.maven.org/maven2/org/onosproject/onos-releases/2.7.0/onos-admin-2.7.0.tar.gz \
  > tools.tar.gz
tar xf tools.tar.gz
mv onos-admin-2.7.0 tools