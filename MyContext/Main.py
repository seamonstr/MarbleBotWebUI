from WebKit.Page import Page
import os
from marbleui import LookupData
from marblebot import botthread

class Main(Page):

    def title(self):
        return 'My Sample Context'

    def writeContent(self):
        # Add the lookup data to the request and forward to the PSP.
        if botthread.marbleBot().running():
            self.request().botError = None
        else:
            self.request().botError = botthread.marbleBot().error()
        self.request().people = LookupData.getPeople()
        self.request().stories = LookupData.getStories()
        self.forward('Main.psp')
        
