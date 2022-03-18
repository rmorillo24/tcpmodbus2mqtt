# tcpmodbus2mqtt
Convert TCP modbus to mqtt messages.

## How it works
### Datamodel
The `datamodel.json` file defines the parameters I want to read from my modbus slave. The idea is that anyone can use this to add any other parameter with my initial smart meter, or with another one supporting modbus. 
An example of a parameter that will be automatically be read:

```
    "instant_flow": {
                "address": 1,
                "length": 2,
                "polling_secs": 25,
                "format": "ieee754"
    }
```

The format of the data model allows to configure

* Input or output variables
* Register address
* Number of registers to read for this parameter
* format of the value (will be decoded accordingly)

### Reading and looping
Each parameter has a polling time, that may depend on the meaning of the parameter. The script will spawn a process for each parameter. This process will loop infinitelly, with a sleeping time bewteen loops equaling the polling time we have defined

### Servers configuration
Define the following Environment variables to allow the block communicate with the modbus slave and the mqtt server
````
    MODBUS_HOST_IP
    MODBUS_HOST_PORT
    MQTT_BROKER_IP
    MQTT_BROKER_PORT
````

