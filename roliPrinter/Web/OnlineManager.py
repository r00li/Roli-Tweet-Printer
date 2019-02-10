#
# Roli Tweet printer
# Written by Andrej Rolih, www.r00li.com
#

import cherrypy
from cherrypy.lib import auth_digest
import threading
import random
import string
import os

import SettingsManager
from Singleton import *
import Web.ServerMethods


class OnlineManager(Singleton):

    def __init__(self):
        self.authUsers = {SettingsManager.SettingsManager().settingsUsername : SettingsManager.SettingsManager().settingsPassword}
        self.authKey = None

        cherrypy.config.update({'server.socket_port': 8080, 'server.socket_host': '0.0.0.0'})

    def startWebServer(self):
        self.webServerThread = threading.Thread(None, self.__webServerThread, "webServerThread")
        self.webServerThread.start()

    def __webServerThread(self):
        """ Sets up the web server. - configures paths and connects them to correct objects. """

        conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.staticdir.root': os.path.abspath(os.path.join(os.getcwd(), "Web", "public")),
                'tools.__secureheaders.on': True,

                'tools.auth_digest.on': True,
                'tools.auth_digest.realm': 'localhost',
                'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(self.authUsers),
                'tools.auth_digest.key': self.__setupKey(),
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './static',
            }
        }

        api_conf = {
            '/': {
                'tools.auth_digest.on': True,
                'tools.auth_digest.realm': 'localhost',
                'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(self.authUsers),
                'tools.auth_digest.key': self.__setupKey(),
                'tools.__secureheaders.on': True,
            },
            '/settings': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
            },
            '/systemLog': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
            },
            '/twitterFollow': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
            },
            '/twitterModifyUser': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
            },
            '/twitterPrintTweetWithId': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
            },
            '/twitterSaveSettings': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
            },
            '/note': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
            },
            '/redditSaveSettings': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
            },
            '/redditGetAuthorization': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
            },
            '/redditGetRefreshToken': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
            }
        }

        api = Web.ServerMethods.APIMethods()
        api.settings = Web.ServerMethods.SettingsList()
        api.twitterFollow = Web.ServerMethods.FollowTwitterUser()
        api.twitterModifyUser = Web.ServerMethods.ModifyTwitterUser()
        api.twitterPrintTweetWithId = Web.ServerMethods.PrintTweetWithId()
        api.twitterSaveSettings = Web.ServerMethods.SaveTwitterSettings()
        api.systemLog = Web.ServerMethods.SystemLog()
        api.note = Web.ServerMethods.PrintNote()
        api.redditSaveSettings = Web.ServerMethods.SaveRedditSettings()
        api.redditGetAuthorization = Web.ServerMethods.GetRedditAuthorization()
        api.redditGetRefreshToken = Web.ServerMethods.GetRedditRefreshTokenWithCode()

        cherrypy.tree.mount(Web.ServerMethods.ServerMethods(), '/', config=conf)
        cherrypy.tree.mount(api, '/api', config=api_conf)

        cherrypy.log.screen = None

        cherrypy.engine.start()
        cherrypy.engine.block()

    def __setupKey(self):
        """ Return previously generated key for digest auth or generates a new key and returns it if one does not exist """
        if self.authKey is None:
            self.authKey = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))

        return self.authKey


@cherrypy.tools.register('before_finalize', priority=60)
def __secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"