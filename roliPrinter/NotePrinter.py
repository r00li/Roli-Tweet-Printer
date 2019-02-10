#
# Roli Tweet printer
# Written by Andrej Rolih, www.r00li.com
#

import datetime

from TextTools import *
import PrinterManager
import MiniLogger
from Singleton import *


class NotePrinter(Singleton):

    def __init__(self):
        pass

    def printNote(self, note = None, qrData=None):
        dummyPos = PrinterManager.PrinterManager().getDummyPrinter()

        try:
            prettyDate = datetime.datetime.now().strftime('%d.%m.%Y at %H:%M')
        except:
            prettyDate = ""

        dummyPos.set(font=u"a", align=u'center', invert=True, height=2)
        dummyPos.text("             Note              \n")

        dummyPos.set(align=u'right', font=u"b")
        dummyPos.text(prettyDate)
        dummyPos.text("\n\n")

        dummyPos.set(align=u'left')

        if note is not None and len(note) > 0:
            dummyPos.text(removeHTMLEscaping(deEmojify(note)))
            dummyPos.text("\n\n")

        if qrData is not None and len(qrData) > 0:
            dummyPos.qr(qrData, ec=3, size=5)
            dummyPos.text("\n\n")

        dummyPos.set(align=u'center')
        dummyPos.text("-------------------------------\n")

        PrinterManager.PrinterManager().printRawData(dummyPos.output)