# this file contains the main entrypoint to talking to the bot 
# over its serial link. This class is invoked from botthread.py, which is the 
# application's entrypoint.

from time import sleep
import serial
import sys
from time import sleep

class MarbleDropException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

BOT_HELLO = "Marblebot is go!"
BOT_ERROR = "ERROR: "
BOTCMD_MARBLE = "marble %d %d"
BOT_MARBLE_SUCCESS = "Marble dropped."

BOT_DEVICE = '/dev/ttyACM0'

class Marblebot:
    _err = None

    _errThrowInx = 0
    _serial = None

    def __init__(self):
        ''' Connect to the specified serial device.'''
        self._botIsGo = False 
        pass

    def readLine(self):
        line = self._serial.readline().strip()
        if len(line) > 0:
            print ">>bot:%s" % line  # Log all marblebot comms to the logfile
        return line

    def writeLine(self, line):
        self._serial.write(line)
        self._serial.write('\r')
        sleep(1)
        self._serial.readline() # get rid of the echo

    def connect(self):
        try:
            self._serial = serial.Serial(BOT_DEVICE, 9600, timeout = 1)
        except serial.SerialException as e:
            self._err = str(e)
            raise

        # Wait until it's ready...
        print ">> Waiting for the bot"
        while self.readLine().strip() != BOT_HELLO:
            sys.stdout.write(".")
            sys.stdout.flush()

    def dropMarble(self, hopper, chute):
        '''Tells the bot to move a marble from hopper to the chute 
        specified.  Blocks until finished.

        If a time out or an error occurs, throws a MarbleDropException.'''
        if self._err is not None:
            raise MarbleDropException("Bot has an issue; please correct "\
                                      "and reset first.")

        # Now call the drop command, wait for a confirmation.
        self.writeLine(BOTCMD_MARBLE % (hopper, chute))
        line = self.readLine()
        while line == "":
            line = self.readLine()
        try:
            print ">>>LIne read: " + line
            if line != BOT_MARBLE_SUCCESS:
                if len(line) < 7:
                    raise MarbleDropException("Bot has issues.  No error returned.")
                if line[0:7] == BOT_ERROR:
                    raise MarbleDropException("Bot has issues: %s" % line[7:])
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
        self._serial.close()
