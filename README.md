# tcpmodbus2mqtt
Convert TCP modbus to mqtt messages.
Designed as a block that will allow to use it as a docker service, like in a balena device, simply configuring it as a balenaBlock

## How it works
The services loads a datamodel that defines the  the parameters you want to read from a given modbus slave. The idea is that anyone can use use this service with any standard MODBUS slave, only by configuring the datamodel configuration. 

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

## Block usage and configuration
To use the block in you app, you will have to add it as a service 

### docker-compose file
Add a container to your `docker-compose.yml` file like the following example

````
  services:

    tcpmodbus2mqtt:
      image: bh.cr/rmorillo/tcpmodbus2mqtt
      privileged: true
      network_mode: host
      restart: "no"
````
This example pulls directly from the balenaHub registry. You can also clone it and use it in your own repo

### Environment variables
These environment variables have to be defined in each of your devices, according to the servers configuration.

#### Datamodel
`DATAMODEL` The environment variable is a single string JSON with the contents of your datamodel. Please look at the `datamodel.json` file as an example of how it has to be defined

### Servers configuration
The following Environment variables define the MODBUS and MQTT server parameters:

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
