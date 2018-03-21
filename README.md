Python small lib for broadcasting jsonified data
============================

# Core concepts

## Channel

*Channel*
An udp multicasting channel on wich components can both read and write data.
A channel is essentially represented by a tuple (multicast_ip, port).
Here follows a snippet.

```python
from pybroadchan import UDPChannel
udpchan = UDPChannel('224.1.1.1', 1234, 1024)

# --- READ DATA ---
(data, addr) = udpchan.recv()
print 'received %s' % data

# --- SEND DATA ---
udpchan.send("Hello World!")
```

```python
# Creates a log file with 
# - component ownwer description (sample_reader)
# - file name in the form ${fname}_${date}.log
logger = LogFactory('sample_reader', '/logs/reader')
# Instantiate a UDP channel by specifying a custom logger
udpchan = UDPChannel('224.1.1.1', 1234, 1024, logger)

# READ
(data, addr) = udpchan.recv()
print 'received %s' % data

# WRITE
udpchan.send("Hello World!")
```

***SerializableData***
To simplify the serialization of data through multicast channel a basic class is
provided.
It's nothing special but useful to make stuff easy.

```python
# Creates an object and dynamically creates its attributes
data=SerializableData()
data.info.name='Daniele'
data.info.surname = 'Strollo'
data.info.email = 'daniele.strollo@gmail.com'

# Take a JSON representation
jsondata=data.toJSON()

# From JSON to object representation
obj=Message.fromJSON(jsondata)
```    

```json

// Here the json representation
{
  "info": {
    "name": "Daniele",
    "surname": "Strollo",
    "email": "daniele.strollo@gmail.com",
  }
}
```
