#
# Roli Tweet printer
# Written by Andrej Rolih, www.r00li.com
#

import twitter
import requests

import time
import datetime
from itertools import zip_longest
from enum import Enum
from PIL import Image
from io import BytesIO

from Singleton import *
from TextTools import *
import PrinterManager
import MiniLogger
import SettingsManager


class TweetHeader(Enum):
    normal = 0
    reply = 1
    quote = 2


class TweetPrinter(Singleton):

    def __init__(self):
        self.peopleFollowed = []
        self.twitterApi = None

        self.twitterAccessTokenKey = None
        self.twitterAccessTokenSecret = None
        self.twitterConsumerKey = None
        self.twitterConsumerSecret = None

    def initialize(self):
        MiniLogger.MiniLogger().printLog("Tweet printer initializing...")

        self.peopleFollowed = SettingsManager.SettingsManager().twitterFollowing

        self.twitterConsumerKey = SettingsManager.SettingsManager().twitterConsumerKey
        self.twitterConsumerSecret = SettingsManager.SettingsManager().twitterConsumerSecret
        self.twitterAccessTokenKey = SettingsManager.SettingsManager().twitterAccessTokenKey
        self.twitterAccessTokenSecret = SettingsManager.SettingsManager().twitterAccessTokenSecret

        if self.twitterConsumerKey is not None and self.twitterConsumerSecret is not None and self.twitterAccessTokenKey is not None and self.twitterAccessTokenSecret is not None:
            self.twitterApi = twitter.Api(consumer_key=self.twitterConsumerKey,
                                          consumer_secret=self.twitterConsumerSecret,
                                          access_token_key=self.twitterAccessTokenKey,
                                          access_token_secret=self.twitterAccessTokenSecret,
                                          sleep_on_rate_limit=True)

            twitterUser = None
            try:
                twitterUser = self.twitterApi.VerifyCredentials()
            except:
                twitterUser = None

            if twitterUser is not None:
                MiniLogger.MiniLogger().printLog("Tweet printer initialized")
            else:
                MiniLogger.MiniLogger().printLog("Failed to initialize Tweet printer - invalid credentials")
        else:
            self.twitterApi = None
            MiniLogger.MiniLogger().printLog("Failed to initialize Tweet printer - missing data!")

    def resizeImage(self, img, newWidth, newHWidth=200):
        #wpercent = (newWidth / float(img.size[0]))
        #hsize = int((float(img.size[1]) * float(wpercent)))
        #img2 = img.resize((newWidth, hsize), PIL.Image.ANTIALIAS)

        size = (newWidth, newHWidth)
        img.thumbnail(size, Image.ANTIALIAS)

        return img

    def getImagesFromTweet(self, tweet):
        images = []

        if tweet.media is not None:
            for media in tweet.media:
                try:
                    response = requests.get(media.media_url)
                    img = Image.open(BytesIO(response.content))
                    newImg = self.resizeImage(img, 380)
                    images.append(newImg)
                except:
                    MiniLogger.MiniLogger().printLog("Failed downloading tweet image" + str(media.media_url))

        return images

    def grouper(self, n, iterable):
        # Collect data into fixed-length chunks or blocks
        # grouper(3, 'ABCDEFG') --> ABC DEF Gxx"
        # x indicates the fill value

        fillvalue = Image.new('RGB', (1, 1), color=(255, 255, 255))
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    def groupImages(self, allImages):
        returnImages = []
        for im1, im2 in self.grouper(2, allImages):
            images = [im1, im2]

            widths, heights = zip(*(i.size for i in images))

            total_width = sum(widths)
            max_height = max(heights)

            new_im = Image.new('RGB', (total_width, max_height), color=(255, 255, 255))

            x_offset = 0
            for im in images:
                new_im.paste(im, (x_offset, 0))
                x_offset += im.size[0]

            returnImages.append(new_im)
        return returnImages

    def printTweet(self, tweet, header = TweetHeader.normal):
        dummyPos = PrinterManager.PrinterManager().getDummyPrinter()

        try:
            prettyDate = datetime.datetime.fromtimestamp(int(tweet.created_at_in_seconds)).strftime('%d.%m.%Y at %H:%M')
        except:
            prettyDate = ""

        if tweet.full_text is not None and len(tweet.full_text) > 0:
            tweetText = tweet.full_text
        else:
            tweetText = tweet.text

        if header == TweetHeader.reply:
            dummyPos.set(font=u"a", align=u'center', invert=True, height=1)
            dummyPos.text("          Replying to          \n")
        elif header == TweetHeader.quote:
            dummyPos.set(font=u"a", align=u'center', invert=True, height=1)
            dummyPos.text("             Quote             \n")
        else:
            dummyPos.set(font=u"a", align=u'center', invert=True, height=2)
            dummyPos.text("             Tweet             \n")

        dummyPos.set(align=u'right', font=u"b")
        dummyPos.text(tweet.user.name)
        dummyPos.text("\n")
        dummyPos.text(prettyDate)
        dummyPos.text("\n\n")
        dummyPos.set(align=u'left')
        dummyPos.text(removeHTMLEscaping(deEmojify(tweetText)))
        dummyPos.text("\n\n")

        grouppedImages = self.groupImages(self.getImagesFromTweet(tweet))
        for image in grouppedImages:
            dummyPos.image(self.resizeImage(image,380))
            dummyPos.text("\n\n")

        dummyPos.set(align=u'center')
        dummyPos.text("-------------------------------\n")

        return dummyPos.output

    def printNewTweets(self):
        MiniLogger.MiniLogger().printLog("Getting latest twitter data...")

        if self.twitterApi is None:
            MiniLogger.MiniLogger().printLog("Twitter operation failed - No twitter API")
            return

        for following in self.peopleFollowed:
            tweets = None

            try:
                if following.lastPrintedTweetId is not None:
                    tweets = self.twitterApi.GetUserTimeline(screen_name=following.screenName, count=20, since_id=following.lastPrintedTweetId)
                else:
                    tweets = self.twitterApi.GetUserTimeline(screen_name=following.screenName, count=1)
            except Exception as e:
                MiniLogger.MiniLogger().printLog("Could not download twitter timeline")
                MiniLogger.MiniLogger().printLog(e)

            if tweets is not None:
                for tweet in reversed(tweets):
                    if following.isEnabled:
                        printed = self.printSingleTweetAndReplies(tweet)
                    else:
                        printed = True

                    if printed:
                        following.lastPrintedTweetId = tweet.id

    def downloadAndPrintTweetWithId(self, tweetId):
        if self.twitterApi is None:
            MiniLogger.MiniLogger().printLog("Twitter operation failed - No twitter API")
            return

        try:
            tweet = self.twitterApi.GetStatus(tweetId)
            self.printSingleTweetAndReplies(tweet)
        except:
            MiniLogger.MiniLogger().printLog("Error getting single twitter status")

    def printSingleTweetAndReplies(self, tweet):
        if self.twitterApi is None:
            MiniLogger.MiniLogger().printLog("Twitter operation failed - No twitter API")
            return

        output = self.printTweet(tweet)
        success = PrinterManager.PrinterManager().printRawData(output)

        if tweet.in_reply_to_status_id is not None and tweet.in_reply_to_user_id is not None and tweet.user.id is not None and tweet.in_reply_to_user_id != tweet.user.id:
            try:
                reply = self.twitterApi.GetStatus(tweet.in_reply_to_status_id)
                out = self.printTweet(reply, header=TweetHeader.reply)
                PrinterManager.PrinterManager().printRawData(out)
            except:
                MiniLogger.MiniLogger().printLog("Error getting single twitter status")

        if tweet.quoted_status is not None and tweet.user.id is not None and tweet.quoted_status.user is not None and tweet.quoted_status.user.id is not None and tweet.quoted_status.user.id != tweet.user.id:
            out = self.printTweet(tweet.quoted_status, header=TweetHeader.quote)
            PrinterManager.PrinterManager().printRawData(out)

        return success