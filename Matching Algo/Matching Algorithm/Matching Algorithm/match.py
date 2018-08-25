from Actors import Teacher, Opening
import random


class Matcher:
    # TODO this shouldn't take teachers and openings, but preferences
    def __init__(self, teachers, openings):
        # TODO comment
        self.teachers = teachers
        self.openings = openings

        self.actors = teachers + openings

        self.enable_actors()

    def enable_actors(self):
        """
        Enable all actors in this scenario
        Disable all actors that are referenced but not in this scenario
        """
        for actor in self.actors:
            for pref in actor.preferences:
                pref.active = False
        for actor in self.actors:
            actor.active = True

    def save_matches(self, n, m):
        """
        Saves the matches of the actors into their match objects
        Resets actors to prepare for another match
        Args:
            n: the number of matches for each teacher
            m: the number of matches for each opening
        Returns True if we have reached termination, False otherwise
        """
        no_matches = True
        all_inactive = True

        for actor in self.actors:
            if actor.match is not None:
                actor.save_and_reset()
                no_matches = False

            if (type(actor) is Teacher and len(actor.matches) == n) or \
               (type(actor) is Opening and len(actor.matches) == m):
                    actor.active = False
            else:
                all_inactive = False

        # we are done if no one matched or all actors have been marked inactive
        return no_matches or all_inactive

    def stable_match(self):
        """
        Teacher proposing deferred acceptance algorithm
        """
        all_matched = False
        while not all_matched:
            all_matched = True
            for teacher in self.teachers:
                while teacher.match is None and teacher.has_more_preferences():
                    # get top preference that hasn't been proposed to yet
                    opening = teacher.get_next_preference()
                    # propose
                    if opening.propose(teacher):
                        # we tentatively matched
                        if opening.match is not None:
                            # we replaced a different teacher
                            all_matched = False
                            # set the old teacher's match to None
                            opening.match.match = None

                        teacher.match = opening
                        opening.match = teacher

    def multi_match(self, n, m):
        """
        Create a multi-match between teachers and openings such that each opening will
        have n matches, or prefers not having a match to any of its additional options.
        """
        done = False
        while not done:
            self.stable_match()
            done = self.save_matches(n, m)

    def check_stable(self):
        """
        Match: a list of tuples of (opening, teacher)
        Returns True if the match is stable, False otherwise
        """
        # naive brute-force approach
        # ensure that every pair is happy
        for teacher in self.teachers:
            if teacher.active is False:
                continue
            for opening in self.openings:
                if opening.active is False:
                    continue
                if teacher.match is opening and opening.match is teacher:
                    continue
                if teacher.propose(opening) and opening.propose(teacher):
                    # both prefer the other to their current match
                    return False
        return True

    def __str__(self):
        return "\n".join(map(str, self.actors))


def generate_random_actors(n_teachers, n_openings):
    """
    Generates n_teachers teachers and n_openings openings, and assigns them random
    preference orderings.
    """
    teachers = [Teacher() for _ in xrange(n_teachers)]
    openings = [Opening() for _ in xrange(n_openings)]

    for opening in openings:
        opening.set_preferences(random.sample(teachers, n_teachers))
    for teacher in teachers:
        teacher.set_preferences(random.sample(openings, n_openings))

    return teachers, openings


def load_preferences(preference_file):
    def get_line(generator):
        line = generator.next().strip()
        if len(line) > 0 and line[0] == "#":
            return get_line(generator)
        if "|" in line:
            raise KeyError
        return [] if len(line) == 0 else line.split(" ")

    def get_teacher_pref_line(generator):
        """
        Returns two lists, one that occured before a '|' and one after
        If no pipe, all elements are assumed to be part of the first list
        """
        line = generator.next().strip()
        if len(line) > 0 and line[0] == "#":
            return get_teacher_pref_line(generator)
        pieces = [piece.strip() for piece in line.split("|")]
        if len(pieces) > 2:
            raise KeyError
        pieces = map(lambda x: [] if len(x) == 0 else x.split(" "), pieces)
        if len(pieces) == 1:
            pieces.append([])
        return pieces

    try:
        with open(preference_file) as file:
            teacher_names = get_line(file)
            opening_names = get_line(file)

            teachers = {name: Teacher(name) for name in teacher_names}
            openings = {name: Opening(name) for name in opening_names}

            for teacher_name in teacher_names:
                prefs, others = get_teacher_pref_line(file)
                prefs = [openings[name] for name in prefs]
                others = [openings[name] for name in others]
                random.shuffle(others)
                teachers[teacher_name].set_preferences(prefs + others)

            for opening_name in opening_names:
                prefs = get_line(file)
                prefs = [teachers[name] for name in prefs]
                others = [teacher for teacher in teachers.values() if teacher not in prefs]
                random.shuffle(others)
                openings[opening_name].set_preferences(prefs + others)
        return teachers.values(), openings.values()
    except KeyError:
        print "File Malformed!"
    except IOError:
        raise
        print "Unable to properly read file!"
    except StopIteration:
        print "Unexpected end of file!"
