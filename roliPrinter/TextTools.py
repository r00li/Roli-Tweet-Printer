#
# Roli Tweet printer
# Written by Andrej Rolih, www.r00li.com
#

import html
import unicodedata
from unidecode import unidecode


def deEmojify(inputString):
    returnString = ""
    lastAdded = None

    for character in inputString:
        try:
            character.encode("ascii")
            returnString += character
            lastAdded = character
        except UnicodeEncodeError:
            replaced = unidecode(str(character))
            if replaced != '':
                returnString += replaced
            else:
                try:
                    toAdd = "[" + unicodedata.name(character) + "]"
                    if toAdd == lastAdded:
                        returnString += "[=]"
                    else:
                        returnString += toAdd
                        lastAdded = toAdd
                except ValueError:
                    returnString += "[x]"
                    lastAdded = "[x]"

    return returnString

def removeHTMLEscaping(inputString):
    return html.unescape(inputString)