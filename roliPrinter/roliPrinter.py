#
# Roli Tweet printer
# Written by Andrej Rolih, www.r00li.com
# Version 1.0
#

import PrinterManager
import time
import TweetPrinter
import RedditPrinter
import SettingsManager
import Web.OnlineManager
import MiniLogger


if __name__ == '__main__':
    MiniLogger.MiniLogger().printLog("Initializing...")

    SettingsManager.SettingsManager().fromJSON()

    PrinterManager.PrinterManager().setupPrinter()
    Web.OnlineManager.OnlineManager().startWebServer()

    TweetPrinter.TweetPrinter().initialize()
    RedditPrinter.RedditPrinter().initialize()

    MiniLogger.MiniLogger().printLog("Printer ready")

    while True:
        try:
            TweetPrinter.TweetPrinter().printNewTweets()
        except Exception as e:
            MiniLogger.MiniLogger().printLog("Tweet printer main loop exception... " + str(e) + "\n")

        try:
            RedditPrinter.RedditPrinter().printNewReddits()
        except Exception as e:
            MiniLogger.MiniLogger().printLog("Reddit printer main loop exception... " + str(e) + "\n")

        SettingsManager.SettingsManager().toJSON(saveToFile=True)
        time.sleep(120)

    MiniLogger.MiniLogger().printLog("The end")