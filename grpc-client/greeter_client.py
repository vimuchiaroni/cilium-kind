# Copyright 2023 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""gRPC Python helloworld.Greeter client with keepAlive channel options."""

import logging
from time import sleep

import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import logging
import os
logging.basicConfig(level=logging.INFO,format="%(asctime)s;%(levelname)s;%(message)s")

server_url = os.environ.get('SERVER_URL', "localhost:50051")


def unary_call(
    stub: helloworld_pb2_grpc.GreeterStub, request_id: int, message: str
):
    logging.info(f"{server_url}")
    print("call:", request_id)
    try:
        response = stub.SayHello(helloworld_pb2.HelloRequest(name=message))
        logging.info(f"Greeter client received: {response.message}")
    except grpc.RpcError as rpc_error:
        logging.info("Call failed with code: ", rpc_error.code())


def run():
    """
    grpc.keepalive_time_ms: The period (in milliseconds) after which a keepalive ping is
        sent on the transport.
    grpc.keepalive_timeout_ms: The amount of time (in milliseconds) the sender of the keepalive
        ping waits for an acknowledgement. If it does not receive an acknowledgment within this
        time, it will close the connection.
    grpc.keepalive_permit_without_calls: If set to 1 (0 : false; 1 : true), allows keepalive
        pings to be sent even if there are no calls in flight.
    grpc.http2.max_pings_without_data: How many pings can the client send before needing to
        send a data/header frame.
    For more details, check: https://github.com/grpc/grpc/blob/master/doc/keepalive.md
    """
    channel_options = [
        ("grpc.keepalive_time_ms", 8000),
        ("grpc.keepalive_timeout_ms", 5000),
        ("grpc.http2.max_pings_without_data", 5),
        ("grpc.keepalive_permit_without_calls", 1),
    ]
    while True:
        with grpc.insecure_channel(
            target=server_url, options=channel_options
        ) as channel:
            stub = helloworld_pb2_grpc.GreeterStub(channel)
            # Should succeed
            # unary_call(stub, 3, "you")

            # Run 10s, run this with GRPC_VERBOSITY=DEBUG GRPC_TRACE=http_keepalive to observe logs.
            # Client will be closed after receveing GOAWAY from server.
            for i in range(10):
                unary_call(stub, i, "you")
                # logging.info(f"{i} seconds passed.")
                sleep(1)


if __name__ == "__main__":
    run()