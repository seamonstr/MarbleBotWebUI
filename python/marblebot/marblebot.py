# this file contains the main entrypoint to talking to the bot 
# over its serial link. This class is invoked from botthread.py, which is the 
# application's entrypoint.

from time import sleep

class MarbleDropException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Marblebot:
    _err = None

    _errThrowInx = 0

    def __init__(self, device):
        ''' Connect to the specified serial device.'''
        self._botIsGo = False 
        pass

    def dropMarble(self, hopper, chute):
        '''Tells the bot to move a marble from hopper to the chute 
        specified.  Blocks until finished.

        If a time out or an error occurs, throws a MarbleDropException.'''
        
        print ">> thread: Dropping a marble."

        if self._err is not None:
            raise MarbleDropException("Bot has an issue; please correct "\
                                      "and reset first.")

        # If the bot isn't yet started, need to wait until it's ready...
        
        # Now call the drop command, wait for a confirmation.

        # None of this is yet implemented - so here's a dummy thing for the interim
        try:
            # Not yet implemented.  Just sleep for a bit.
            sleep(5)
            # Throw an error on the 5th time
            self._errThrowInx += 1
            if self._errThrowInx == 5:
                print ">> thread: throwing an error!"
                raise MarbleDropException("Error because the moon is in the "\
                                          "wrong quadrant!")
        except MarbleDropException as e:
            self._err = e.value
            raise

    def error(self):
        '''Return the last error returned by the bot.'''
        return self._err

    def reset(self):
        self._err = None

    def disconnect(self):
        ''' Disconnect from the serial port. '''
        pass
