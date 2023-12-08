#!/bin/bash

#this script is for bootstrapping an onos application

export ONOS\_POM\_VERSION=2.7.0

tools/onos-create-app app org.skku skku-app 1.0-SNAPSHOT org.skku.app

cd skku-app
mvn clean install
cd ..
tools/onos-app $1 install! target/skku-app-1.0-SNAPSHOT.oar