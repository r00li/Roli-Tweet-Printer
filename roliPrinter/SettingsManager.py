#
# Roli Tweet printer
# Written by Andrej Rolih, www.r00li.com
#

from Singleton import *
import MiniLogger
import json


class TwitterFollower:

    def __init__(self, screenName=None):
        self.screenName = screenName
        self.lastPrintedTweetId = None
        self.isEnabled = True

    def toDict(self):
        jsonDict = {}
        jsonDict['screenName'] = self.screenName
        jsonDict['lastPrintedTweetId'] = self.lastPrintedTweetId
        jsonDict['isEnabled'] = self.isEnabled

        return jsonDict

    def fromDict(self, jsonDict):
        self.screenName = jsonDict.get('screenName', self.screenName)
        self.lastPrintedTweetId = jsonDict.get('lastPrintedTweetId', self.lastPrintedTweetId)
        self.isEnabled = jsonDict.get('isEnabled', self.isEnabled)


class SettingsManager(Singleton):

    def __init__(self):
        # Global settings fields
        self.printerUSBPid = None
        self.printerUSBVid = None
        self.settingsUsername = "printer"
        self.settingsPassword = "printer"

        # Twitter fields
        self.twitterConsumerKey = ''
        self.twitterConsumerSecret = ''
        self.twitterAccessTokenKey = ''
        self.twitterAccessTokenSecret = ''

        self.twitterFollowing = []

        # Reddit fields
        self.redditClientId = None
        self.redditClientSecret = None
        self.redditRefreshToken = None
        self.redditLastInboxItemRead = None

    def toJSON(self, saveToFile=False):
        writeDict = {}

        globalDict = {}
        globalDict['printerUSBPid'] = self.printerUSBPid
        globalDict['printerUSBVid'] = self.printerUSBVid
        globalDict['settingsUsername'] = self.settingsUsername
        globalDict['settingsPassword'] = self.settingsPassword
        writeDict['global'] = globalDict

        twitterDict = {}
        twitterDict['twitterConsumerKey'] = self.twitterConsumerKey
        twitterDict['twitterConsumerSecret'] = self.twitterConsumerSecret
        twitterDict['twitterAccessTokenKey'] = self.twitterAccessTokenKey
        twitterDict['twitterAccessTokenSecret'] = self.twitterAccessTokenSecret

        followingArray = []
        for following in self.twitterFollowing:
            if hasattr(following, 'toDict'):
                followingArray.append(following.toDict())
        twitterDict['twitterFollowing'] = followingArray

        writeDict['twitter'] = twitterDict

        redditDict = {}
        redditDict['redditClientId'] = self.redditClientId
        redditDict['redditClientSecret'] = self.redditClientSecret
        redditDict['redditRefreshToken'] = self.redditRefreshToken
        redditDict['redditLastInboxItemRead'] = self.redditLastInboxItemRead
        writeDict['reddit'] = redditDict

        if saveToFile:
            try:
                with open('settings.json', 'w') as outfile:
                    json.dump(writeDict, outfile, indent=4)
            except:
                MiniLogger.MiniLogger().printLog("Could not save JSON to file!")

        return json.dumps(writeDict)

    def fromJSON(self, jsonString=None):
        readDict = {}

        if jsonString is None:
            try:
                with open('settings.json', 'r') as infile:
                    readDict = json.load(infile)
            except:
                MiniLogger.MiniLogger().printLog("Could not load JSON file!")
        else:
            readDict = json.loads(jsonString)

        globalDict = readDict.get('global')
        if globalDict is not None:
            self.printerUSBPid = globalDict.get('printerUSBPid',self.printerUSBPid)
            self.printerUSBVid = globalDict.get('printerUSBVid', self.printerUSBVid)
            self.settingsUsername = globalDict.get('settingsUsername', self.settingsUsername)
            self.settingsPassword = globalDict.get('settingsPassword', self.settingsPassword)

        twitterDict = readDict.get('twitter')
        if twitterDict is not None:
            self.twitterConsumerKey = twitterDict.get('twitterConsumerKey',self.twitterConsumerKey)
            self.twitterConsumerSecret = twitterDict.get('twitterConsumerSecret', self.twitterConsumerSecret)
            self.twitterAccessTokenKey = twitterDict.get('twitterAccessTokenKey', self.twitterAccessTokenKey)
            self.twitterAccessTokenSecret = twitterDict.get('twitterAccessTokenSecret', self.twitterAccessTokenSecret)

            followingArray = twitterDict.get('twitterFollowing', [])
            for following in followingArray:
                toAdd = TwitterFollower()
                toAdd.fromDict(following)
                self.twitterFollowing.append(toAdd)

        redditDict = readDict.get('reddit')
        if redditDict is not None:
            self.redditClientId = redditDict.get('redditClientId',self.redditClientId)
            self.redditClientSecret = redditDict.get('redditClientSecret', self.redditClientSecret)
            self.redditRefreshToken = redditDict.get('redditRefreshToken', self.redditRefreshToken)
            self.redditLastInboxItemRead = redditDict.get('redditLastInboxItemRead', self.redditLastInboxItemRead)