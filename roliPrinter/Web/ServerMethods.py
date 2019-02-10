#
# Roli Tweet printer
# Written by Andrej Rolih, www.r00li.com
#

import cherrypy
import SettingsManager
import MiniLogger
import NotePrinter
import RedditPrinter
import PrinterManager
import TweetPrinter
import json


class ServerMethods(object):

    @cherrypy.expose
    def index(self):
        return open('Web/public/index.html')

class APIMethods(object):

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPError(status=404, message="No API method specified")

class SettingsList(object):

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self):
        response = {}
        response["settings"] = SettingsManager.SettingsManager().toJSON()
        return response

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json

        usbVID = data["usbVID"]
        usbPID = data["usbPID"]

        if usbVID is not None:
            SettingsManager.SettingsManager().printerUSBVid = usbVID

        if usbPID is not None:
            SettingsManager.SettingsManager().printerUSBPid = usbPID

        SettingsManager.SettingsManager().toJSON(saveToFile=True)

        PrinterManager.PrinterManager().setupPrinter()

        return {"response": "ok"}

class FollowTwitterUser(object):

    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json

        if data['screenName'] is not None and len(data['screenName']) > 0:
            followed = SettingsManager.TwitterFollower(screenName=data['screenName'])
            SettingsManager.SettingsManager().twitterFollowing.append(followed)
            SettingsManager.SettingsManager().toJSON(saveToFile=True)

            return {"response": "ok"}
        else:
            raise cherrypy.HTTPError(status=430, message="Missing screen name")

class ModifyTwitterUser(object):

    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self, userIndex=''):

        data = cherrypy.request.json

        index = idToInt(userIndex)
        if index is not None and index >= 0 and index < len(SettingsManager.SettingsManager().twitterFollowing):
            if data['delete'] is not None and data['delete'] == True:
                print("Delete action received")

                del SettingsManager.SettingsManager().twitterFollowing[index]
                SettingsManager.SettingsManager().toJSON(saveToFile=True)

                return {"response": "ok"}
            else:
                print("Disable action receivd")

                SettingsManager.SettingsManager().twitterFollowing[index].isEnabled = not SettingsManager.SettingsManager().twitterFollowing[index].isEnabled
                SettingsManager.SettingsManager().toJSON(saveToFile=True)

                return {"response": "ok"}
        else:
            raise cherrypy.HTTPError(status=430, message="Missing or invalid id")

class PrintTweetWithId(object):

    exposed = True

    @cherrypy.tools.json_out()
    def POST(self, tweetId=''):

        tweet = idToInt(tweetId)
        if tweet is not None:
            TweetPrinter.TweetPrinter().downloadAndPrintTweetWithId(tweet)
        else:
            raise cherrypy.HTTPError(status=430, message="Missing or invalid id or tweet printer")

class SystemLog(object):

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self):
        return json.dumps(MiniLogger.MiniLogger().toJSONDict())

class PrintNote(object):

    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json

        note = data["note"]
        qrData = data["qrData"]
        if (note is not None and len(note) > 0) or (qrData is not None and len(qrData) > 0):
            NotePrinter.NotePrinter().printNote(note, qrData)
            return {"response": "ok"}
        else:
            raise cherrypy.HTTPError(status=430, message="Either a note or QR data (or both) must be specified.")

class SaveRedditSettings(object):

    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json

        clientId = data["redditClientId"]
        clientSecret = data["redditClientSecret"]
        refreshToken = data["redditRefreshToken"]

        if clientId is not None:
            SettingsManager.SettingsManager().redditClientId = clientId

        if clientSecret is not None:
            SettingsManager.SettingsManager().redditClientSecret = clientSecret

        if refreshToken is not None:
            SettingsManager.SettingsManager().redditRefreshToken = refreshToken

        SettingsManager.SettingsManager().toJSON(saveToFile=True)

        RedditPrinter.RedditPrinter().initialize()

        return {"response": "ok"}

class GetRedditAuthorization(object):

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self):
        authUrl = RedditPrinter.RedditPrinter().createNewAuthorizationRequest()

        if authUrl is not None and len(authUrl) > 0:
            return json.dumps({"authURL" : authUrl})
        else:
            raise cherrypy.HTTPError(status=430, message="Can't get reddit authorization URL. See log for details.")


class GetRedditRefreshTokenWithCode(object):
    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json

        code = data["code"]
        if code is None or len(code) == 0:
            raise cherrypy.HTTPError(status=430, message="Can't get refresh token. Missing authorization code")

        token = RedditPrinter.RedditPrinter().getRefreshTokenFromCode(code)

        if token is None or len(token) == 0:
            raise cherrypy.HTTPError(status=431, message="Getting refresh token failed. Check log for details.")
        else:
            SettingsManager.SettingsManager().redditRefreshToken = token
            SettingsManager.SettingsManager().toJSON(saveToFile=True)

            RedditPrinter.RedditPrinter().initialize()

            return {"response": "ok"}

class SaveTwitterSettings(object):

    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json

        accessToken = data["accessToken"]
        accessTokenSecret = data["accessTokenSecret"]
        consumerKey = data["consumerKey"]
        consumerSecret = data["consumerSecret"]

        if accessToken is not None and accessTokenSecret is not None and consumerKey is not None and consumerSecret is not None:
            SettingsManager.SettingsManager().twitterAccessTokenKey = accessToken
            SettingsManager.SettingsManager().twitterAccessTokenSecret = accessTokenSecret
            SettingsManager.SettingsManager().twitterConsumerKey = consumerKey
            SettingsManager.SettingsManager().twitterConsumerSecret = consumerSecret

            SettingsManager.SettingsManager().toJSON(saveToFile=True)

            TweetPrinter.TweetPrinter().initialize()

            return {"response": "ok"}
        else:
            raise cherrypy.HTTPError(status=430, message="Saving twitter settings failed - missing data")

def idToInt(inputId):

    outId = None
    if not len(str(inputId)):
        return outId

    try:
        outId = int(inputId)
    except:
        pass

    return outId
