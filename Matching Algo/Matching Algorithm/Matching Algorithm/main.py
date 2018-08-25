from match import *
#from database import load_preferences_from_db, write_matches_to_db
import sys


def main(n, m, pref_file=None):
    db = False
    if pref_file:
        preferences = load_preferences(pref_file)
        if preferences is None:
            sys.exit()
        teachers, openings = preferences
        print "Loaded actors from file"
    else:
        db = True
        teachers, openings = load_preferences_from_db()
        print "Loaded actors from database"
    matcher = Matcher(teachers, openings)

    print ""
    print "Matching...",
    matcher.multi_match(n, m)
    print "complete"

    for actor in teachers + openings:
        print actor

    if db:
        write_matches_to_db(teachers)

if __name__ == '__main__':

    n = 5
    m = 5
    prefs = "t1.preferences"

    main(n, m, prefs)
