class Actor(object):
    counter = 0

    def __init__(self, id=None, preferences=None):
        """
        Create an Actor
        Preferences: a list of the other type of Actor, strictly ordered by preferences
        For a certain type of Actor, all preferences lists must contain the same set of the other type
        """
        if id is None:
            Actor.counter += 1
            id = Actor.counter

        self.id = id
        self.preferences = preferences
        self.match = None

        # the matches we've made previously
        self.matches = set()

        # whether this Actor can be matched
        self.active = True

    def set_preferences(self, preferences):
        self.preferences = preferences

    def save_and_reset(self):
        """
        Save the match into the matches set, and reset internal state for reuse
        """
        self.matches.add(self.match)
        self.match = None

    def propose(self, proposal):
        """
        Propose to this Actor (proposal must be of the opposite type)
        Returns True if this Actor is preferred to the current match; False otherwise
        """
        if not self.active or proposal in self.matches:
            return False

        for actor in self.preferences:
            if actor is self.match:
                return False
            if actor is proposal:
                return True
        # it's not currently matched, but prefers it this way
        return False

    def __str__(self):
        return "<" + str(type(self))[15:-2] + "#" + str(self.id) + "; preferences: " + ",".join([str(p.id) for p in self.preferences]) + \
                "; matches: " + ",".join(map(lambda match: str(match.id), self.matches))


class Teacher(Actor):
    """
    Teachers are the proposing actors
    """
    def __init__(self, id=None, preferences=None):
        """
        Construct a Teacher
        """
        self.preference_index = 0
        super(Teacher, self).__init__(id, preferences)

    def get_next_preference(self):
        """
        Return the most-preferred Actor that hasn't been proposed to before
        """
        item = self.preferences[self.preference_index]
        self.preference_index += 1
        return item

    def has_more_preferences(self):
        """
        Returns True if this teacher has any other preferences (Openings preferred to being unmatched)
        or False otherwise
        """
        return self.active and self.preference_index < len(self.preferences)

    def save_and_reset(self):
        super(Teacher, self).save_and_reset()
        self.preference_index = 0


class Opening(Actor):
    """
    Openings are the Actors that are proposed to by teachers
    """
