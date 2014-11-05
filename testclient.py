import zmq

from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from tinyrpc import RPCClient
import numpy as np
import time

ctx = zmq.Context()

rpc_client = RPCClient(
    JSONRPCProtocol(),
    ZmqClientTransport.create(ctx, 'tcp://127.0.0.1:5002')
)

remote_server = rpc_client.get_proxy()

# call a method called 'reverse_string' with a single string argument


for voltage in np.linspace(0,30.0,100):
    value = voltage * 5.0/30.0
    result = remote_server.writeAnalogOutput(channel='Dev3/ao0',value=value)
    print "Server answered:", result
    time.sleep(0.1)