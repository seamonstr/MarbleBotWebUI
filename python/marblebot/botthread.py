from threading import Thread
from time import sleep
import marblebot

# The serial device to use to talk to the bot
SERIAL_DEVICE="/dev/somethingorother"

class BotThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self._queue = queue
        self.daemon = True
        self._bot = marblebot.Marblebot(SERIAL_DEVICE)

    def run(self):
        try:
          while True:
              if len(self._queue) > 0:
                  try:
                      self._bot.dropMarble(_queue[0][0], _queue[0][1])
                      # Only remove from the queue if this was successful (
                      # ie. didn't throw any exceptions.)
                      self._queue.remove(_queue[0])
                  except marblebot.MarbleDropException as e:
                      self._error = e.value
                      # Exit the while loop and exit the thread
                      break
        finally:
            _bot.disconnect()

class MarblebotThread:
   """A thread that manages a queue of marble drop operations. It processes
      any ops that come in; if any marble drop throws an error, the thread 
      exits and needs restarting.
   """
   _queue = []

   def start(self):
       """
       Start the thread.  asserts if the thread is already running.
       """
       self._botThread = BotThread(self._queue)
       self._botThread.start()

   def running(self):
       """ 
       Is the thread still running?
       """
       return self._botThread.isAlive()

   def error(self):
       """ 
       If the thread has exited, what was the reason?
       """
       assert not self.running()
       return self._botThread._error

   def dropMarble(self, chute, hopper):
       """
       Queue up a marble to be dropped - this is what the app
       uses to add a marble to the queue.  This class manages the 
       handing of these over to the bot as it gets around to them.
       """
       self._queue.append((chute, hopper))

   def queueLength(self):
       return len(self._queue)
