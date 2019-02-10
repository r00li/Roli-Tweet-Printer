#
# Roli Tweet printer
# Written by Andrej Rolih, www.r00li.com
#

from Singleton import *
import collections
import datetime

class MiniLogger(Singleton):

    def __init__(self):
        self.logQueue = collections.deque(maxlen=100)

    def printLog(self, string):
        print(datetime.datetime.now().strftime('%d.%m.%Y-%H:%M') + ": " + str(string))
        self.logQueue.appendleft(datetime.datetime.now().strftime('%d.%m.%Y-%H:%M') + ": " + str(string))

    def toJSONDict(self):
        logString = ""
        for entry in self.logQueue:
            logString += entry + "\n"

        return {"log" : logString}