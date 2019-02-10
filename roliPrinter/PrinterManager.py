#
# Roli Tweet printer
# Written by Andrej Rolih, www.r00li.com
#

from Singleton import *
import SettingsManager
import MiniLogger

try:
    from escpos import *
except:
    MiniLogger.MiniLogger().printLog("Could not import escpos package. Testing only!")


class PrinterManager(Singleton):

    def __init__(self):
        self.pos = None

    def setupPrinter(self):
        MiniLogger.MiniLogger().printLog("Setting up printer")
        try:
            self.pos = printer.Usb(SettingsManager.SettingsManager().printerUSBPid,
                          SettingsManager.SettingsManager().printerUSBVid)
            MiniLogger.MiniLogger().printLog("Printer ready")
        except:
            MiniLogger.MiniLogger().printLog("Could not initialize printer! Check your USB PID and VID values")

    def printRawData(self, data):
        try:
            self.pos._raw(data)
            return True
        except:
            MiniLogger.MiniLogger().printLog("Printing error, setting up printer again")
            self.setupPrinter()

            return False

    def getDummyPrinter(self):
        return printer.Dummy()