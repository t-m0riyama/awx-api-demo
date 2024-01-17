AWX API Demo
============

This repository contains examples of AWX job execution via REST API.
This is a sample of calling the API from the GUI(Flet).

See also. https://flet.dev/

## Requirement
* Python 3.8 or later
* flet 0.11 or later

## Contents

``` contents
awx-api-demo
 |-- LICENSE
 |-- README.md: this document
 |-- awx_demo
 |   |-- awx_api: AWX API modules
 |   `-- components: Flet component modules
 |-- main.py: main script
 `-- requirements.txt: dependent modules
```

## How to use
1. specify the AWX URL.
```bash
$ export AWX_URL=https://awx.example.com/
```

2. specifies the port number to listen on, if necessary. (default 8888)
```bash
$ export FLET_PORT=8000
```

3. run the main script.
```bash
$ python main.py
```

