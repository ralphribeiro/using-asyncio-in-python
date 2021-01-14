# Server code
import zmq
import itertools
import time


context = zmq.Context()
pusher = context.socket(zmq.PUSH)
pusher.bind("tcp://*:5557")

publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556")


for i in itertools.count():
    try:
        time.sleep(1)
        publisher.send_json(i)
        pusher.send_json(i)
    except KeyboardInterrupt:
        break
