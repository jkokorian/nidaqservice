import zmq

from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from tinyrpc import RPCClient
import numpy as np
import time
import argparse
import datetime
import dateutil

parser = argparse.ArgumentParser(prog="logAnalogInputs",
                        description="Calls a pydaqservice and reads the analog input values")
#parser.add_argument('channel', type=str, help='The physical output channel to write to')
parser.add_argument('endpoint', type=str,
                   help='The server address')

parser.add_argument('--outfile', dest='outfile', type=str, default=None,
                    help='A file to write the analog input values to (csv)')

parser.add_argument('--interval', dest='interval', type=int, default=1,
                    help="The time between samples in seconds")

args = parser.parse_args()


ctx = zmq.Context()

rpc_client = RPCClient(
    JSONRPCProtocol(),
    ZmqClientTransport.create(ctx, endpoint=args.endpoint)
)

remote_server = rpc_client.get_proxy()

# call a method called 'reverse_string' with a single string argument


channels=range(8)

if (args.outfile is not None):
    with file(args.outfile,'w') as f:
        f.write(",".join(["datetime"] + ["ai%i" % ch for ch in channels]) + "\n")

while True:
    results = []
    now = datetime.datetime.now()
    for ch in channels:
        value = remote_server.readAnalogInput(channel='Dev3/ai%i' % ch)
        results.append(value)
    
    csvString = ",".join(["%s" % value for value in ([now.strftime("%Y-%m-%d %H:%M:%S.%f")] + results)])
    print csvString
    if args.outfile is not None:    
        with file(args.outfile,'a') as f:        
            f.write(csvString + "\n")
        
    time.sleep(args.interval)