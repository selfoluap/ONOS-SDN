#!/bin/bash

sudo mn --custom ./topo.py --topo singleswitchtopo --mac --switch ovs,protocols=OpenFlow14 --controller remote,ip=172.17.0.2