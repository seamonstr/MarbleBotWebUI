
from WebKit.Page import Page
import os

class Main(Page):

    def title(self):
        return 'My Sample Context'

    def writeContent(self):
        self.writeln('<h1>Welcome to Webware for Python!</h1>')
        self.writeln('''
        <p>This is a sample context generated for you and has purposly been kept
        very simple to give you something to play with to get yourself started.
        The code that implements this page is located in <b>%s</b>.</p>
        ''' % self.request().serverSidePath())
        self.writeln("Current directory is: %s" % os.getcwd())
        self.writeln('''
        <p>There are more examples and documentation in the Webware distribution,
        which you can get to from here:</p>
        <ul>
        ''')
        servletPath = self.request().servletPath()
        contextName = self.request().contextName()
        for ctx in sorted(self.application().contexts()):
            if ctx in ('default', contextName) or '/' in ctx:
                continue
            self.writeln('<li><a href="%s/%s/">%s</a></li>'
                % (servletPath, ctx, ctx))
        self.writeln('</ul>')
