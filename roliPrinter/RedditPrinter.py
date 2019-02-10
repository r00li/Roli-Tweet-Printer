#
# Roli Tweet printer
# Written by Andrej Rolih, www.r00li.com
#

import praw

import datetime

from Singleton import *
from TextTools import *
import PrinterManager
import MiniLogger
import SettingsManager


class RedditPrinter(Singleton):

    def __init__(self):
        self.clientId = None
        self.clientSecret = None
        self.refreshToken = None

        self.reddit = None
        self.scopes = ['identity','mysubreddits', 'privatemessages', 'read']
        self.userAgent = 'roliPrinter'

    def initialize(self):
        MiniLogger.MiniLogger().printLog("Reddit printer initializing...")

        self.clientId = SettingsManager.SettingsManager().redditClientId
        self.clientSecret = SettingsManager.SettingsManager().redditClientSecret
        self.refreshToken = SettingsManager.SettingsManager().redditRefreshToken

        if self.clientId is None or self.refreshToken is None:
            MiniLogger.MiniLogger().printLog("Cannot initialize Reddit - Missing refresh token or clientId")
            return

        try:
            self.reddit = praw.Reddit(client_id=self.clientId, client_secret=self.clientSecret, refresh_token=self.refreshToken, user_agent=self.userAgent)
        except Exception as e:
            MiniLogger.MiniLogger().printLog("Error initializing reddit: " + str(e))

        if len(self.reddit.auth.scopes()) == len(self.scopes):
            MiniLogger.MiniLogger().printLog("Reddit initialization success!")
        else:
            MiniLogger.MiniLogger().printLog("Reddit initialization FAILED - Scopes mismatch: " + str(self.reddit.auth.scopes()))

    def createNewAuthorizationRequest(self):
        if self.clientId is None:
            MiniLogger.MiniLogger().printLog("Cannot request Reddit auth URL - Missing clientId")
            return None

        try:
            self.reddit = praw.Reddit(client_id=self.clientId, client_secret=self.clientSecret, redirect_uri='http://localhost:8080', user_agent=self.userAgent)
            return str(self.reddit.auth.url(self.scopes, '...', 'permanent'))
        except:
            MiniLogger.MiniLogger().printLog("Request for reddit auth URL failed")
            return None

    def getRefreshTokenFromCode(self, code):
        if not self.reddit or not code:
            MiniLogger.MiniLogger().printLog("Cannot initialize with code - missing reddit instance or code")
            return None

        try:
            return self.reddit.auth.authorize(code)
        except:
            MiniLogger.MiniLogger().printLog("Couldn't get reddit access token")
            return None

    def printRedditCommentOrMessage(self, comment):
        dummyPos = PrinterManager.PrinterManager().getDummyPrinter()

        try:
            prettyDate = datetime.datetime.fromtimestamp(int(comment.created_utc)).strftime('%d.%m.%Y at %H:%M')
        except:
            prettyDate = ""

        try:
            subreddit = "r/" + comment.subreddit.display_name
        except:
            subreddit = "MESSAGE"

        try:
            title = comment.link_title
        except:
            title = comment.subject

        authorName = ""
        if comment is not None and comment.author is not None and comment.author.name is not None:
            authorName = str(comment.author.name)

        dummyPos.set(font=u"a", align=u'center', invert=True, height=2)
        dummyPos.text("             Reddit            \n")

        dummyPos.set(align=u'right', font=u"b")
        try:
            dummyPos.text(authorName)
        except:
            MiniLogger.MiniLogger().printLog("Getting reddit commenter name error")
        dummyPos.text("\n")
        dummyPos.text(subreddit)
        dummyPos.text("\n")
        dummyPos.text(prettyDate)
        dummyPos.text("\n\n")
        dummyPos.set(align=u'left', font=u"b")
        dummyPos.text(title)
        dummyPos.text("\n\n")
        dummyPos.set(align=u'left')
        dummyPos.text(removeHTMLEscaping(deEmojify(comment.body)))
        dummyPos.text("\n\n")

        dummyPos.set(align=u'center')
        dummyPos.text("-------------------------------\n")

        return dummyPos.output

    def printNewReddits(self):
        MiniLogger.MiniLogger().printLog("Getting latest reddits...")
        if self.reddit is None:
            MiniLogger.MiniLogger().printLog("No reddit instance to print reddits - aborting")
            return

        items = []

        try:
            lastItemRead = SettingsManager.SettingsManager().redditLastInboxItemRead
            if lastItemRead is None or len(lastItemRead) == 0:
                items = self.reddit.inbox.all(limit=1)
            else:
                items = self.reddit.inbox.all(limit=20, params={'before': lastItemRead}) # Weirdly enough the correct parameter is before not after since inbox seems to be returned in the wrong order
        except Exception as e:
            MiniLogger.MiniLogger().printLog("Error refreshing reddits: " + str(e))

        for item in reversed(list(items)):
            raw = self.printRedditCommentOrMessage(item)
            PrinterManager.PrinterManager().printRawData(raw)

            if type(item) is praw.models.Comment:
                lastId = "t1_" + item.id
            else:
                lastId = "t4_" + item.id

            SettingsManager.SettingsManager().redditLastInboxItemRead = lastId