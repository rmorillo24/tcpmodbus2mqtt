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

## How to try it 

The easiest way I've found to test this block is using Nodered as a modbus server, and a Python script that injects random values in the server so they can be read. The schema is simple...

![tcpmodbus2mqtt test setup](https://github.com/rmorillo24/tcpmodbus2mqtt/blob/main/assets/testSetup.png)

### Use NodeRed to simulate a TCP Modbus device
1. Install [Node Red](https://nodered.org/docs/getting-started/local) in the same LAN as your device
2. Install the MODBUS server for NodeRed, [node-red-contrib-modbus](https://flows.nodered.org/node/node-red-contrib-modbus)
3. Configure the server with your local IP address and a port of your election (eg. 10502)
4. Run `assets\randomModbusInjector.py` to populate your MODBUS simulator with data. First your will have to configure the IP address of the MODBUS server

### Use any MQTT broker to publish your messages
Any MQTT broker with a reachable IP address will work. 
For instance, you can install a mosquito broker in the same balena device adding the following service:

````
  mqtt:
    image: eclipse-mosquitto:1.6.15
    ports:
      - "1883:1883"
    restart: always  
````

### Create your balenaCloud fleet and add the device
1. Create a balenaCloud fleet. I you don't know how to, you can follow the [Getting Started](https://www.balena.io/docs/learn/getting-started/fincm3/python/) guide
2. Add to the docker-compose file containing the service as above
3. Configure the Device Variables in your app with the addresses and ports of the MODBUS and MQTT servers
4. Copy the contents of `assets\datamodel.json` into the `DATAMODEL_JSON` variable
5. You will be able to read the messages in your broker.
6. You may use the logs in the balenaCloud Dashboard to check if the `tcpmodbus2mqtt` service is connecting to the services and running



## The origins as an example
I started to build a Water Leak Detector in this [GH repo](https://github.com/rmorillo24/WaterLeakDetector). I used many existing balenaBlocks that made my life much simpler, and then I realized that much of what I was doing could be converted into a block.
The Water Leak Detector 's only logic is to see if there's a leak. All the readings, publishing, graphing, storage, etc are blocks.


## Acknowledgments
Some inspiration on:
* [modbus2mqtt](https://github.com/Instathings/modbus2mqtt)
* [modbus-herdsman-converters](https://github.com/Instathings/modbus-herdsman-converters)
