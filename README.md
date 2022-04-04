# tcpmodbus2mqtt
Convert TCP modbus to mqtt messages.
Designed as a block that will allow to use it as a docker service, like in a balena device, simply configuring it as a balenaBlock

## Block usage and configuration
To use the block in you app, you will have to add it as a service and define Device Variables in your app

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
These environment variables have to be defined in each of your devices, as they may have different values and datamodels.
The following is a screenshot of the balenaCloud's `Device Variables` tab

![Device Variables screenshot example](https://raw.githubusercontent.com/rmorillo24/tcpmodbus2mqtt/main/assets/devicevariables.png)

_NOTE:_ `DATAMODEL` is the environment variable containing a single string JSON with the contents of your datamodel. Please look at the `assets/datamodel.json` file as an example of how it has to be defined



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



## The origins as an example
I started to build a Water Leak Detector in this [GH repo](https://github.com/rmorillo24/WaterLeakDetector). I used many existing balenaBlocks that made my life much simpler, and then I realized that much of what I was doing could be converted into a block.
The Water Leak Detector 's only logic is to see if there's a leak. All the readings, publishing, graphing, storage, etc are blocks.


## Acknowledgments
Some inspiration on:
* [modbus2mqtt](https://github.com/Instathings/modbus2mqtt)
* [modbus-herdsman-converters](https://github.com/Instathings/modbus-herdsman-converters)
