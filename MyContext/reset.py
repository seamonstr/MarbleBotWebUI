# Handler for resetting the bot if it's gone wrong.
from WebKit.HTTPContent import HTTPContent
from marblebot import botthread

class reset(HTTPContent):
    def respondToGet(self, transaction):
        if botthread.marbleBot().running():
            err = "The bot seems fine. Reset using the button."
            self.response().sendError(400, err);
            self.response().write("400: %s" % err)
            self.endResponse()
        else:
            botthread.reset()
            self.sendRedirectAndEnd("Main")
