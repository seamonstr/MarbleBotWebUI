# Manages the reference data for the web page.  
# THe reference data is two dicts:
# * stories: a story-name to chute-index map
# * people: a map of person-name to (hopper-index, picture path) tuple

DATA_FILE='var/data.py'

STORIES_KEY = 'stories'
PEOPLE_KEY = 'people'

_stories = None
_people = None

def init():
    data = {}
    execfile(DATA_FILE, data)
    if STORIES_KEY not in data.keys() or PEOPLE_KEY not in data.keys():
        raise Exception("Stories or data not found in data.py!")

    global _stories, _people
    _stories = data[STORIES_KEY]
    _people = data[PEOPLE_KEY]

def getPeople():
    return _people

def getStories():
    return _stories
    
# Main bit...
# Load the lookup data
init()
