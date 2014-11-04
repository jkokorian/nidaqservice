import zmq

from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from tinyrpc import RPCClient

ctx = zmq.Context()

rpc_client = RPCClient(
    JSONRPCProtocol(),
    ZmqClientTransport.create(ctx, 'tcp://127.0.0.1:5002')
)

remote_server = rpc_client.get_proxy()

# call a method called 'reverse_string' with a single string argument

for i in range(10):
    result = remote_server.writeAnalogOutput(channel='dev3/ao1',value=3.2)
    print "Server answered:", result