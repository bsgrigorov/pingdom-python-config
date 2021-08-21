# Python library for Pingdom V3 API

To generate an Pingdom API V3 Token, go to https://my.pingdom.com/3/api-tokens

For Pingdom API V3 documents, go to https://docs.pingdom.com/api/

``` code:: python

  import pingdomv3
  client = Client('1234567890-999999999999999999999999999999999999999999999999999999999999')
  # get list of of a checks
  client.get_checks()
  # returns 
  client.get_check(2321)
  # create a new check
  client.create_check({...})
  # make a duplication of a check
  client.duplicate_check('5626090')
  # delete a check
  client.delete_check(5626090)

```
# Installation
    $> pip install pingdomv3
    
# Contribution welcome

I simply started this simple project to easily duplicate existing checks so I can quickly manipulate checks in a quick `duplicate -> modify -> live` way. If you need other APIs, feel free to contribute.


