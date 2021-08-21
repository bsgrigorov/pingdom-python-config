# Pingdom API
We are using Pingdom API v3 and a python library for v3 [pingdomv3](https://github.com/cheney-yan/pingdom-py-api-v3).
Check management: create, delete, update, list

## Uptime Checks
In order to run the scripts you will need an API token from Pingdom. You can create one [here](https://my.pingdom.com/app/api-tokens) or reuse an existing one.

To create or update the checks you will need to make changes to [checks](checks) folder, export the token and run the script.
``` code:: shell
$ export PINGDOM_API_TOKEN=
$ python src/configure_checks.py
```
The checks will be created if they do not exist and the existing checks will be updated with changes made to [checks.yaml](src/checks.yaml). 

If you wish to cleanup checks not in the [checks](checks) folder run:
```
$ python src/configure_checks.py --clean
usage: configure_checks.py [-h] [-c [CLEAN [CLEAN ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -c [CLEAN [CLEAN ...]], --clean [CLEAN [CLEAN ...]]
                        Clean all other checks.
```

### Integrations
To add integrations to checks so that you are alerted in Slack or other such tools you need to create integrations in Pingdom UI. ALternatively you can write your code that does it using the API. 

Once you have created the integrations, you need to get the integration id of each integration by selecting the integration in the UI and looking at the URL. It will have the id like so:
```
https://my.pingdom.com/integrations/settings#integration=107059
```

Note: Any arrays in the JSON for the checks needs to be converted to a comma-delimmited string, or else it will take only one of the array elements.