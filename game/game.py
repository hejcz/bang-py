from game.queue import Queue

# contains all events that players must do
eventsQueue = Queue()
while eventsQueue.peek() is not None:
    nextEvent = eventsQueue.poll()


