# SNMP Light Check
SNMP poll light levels for a list of Cisco IOS node-ports

## Installation
This script uses the pyyaml and easysnmp modules

`pip install pyyaml`

See https://easysnmp.readthedocs.io/en/latest/ for easysnmp installation instructions

## Configuration
Update config.yml with the snmp community string and domain for your nodes

## Create a Node-port CSV
This script reads a node,port list from a CSV. Create a CSV with the node-ports you want to poll using example.csv as a template.

## Usage
`python snmp_lightcheck.py my_node_ports.csv`
