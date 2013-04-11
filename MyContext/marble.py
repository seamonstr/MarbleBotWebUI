# Handler for the submission of a marble request
from WebKit.HTTPContent import HTTPContent
import os
from marbleui import LookupData
from marblebot import botthread

FIELD_PERSON = "person"
FIELD_STORY1 = "story1"
FIELD_STORY2 = "story2"

class MissingFieldException(Exception):
    pass

class marble(HTTPContent):
    def getField(self, tx, field):
        if not tx.request().hasField(field):
            raise MissingFieldException("%s not specified" % field)
        return tx.request().field(field)

    def respondToGet(self, transaction):
        err = None
        # Grab the inx for person, stories
        try:
            person = int(self.getField(transaction, FIELD_PERSON))
            story1 = int(self.getField(transaction, FIELD_STORY1))
            story2 = int(self.getField(transaction, FIELD_STORY2))
        except MissingFieldException as e:
            err = str(e)
        except ValueError as e:
            err = str(e)

        if err is None:
            # Check they're all in range
            if (person not in LookupData.getPeople().keys()) or \
               (story1 not in LookupData.getStories().keys()) or \
               (story2 not in LookupData.getStories().keys()):
                 err = "One of the supplied story or person values is not valid."

        # Return any error...
        if err is not None:
            self.response().sendError(400, err)
            self.response().write("400: %s" % err)
            self.endResponse()
        else:
            # let the bot know
            botthread.marbleBot().dropMarble(person, story1)
            botthread.marbleBot().dropMarble(person, story2)
            self.sendRedirectAndEnd("Main?grateful=lots")
