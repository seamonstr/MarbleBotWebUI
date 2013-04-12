from threading import Thread
from time import sleep
import marblebot

class BotThread(Thread):
    _error = None
    def __init__(self, queue):
        Thread.__init__(self)
        self._queue = queue
        self.daemon = True
        self._bot = marblebot.Marblebot()

    def run(self):
        print ">> thread: going"
        try:
            self._bot.connect()
            try:
                while True:
                    if len(self._queue) > 0:
                        self._bot.dropMarble(self._queue[0][0], self._queue[0][1])
                        # Only remove from the queue if this was successful
                        # (ie. didn't throw any exceptions.)
                        self._queue.remove(self._queue[0])
                        print ">> thread: queue count now %d." % len(self._queue)
                    else:
                        # Nothing in the queue - sleep
                        sleep(2)
            finally:
                self._bot.disconnect()
        except:
            self._error = self._bot.error()

class MarblebotThread:
   """A thread that manages a queue of marble drop operations. It processes
      any ops that come in; if any marble drop throws an error, the thread 
      exits and needs restarting.
   """
   _queue = []
   _botThread = None

   def start(self):
       """
       Start the thread.  asserts if the thread is already running.
       """
       assert self._botThread is None or not self.running(), \
           "Trying to start botthread when it's already running."

       self._botThread = BotThread(self._queue)
       self._botThread.start()
       print ">> Bot thread started."

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

def init():
    global _mblBotThread
    _mblBotThread = MarblebotThread()
    _mblBotThread.start()

# Called by the app once a person has fixed the issue.
def reset():
    _mblBotThread.start()

def marbleBot():
    return _mblBotThread

# Get the thread going...
init()

