# tcpmodbus2mqtt
Convert TCP modbus to mqtt messages.

## Usage

### docker-compose.yml
Add a container to your `docker-compose.yml` file like the following example

````
  services:

    serialmodbus2mqtt:
      image: rmorillo/tcpmodbus2mqtt
      privileged: true
      environment:
        MODBUS_HOST_IP: '192.168.1.132'
        MODBUS_HOST_PORT: '10502'
        MQTT_BROKER_IP: '127.0.0.1'
        MQTT_BROKER_PORT: '1883'
      network_mode: host
      restart: "no"
````

### Datamodel
The `datamodel.json` file defines the parameters you want to read from my modbus slave. The idea is that anyone can use this to add any parameter with any device or machine with a standard MODBUS slave. 
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
* format of the value (will be decoded accordingly) __NOTE__: as of now, ony ieee754 is implemented

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

## Acknowledgments
Some inspiration on:
* [modbus2mqtt](https://github.com/Instathings/modbus2mqtt)
* [modbus-herdsman-converters](https://github.com/Instathings/modbus-herdsman-converters)
