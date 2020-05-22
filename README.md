# Net-Utils
## Wildcard Calc
### Usage
```
python wildcard_calc.py --help
usage: wildcard_calc.py [-h] -a ADDRESS -w WILDCARD [-n]

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Address part of the statement, eg. 192.168.1.0
  -w WILDCARD, --wildcard WILDCARD
                        Wildcard mask, eg. 0.0.0.255
  -n, --netmask         Show

python wildcard_calc.py --address 192.168.1.0 --wildcard 0.0.1.0

Address: '192.168.1.0' Wildcard: '0.0.1.0'
192.168.0.0/32
192.168.1.0/32

python wildcard_calc.py --address 192.168.1.0 --wildcard 0.0.1.0 --netmask

Address: '192.168.1.0' Wildcard: '0.0.1.0'
192.168.0.0/255.255.255.255
192.168.1.0/255.255.255.255
```
    
