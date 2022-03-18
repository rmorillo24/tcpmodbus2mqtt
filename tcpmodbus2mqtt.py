import struct
import binascii
import time
import _thread
import os
import json
from collections import OrderedDict
from datetime import datetime

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

from pymodbus.client.sync import ModbusTcpClient
import paho.mqtt.client as mqtt

import logging


def init_servers(modbus_host, modbus_port, mqtt_ip, mqtt_port):
    """
    init_servers: Reads environment variables for MODBUS server and MQTT broker. Then, connects.
        I'm leaving some hardcoded values for testing
    """
    #Loading environment variables for configuring the modbus server
    try:
        modbus_host = os.environ['MODBUS_HOST_IP']
        modbus_port = os.environ['MODBUS_HOST_PORT']
    except:
        log.log(logging.WARNING, "MODBUS slave address variables harcoded.")
        #not exiting for testing purposes

    #Loading environment variables for configuring the mqtt broker
    try:
        mqtt_ip = os.environ['MQTT_BROKER_IP']
        mqtt_port = os.environ['MQTT_BROKER_PORT']
    except:
        log.warning("MQTT broker address variables harcoded.")
        #not exiting for testing purposes

    #Connecting to MODBUS server
    try:
        logging.info("Attempting to connect to MODBUS server " + modbus_host + ":" + modbus_port)
        modbusc.connect()
        logging.info("Connected")
    except Exception as e:
        print(e)
        log.fatal("Could not connect to MODBUS server. Exitting.")
        exit()

    #Connecting to mqtt broker
    try:
        logging.info("Attempting to connect to MQTT broker " + mqtt_ip + ":" + mqtt_port)
        mqttc.connect(mqtt_ip, int(mqtt_port))  # Connect to (broker, port, keepalive-time)
        logging.info("Connected")
    except:
        log.fatal("Could not connect to MQTT broker. Exitting")
        # exit()

     
def readInputRegisters(address, size, format):
    """
    readInputRegisters uses the modbus client object to read a holding register
    
    address: address of the register
        TODO: check with a serial modbus
    size: number of registers to read
    format: coding format of the read value
        TODO: implement the formatting. Right now, this parameter is not used

    """
    #Read input registers
    try:
        rr = modbusc.read_holding_registers(address,
                                            size,
                                            unit=1)
        assert(not rr.isError())     # test that we are not an error
        assert(rr.function_code < 0x80) # test that we are not an error
    except Exception as e:
        log.exception(e)
        raise Exception("Could not read holding_registers")

    # Decoding PYTHON FLOAT IEEE 754
    try:
        decoder = BinaryPayloadDecoder.fromRegisters(rr.registers,
                                                     Endian.Little,
                                                     Endian.Little)
        value = decoder.decode_32bit_float()
    except Exception as e:
        raise Exception("Could not decode read value")
    return value


def loop_read_register(name, address, size, polling_secs, format):
    """
    loop_read_register read the polling time configuration to poll the register value. Once it's read it publishes to the mqtt server

    name: name of the parameter
    address: register address
    size: number of registers
    format: coding format of the read value
    """
    error = False
    while( not error ):
        try:
            value = readInputRegisters(address, size, format)
            log.info("Read: " + name +  ":" + str(value))
            msg = mqttc.publish("sensors",
                                json.dumps( { name: value } )) 
            if not msg.is_published():
                raise(Exception("Message not published in mqtt broker"))
        except Exception as e:
            log.log (logging.CRITICAL, e)
            error = True #TO-REVIEW if we want to stop the loop only because one reading fails. Could it happen?
        time.sleep(polling_secs) # Waiting for next poll,


#########
# Configuring logger
logging.basicConfig()
log = logging.getLogger('main')
log.setLevel(logging.INFO)
log.propagate = False
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
log.addHandler(ch)


#########
# Setting modbus and mqtt servers with hardcoded default values
global mqttc
global modbusc
modbus_host = "192.168.1.132"
modbus_port = "10502"
mqtt_ip = "127.0.0.1"
mqtt_port = "1883"
modbusc = ModbusTcpClient(modbus_host, modbus_port)
mqttc = mqtt.Client("mqttbroker")  # Create instance of client with client ID “digitest”
init_servers(modbus_host, modbus_port, mqtt_ip, mqtt_port)

#########
# loading datamodel
try:
    with open('datamodel.json', 'r') as myfile:
        data = myfile.read()
    datamodel = json.loads(data)
except Exception as e:
    log.fatal(e)
    log.fatal("Could not parse datamodel file. Exitting.")
    exit()


#########
# Looping datamodel to spawn a loop for each parameter
for key, value in datamodel['fromModbus']['input'].items():
    try:
        log.info("Launching process to read %s from address %s, length %s, polling time:%s, format: %s" %(key, value['address'], value['length'], value['polling_secs'], value['format']))
        _thread.start_new_thread( 
            loop_read_register, (key, 
                                 value['address'],
                                 value['length'],
                                 value['polling_secs'],
                                 value['format']) )
    except Exception as e:
        log.exception("Could not start process to read")
        log.exception(e)



while(1):
    pass # to enable threads working

