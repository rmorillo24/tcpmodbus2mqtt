from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
from collections import OrderedDict
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder

import numpy as np    
import os
import time

ORDER_DICT = {
    "<": "LITTLE",
    ">": "BIG"
}

client = ModbusClient('192.168.1.132', port=10502)
client.connect()

print("Starting random positive floats injector")

while(1):
    print("-" * 40)
    #IEEE745 for instant flow
    my_random = np.random.uniform(0, 1000)
    builder = BinaryPayloadBuilder(byteorder=Endian.Little,
                                    wordorder=Endian.Little)
    builder.add_32bit_float(my_random)
    payload = builder.to_registers()
    print("Instant float: %s -> %s" % (my_random,payload))
    payload = builder.build()
    address = 1
    #Writing into the slave
    client.write_registers(address, payload, skip_encode=True, unit=1)

    #float for daily accumulated flow
    my_random = np.random.uniform(0, 1000)
    builder = BinaryPayloadBuilder(byteorder=Endian.Little,
                                    wordorder=Endian.Little)
    builder.add_32bit_float(my_random)
    payload = builder.to_registers()
    print("daily accumulated: %s -> %s" % (my_random,payload))
    payload = builder.build()
    address = 137
    #Writing into the slave
    client.write_registers(address, payload, skip_encode=True, unit=1)

    #float for monthly accumulated flow
    my_random = np.random.uniform(0, 1000)
    builder = BinaryPayloadBuilder(byteorder=Endian.Little,
                                    wordorder=Endian.Little)
    builder.add_32bit_float(my_random)
    payload = builder.to_registers()
    print("monthly accumulated: %s -> %s" % (my_random,payload))
    payload = builder.build()
    address = 141
    #Writing into the slave
    client.write_registers(address, payload, skip_encode=True, unit=1)
    
    #IEEE745 for test
    my_random = 361
    builder = BinaryPayloadBuilder(byteorder=Endian.Little,
                                    wordorder=Endian.Little)
    builder.add_32bit_float(my_random)
    payload = builder.to_registers()
    print("Test: %s -> %s" % (my_random,payload))
    payload = builder.build()
    address = 361
    #Writing into the slave
    client.write_registers(address, payload, skip_encode=True, unit=1)


    time.sleep(25)


