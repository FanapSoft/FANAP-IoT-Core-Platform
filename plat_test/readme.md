# Platform checker
Checking Fanap Enterprise IOT Platform reset API

Supported commands:
- Devicetype Add
- Devicetype List
- Devicetype Show



## ToDo
- Set correct `processes` count in pool configuration.
- Support delete command
- Support delete available data-types
 

## Requirements 
- Python 3.x
- requests


## How to use

```
usage: plat_tester.py [-h] [-t token] [-H host] [-c cnt] [-prefix prefix]
                      [-T thread-cnt] [-f file]
                      {add,delete,list,show}

Interactive Tests

positional arguments:
  {add,delete,list,show}
                        Select type of test. "add": Add new devicetypes and
                        store responses in file. "list": Compare devicetype-
                        list with response file. "show": Compare devicetype-
                        show content with resonse file. "delete-all: Delete
                        all defined devicetypes.

optional arguments:
  -h, --help            show this help message and exit
  -t token              Overwrite access token
  -H host               Determine HOST address
                        default=http://api.thingscloud.ir/srv/iot
  -c cnt                Test count for add
  -prefix prefix        Name prefix for test operations
  -T thread-cnt         Thread count for concurrent process default=1
  -f file               Target file for test default=out.csv
```

