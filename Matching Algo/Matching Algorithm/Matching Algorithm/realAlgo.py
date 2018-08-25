import numpy as np
males = [

]

females = [

]

candidates = [
    
]

employers = [
    
]


def removeExtras(preference_file1, preference_file2, preference_file3):

    candPrefs = np.loadtxt(preference_file1, dtype=int, delimiter=',')
    employerPrefs = np.loadtxt(preference_file2, dtype=int, delimiter=',')

    for i in range(len(employerPrefs)):
        appliedList = []
        for j in range(len(employerPrefs[i])):
            if (candPrefs[j][i] == 0):
                employerPrefs[i][j] = 0
            else:
                appliedList.append(employerPrefs[i][j])

        appliedList.sort()

        for j in range(len(appliedList)):
            for k in range(len(employerPrefs[i])):
                if (employerPrefs[i][k] == appliedList[j]):
                    employerPrefs[i][k] = j + 1

    np.savetxt(preference_file3, employerPrefs, fmt='%d', delimiter=",")

def convertDataFile(preference_file, outputFile):

    sparsePreferences = np.loadtxt(preference_file, dtype = int, delimiter = ",")

    pref = 1
    densePreferences = np.zeros((100,100), dtype = int)
    for i in range(len(sparsePreferences)):
        pref = 1
        maxPref = max(sparsePreferences[i])
        while(pref <= maxPref):
            for j in range(len(sparsePreferences[i])):
                if(sparsePreferences[i][j] == pref):
                    densePreferences[i][pref-1] = (j+1)
            pref+=1

    np.savetxt(outputFile, densePreferences, fmt='%d', delimiter=",")

def preservePrefs(preference_file1, preference_file2, outputFile):

    prefs = np.loadtxt(preference_file1, dtype=int, delimiter=',')
    oldPreferences = np.loadtxt(preference_file2, dtype=int, delimiter=',')

    newPreferences = prefs

    oldPrefsIndexList = []

    for i in range(len(oldPreferences)):
        tempIndexList = []
        for j in range(len(oldPreferences[i])):

            if (oldPreferences[i][j] == 0):
                break

            for k in range(len(prefs[i])):
                if (oldPreferences[i][j] == prefs[i][k]):
                    tempIndexList.append(k)
                    break

        tempIndexList.sort()
        oldPrefsIndexList.append(tempIndexList)

    for i in range(len(oldPrefsIndexList)):
        for j in range(len(oldPrefsIndexList[i])):
            newPreferences[i][oldPrefsIndexList[i][j]] = oldPreferences[i][j]

    print newPreferences[0]
    print oldPrefsIndexList[0]
    print oldPreferences[0]

    np.savetxt(outputFile, newPreferences, fmt='%d', delimiter=",")

def setUpInputFile(preference_file1, preference_file2, inputFile):

    candPrefs = np.loadtxt(preference_file1, dtype=int, delimiter=',')
    employerPrefs = np.loadtxt(preference_file2, dtype=int, delimiter=',')

    f = open(inputFile, 'w')

    for i in range(len(candPrefs)):
        f.write(str(i+1))
        f.write(" ")

    f.write("\n")

    for i in range(len(employerPrefs)):
        f.write("e")
        f.write(str(i+1))
        f.write(" ")

    f.write("\n")



    f.write("# Candidate Prefs\n")

    for cand in candPrefs:

        for pref in cand:
            if (pref != 0):
                f.write("e")
                f.write(str(pref))
                f.write(" ")
            else:
                break

        f.write("\n")


    f.write("# Employer Prefs\n")

    for employer in employerPrefs:

        for pref in employer:
            if (pref != 0):
                f.write(str(pref))
                f.write(" ")
            else:
                break

        f.write("\n")

    f.close()

# Parsing from match.py
def loadData(preference_file):
    def get_line(generator):
        line = generator.next().strip()
        if len(line) > 0 and line[0] == "#":
            return get_line(generator)
        if "|" in line:
            raise KeyError
        return [] if len(line) == 0 else line.split(" ")

    file = open(preference_file)

    teachers = get_line(file)
    openings = get_line(file)

    global candidates
    global employers

    for teacher in teachers:
        prefs = get_line(file)
        temp = { 'name':teacher, 'is_free':True, 'gender':'male', 'preferences':prefs, 'engaged_to':'', 'proposed_to':[] }
        males.append(temp)

        # Set up output dictionary
        candidates.append( { 'name':teacher, 'matches':[] } )



    for opening in openings:
        prefs = get_line(file)
        temp = { 'name':opening, 'is_free':True, 'gender':'female', 'preferences':prefs, 'engaged_to':'', 'proposed_to':[] }
        females.append(temp)

        # Set up output dictionary
        employers.append( { 'name':opening, 'matches':[] } )

    #print(teachers)
    #print(openings)
    for m in females:
        print(m)
    #print(females)


def break_engagement(person):
    breakingWith = is_engaged_to(person)
    for m in males:
        if m["name"] == person:
            if m["engaged_to"] != "":
                m["engaged_to"] = ""
                m["is_free"] = True
                print("{} is breaking with {}.".format(person, breakingWith))

    for f in females:
        if f["name"] == person:
            if f["engaged_to"] != "":
                f["engaged_to"] = ""
                m["is_free"] = True
                print("{} is breaking with {}.".format(person, breakingWith))


def is_engaged_to(person):
    for m in males:
        if m["name"] == person:
            return m["engaged_to"]

    for f in females:
        if f["name"] == person:
            return f["engaged_to"]

    return False


def is_engaged(person):
    for m in males:
        if m["name"] == person:
            if m["engaged_to"] != "":
                return True

    for f in females:
        if f["name"] == person:
            if f["engaged_to"] != "":
                return True

    return False


def who_do_you_love_more(person, candidate1, candidate2):
    for m in males:
        if m["name"] == person:
            for x in range(0, len(males)):
                if candidate1 == m["preferences"][x]:
                    return candidate1
                if candidate2 == m["preferences"][x]:
                    return candidate2

    for f in females:
        if f["name"] == person:
            for x in range(0, len(females)):
                if candidate1 == f["preferences"][x]:
                    return candidate1
                if candidate2 == f["preferences"][x]:
                    return candidate2


def engage(dramaKing, dramaQueen):
    for m in males:
        if m["name"] == dramaKing:
            m["engaged_to"] = dramaQueen
            m["is_free"] = False

    for f in females:
        if f["name"] == dramaQueen:
            f["engaged_to"] = dramaKing
            f["is_free"] = False


def get_name_from_ranking(dramaKing, rank):
    for m in males:
        if m["name"] == dramaKing:
            return m["preferences"][rank]


def main():
    count = 0
    while (True):
        
        # Termination Condition 1 (Max Attempts)

        #count+=1
        #print count
        #if (count > 1):
                    #print("\n\n\nMax Iter Reached!")
                    #print(count)
                    #return

        
        # Termination Condition 2 (No Breaks)
        noBreaks = True
                    
        good = 1
        for m in males:
            dramaKing = m["name"]
            if (m["is_free"] == False) and (len(m["proposed_to"]) != len(females)):
                good += 1
                if good == len(males):
                    print("\n\n\nSuccess!")
                    print(count)
                    return

            for x in range(0, len(m['preferences'])):
                if not is_engaged(dramaKing):
                    if x not in m["proposed_to"]:
                        m["proposed_to"].append(x)

                        woman = get_name_from_ranking(dramaKing, x)

                        if is_engaged(woman):
                            currentManOfTheEngaged = is_engaged_to(woman)

                            betterLover = who_do_you_love_more(
                                woman, currentManOfTheEngaged, dramaKing)

                            engage(betterLover, woman)

                            if betterLover != currentManOfTheEngaged:
                                break_engagement(currentManOfTheEngaged)

                                # Termination 2
                                noBreaks = False
                        else:
                            engage(dramaKing, woman)

        # Termination 2
        if (noBreaks):
            return


def happyend():
    print("Resolution:\n")
    for m in males:
        dramaKing = m["name"]
        dramaQueen = m["engaged_to"]

        print("{} <---> {}".format(dramaKing, dramaQueen))

        for candidate in candidates:
            if (candidate['name'] == dramaKing):
                candidate['matches'].append(dramaQueen)

    for f in females:
        dramaKing = f["engaged_to"]
        dramaQueen = f["name"]

        print("{} <---> {}".format(dramaQueen, dramaKing))

        for employer in employers:
            if (employer['name'] == dramaQueen):
                employer['matches'].append(dramaKing)

def removeTopMatch():

    global males
    global females

    newMaleGroup = []
    newFemaleGroup = []

    for m in males:
        try:
            m['preferences'].remove(m['engaged_to'])
        except ValueError:
            pass
        m['engaged_to'] = ''
        m['is_free'] = True
        m['proposed_to'] = []
        if (len(m['preferences']) == 0):
            for f in females:
                try:
                    f['preferences'].remove(m['name'])
                except ValueError:
                    pass
        else:
            newMaleGroup.append(m)

    for f in females:
        try:
            f['preferences'].remove(f['engaged_to'])
        except ValueError:
            pass

        f['engaged_to'] = ''
        f['is_free'] = True
        f['proposed_to'] = []
        if (len(f['preferences']) == 0):
            for m in males:
                try:
                    m['preferences'].remove(f['name'])
                except ValueError:
                    pass
        else:
            newFemaleGroup.append(f)

    males = newMaleGroup
    females = newFemaleGroup


def writeOutput():
    
    f = open('outputMatches.txt', 'w')

    for candidate in candidates:
        for match in candidate['matches']:
            if (match != ''):
                f.write(match)
                f.write(" ")
            else:
                f.write("-1")
                f.write(" ")
        f.write("\n")

    for employer in employers:
        for match in employer['matches']:
            if (match != ''):
                f.write(match)
                f.write(" ")
            else:
                f.write("-1")
                f.write(" ")
        f.write("\n")


    f.close()

def writeOutputToCSV(match_file1, match_file2, numRounds):

    candMatches = np.zeros( (len(candidates), numRounds), dtype='|S5' )
    employerMatches = np.zeros( (len(employers), numRounds), dtype='|S5' )

    for i, candidate in enumerate(candidates):
        tempIndex = 0
        for match in candidate['matches']:
            if (match != ''):
                candMatches[i][tempIndex] = match
                tempIndex += 1
            else:
                candMatches[i][tempIndex] = "-1"
                tempIndex += 1

    for i, employer in enumerate(employers):
        tempIndex = 0
        for match in employer['matches']:
            if (match != ''):
                employerMatches[i][tempIndex] = match
                tempIndex += 1
            else:
                employerMatches[i][tempIndex] = "-1"
                tempIndex += 1

    np.savetxt(match_file1, candMatches, fmt='%s', delimiter=",")
    np.savetxt(match_file2, employerMatches, fmt='%s', delimiter=",")



# Metrics

# Not used much
def calcStabilityMetrics(preference_file1, preference_file2, match_file1, match_file2):

    candPrefs = np.loadtxt(preference_file1, dtype='|S5', delimiter=',')
    employerPrefs = np.loadtxt(preference_file2, dtype='|S5', delimiter=',')
    candMatches = np.loadtxt(match_file1, dtype='|S5', delimiter=',')
    employerMatches = np.loadtxt(match_file2, dtype='|S5', delimiter=',')


    for i in range(len(candPrefs)):
        for j in range(len(candPrefs[i])):
            if (candPrefs[i][j] != '0'):
                candPrefs[i][j] = 'e' + candPrefs[i][j]
            else:
                candPrefs[i][j] = ''

    for i in range(len(employerPrefs)):
        for j in range(len(employerPrefs[i])):
            if (employerPrefs[i][j] == '0'):
                employerPrefs[i][j] = ''

    print candPrefs[0]
    print employerPrefs[0]
    print candMatches[0]
    print employerMatches[0]


    # Calculate Metric for Employer.

    # 100x100
    employerMetrics = np.zeros( (len(employerMatches)+2,len(employerMatches[0])+2) , dtype=float)

    # Count jobs for each displament distance for an employer. (e.g. 5 jobs were displaced by distance 3)
    for i in range(len(employerPrefs)):
        for j in range(len(employerPrefs[i])):
            if (employerPrefs[i][j] == ''):
                break
            for k in range(len(employerMatches[i])):
                if (employerPrefs[i][j] == employerMatches[i][k]):
                    distance = abs(k-j)
                    employerMetrics[i][distance] += 1

    # Calc total displacement & average for an employer
    for i in range(len(employerPrefs)):
        sum = 0.0
        for j in range(len(employerPrefs[i])):
            sum += j*employerMetrics[i][j]
        avg = sum/np.sum(employerMetrics[0])
        employerMetrics[i][len(employerMetrics)-2] = sum
        employerMetrics[i][len(employerMetrics)-1] = avg


    # Calc total jobs displacement per distance. (e.g. 500 jobs were displaced by distance 3.)
    # And calculate average (Only divide by the number of employers that are actually able to reach a certain displacement).
    for j in range(len(employerPrefs[0])):
        sum = 0.0
        count = 0
        for i in range(len(employerPrefs)):
            if (employerMatches[i][j] == ''):
                continue
            sum += employerMetrics[i][j]
            count += 1
        if (count == 0):
            break
        avg = sum/count
        employerMetrics[len(employerMetrics)-2][j] = sum
        employerMetrics[len(employerMetrics)-1][j] = avg


    np.savetxt('employerMetrics.csv', employerMetrics, fmt='%f', delimiter=',')

# Used for Normal DAA & LMF
def calcDisplacementMetrics(preference_file1, preference_file2, match_file1, match_file2, numberOfTopJobsToConsider, penalty):

    candPrefs = np.loadtxt(preference_file1, dtype='|S5', delimiter=',')
    employerPrefs = np.loadtxt(preference_file2, dtype='|S5', delimiter=',')
    candMatches = np.loadtxt(match_file1, dtype='|S5', delimiter=',')
    employerMatches = np.loadtxt(match_file2, dtype='|S5', delimiter=',')


    for i in range(len(candPrefs)):
        for j in range(len(candPrefs[i])):
            if (candPrefs[i][j] != '0'):
                candPrefs[i][j] = 'e' + candPrefs[i][j]
            else:
                candPrefs[i][j] = ''

    for i in range(len(employerPrefs)):
        for j in range(len(employerPrefs[i])):
            if (employerPrefs[i][j] == '0'):
                employerPrefs[i][j] = ''

    print candPrefs[0]
    print employerPrefs[0]
    print candMatches[0]
    print employerMatches[0]


    # Calculate Metric for Employer.

    # 100x100
    employerMetrics = np.zeros( (len(employerMatches)+4, numberOfTopJobsToConsider) , dtype=float)

    # Calc displacement for the first n matches

    for j in range(numberOfTopJobsToConsider):

        for i in range(len(employerMatches)):

            if (employerMatches[i][j] == '-1'):
                employerMetrics[i][j] = -1

            elif (employerMatches[i][j] == ''):
                employerMetrics[i][j] = -2

            else:

                # Calc penalty for no match

                totalPenalty = 0

                for k in range(j):
                    if (employerMatches[i][k] == '-1'):
                        totalPenalty += penalty


                for k in range(len(employerPrefs[i])):
                    if (employerMatches[i][j] == employerPrefs[i][k]):
                        distance = k
                        employerMetrics[i][j] = distance + totalPenalty

        sum = 0
        count = 0

        for i in range(len(employerMatches)):
            if (employerMetrics[i][j] != -1 and employerMetrics[i][j] != -2):
                sum += employerMetrics[i][j]
                count += 1

        employerMetrics[len(employerMetrics)-4][j] = sum
        employerMetrics[len(employerMetrics)-3][j] = sum/count

    # Count jobs that have no matches
    for j in range(numberOfTopJobsToConsider):
        total = 0.0
        noMatchCount = 0.0

        for i in range(len(employerMatches)):
            if (employerMatches[i][j] != ''):
                total += 1
            if (employerMatches[i][j] == '-1'):
                noMatchCount += 1

        if (total == 0):
            break

        else:
            employerMetrics[len(employerMetrics)-2][j] = noMatchCount
            employerMetrics[len(employerMetrics)-1][j] = (noMatchCount/total)*100

    np.savetxt('employerMetrics.csv', employerMetrics, fmt='%f', delimiter=',')


    # ------------------ #

    # Calculate Metric for Candidate.

    # 100x100
    candMetrics = np.zeros( (len(candMatches)+4, numberOfTopJobsToConsider) , dtype=float)

    # Calc displacement for the first n matches

    for j in range(numberOfTopJobsToConsider):

        for i in range(len(candMatches)):

            if (candMatches[i][j] == '-1'):
                candMetrics[i][j] = -1

            elif (candMatches[i][j] == ''):
                candMetrics[i][j] = -2

            else:

                # Calc penalty for no match

                totalPenalty = 0

                for k in range(j):
                    if (candMatches[i][k] == '-1'):
                        totalPenalty += penalty


                for k in range(len(candPrefs[i])):
                    if (candMatches[i][j] == candPrefs[i][k]):
                        distance = k
                        candMetrics[i][j] = distance + totalPenalty

        sum = 0
        count = 0

        for i in range(len(candMatches)):
            if (candMetrics[i][j] != -1 and candMetrics[i][j] != -2):
                sum += candMetrics[i][j]
                count += 1

        candMetrics[len(candMetrics)-4][j] = sum
        candMetrics[len(candMetrics)-3][j] = sum/count

    # Count jobs that have no matches
    for j in range(numberOfTopJobsToConsider):
        total = 0.0
        noMatchCount = 0.0

        for i in range(len(candMatches)):
            if (candMatches[i][j] != ''):
                total += 1
            if (candMatches[i][j] == '-1'):
                noMatchCount += 1

        if (total == 0):
            break

        else:
            candMetrics[len(candMetrics)-2][j] = noMatchCount
            candMetrics[len(candMetrics)-1][j] = (noMatchCount/total)*100

    np.savetxt('candMetrics.csv', candMetrics, fmt='%f', delimiter=',')

# Sets up data for Mixed Algo
def mixedAlgo(match_file1, match_file2, match_file3, match_file4):

    newCandMatches = np.loadtxt(match_file1, dtype='S5', delimiter=',')
    newEmployerMatches = np.loadtxt(match_file2, dtype='S5', delimiter=',')
    lmfCandMatches = np.loadtxt(match_file3, dtype='S5', delimiter=',')
    lmfEmployerMatches = np.loadtxt(match_file4, dtype='S5', delimiter=',')


    for j in range(len(newEmployerMatches[0])):
        for i in range(len(newEmployerMatches)):

            if (newEmployerMatches[i][j] == '-1'):

                for k in range(len(lmfEmployerMatches[i])):

                    newMatch = lmfEmployerMatches[i][k]

                    if (newMatch == '-1'):
                        continue

                    alreadyMatched = False

                    for x in range(len(newEmployerMatches)):

                        if (newEmployerMatches[x][j] == newMatch):
                            alreadyMatched = True
                            break

                    for x in range(j):

                        if (newEmployerMatches[i][x] == newMatch):
                            alreadyMatched = True
                            break

                    if (alreadyMatched == False):
                        newEmployerMatches[i][j] = newMatch
                        newCandMatches[int(newMatch)-1][j] = 'e' + str(i+1)
                        break

    np.savetxt('new_employer_matches.csv', newEmployerMatches, fmt='%s', delimiter=',')
    np.savetxt('new_candidate_matches.csv', newCandMatches, fmt='%s', delimiter=',')

# Used for Mixed
def calcDisplacementMixedMetrics(preference_file1, preference_file2, preference_file3, preference_file4, match_file1, match_file2, numberOfTopJobsToConsider, penalty):

    candPrefs = np.loadtxt(preference_file1, dtype='|S5', delimiter=',')
    employerPrefs = np.loadtxt(preference_file2, dtype='|S5', delimiter=',')
    lmfCandPrefs = np.loadtxt(preference_file3, dtype='|S5', delimiter=',')
    lmfEmployerPrefs = np.loadtxt(preference_file4, dtype='|S5', delimiter=',')
    candMatches = np.loadtxt(match_file1, dtype='|S5', delimiter=',')
    employerMatches = np.loadtxt(match_file2, dtype='|S5', delimiter=',')


    for i in range(len(candPrefs)):
        for j in range(len(candPrefs[i])):
            if (candPrefs[i][j] != '0'):
                candPrefs[i][j] = 'e' + candPrefs[i][j]
            else:
                candPrefs[i][j] = ''

    for i in range(len(employerPrefs)):
        for j in range(len(employerPrefs[i])):
            if (employerPrefs[i][j] == '0'):
                employerPrefs[i][j] = ''

    for i in range(len(lmfCandPrefs)):
        for j in range(len(lmfCandPrefs[i])):
            if (lmfCandPrefs[i][j] != '0'):
                lmfCandPrefs[i][j] = 'e' + lmfCandPrefs[i][j]
            else:
                lmfCandPrefs[i][j] = ''

    for i in range(len(lmfEmployerPrefs)):
        for j in range(len(lmfEmployerPrefs[i])):
            if (lmfEmployerPrefs[i][j] == '0'):
                lmfEmployerPrefs[i][j] = ''

    print candPrefs[0]
    print employerPrefs[0]
    print candMatches[0]
    print employerMatches[0]


    # Calculate Metric for Employer.

    # 100x100
    employerMetrics = np.zeros( (len(employerMatches)+4, numberOfTopJobsToConsider) , dtype=float)


    # Calc displacement for the first n matches

    for j in range(numberOfTopJobsToConsider):

        for i in range(len(employerMatches)):

            if (employerMatches[i][j] == '-1'):
                employerMetrics[i][j] = -1

            elif (employerMatches[i][j] == ''):
                employerMetrics[i][j] = -2

            else:

                # Calc penalty for no match

                totalPenalty = 0

                for k in range(j):
                    if (employerMatches[i][k] == '-1'):
                        totalPenalty += penalty

                found = False
                for k in range(len(employerPrefs[i])):
                    if (employerMatches[i][j] == employerPrefs[i][k]):
                        distance = k
                        employerMetrics[i][j] = distance + totalPenalty
                        found = True

                # Mixed
                if (found == False):
                    for k in range(len(lmfEmployerPrefs[i])):
                        if (employerMatches[i][j] == lmfEmployerPrefs[i][k]):
                            distance = k
                            employerMetrics[i][j] = distance/10 + totalPenalty
                            found = True


        sum = 0
        count = 0

        for i in range(len(employerMatches)):
            if (employerMetrics[i][j] != -1 and employerMetrics[i][j] != -2):
                sum += employerMetrics[i][j]
                count += 1

        employerMetrics[len(employerMetrics)-4][j] = sum
        employerMetrics[len(employerMetrics)-3][j] = sum/count

    # Count jobs that have no matches
    for j in range(numberOfTopJobsToConsider):
        total = 0.0
        noMatchCount = 0.0

        for i in range(len(employerMatches)):
            if (employerMatches[i][j] != ''):
                total += 1
            if (employerMatches[i][j] == '-1'):
                noMatchCount += 1

        if (total == 0):
            break

        else:
            employerMetrics[len(employerMetrics)-2][j] = noMatchCount
            employerMetrics[len(employerMetrics)-1][j] = (noMatchCount/total)*100

    np.savetxt('employerMetrics.csv', employerMetrics, fmt='%f', delimiter=',')



    # Calculate Metric for Candidate.

    # 100x100
    candMetrics = np.zeros( (len(candMatches)+4, numberOfTopJobsToConsider) , dtype=float)


    # Calc displacement for the first n matches

    for j in range(numberOfTopJobsToConsider):

        for i in range(len(candMatches)):

            if (candMatches[i][j] == '-1'):
                candMetrics[i][j] = -1

            elif (candMatches[i][j] == ''):
                candMetrics[i][j] = -2

            else:

                # Calc penalty for no match

                totalPenalty = 0

                for k in range(j):
                    if (candMatches[i][k] == '-1'):
                        totalPenalty += penalty

                found = False
                for k in range(len(candPrefs[i])):
                    if (candMatches[i][j] == candPrefs[i][k]):
                        distance = k
                        candMetrics[i][j] = distance + totalPenalty
                        found = True

                # Mixed
                if (found == False):
                    for k in range(len(lmfCandPrefs[i])):
                        if (candMatches[i][j] == lmfCandPrefs[i][k]):
                            distance = k
                            candMetrics[i][j] = distance/10 + totalPenalty
                            found = True


        sum = 0
        count = 0

        for i in range(len(candMatches)):
            if (candMetrics[i][j] != -1 and candMetrics[i][j] != -2):
                sum += candMetrics[i][j]
                count += 1

        candMetrics[len(candMetrics)-4][j] = sum
        candMetrics[len(candMetrics)-3][j] = sum/count

    # Count jobs that have no matches
    for j in range(numberOfTopJobsToConsider):
        total = 0.0
        noMatchCount = 0.0

        for i in range(len(candMatches)):
            if (candMatches[i][j] != ''):
                total += 1
            if (candMatches[i][j] == '-1'):
                noMatchCount += 1

        if (total == 0):
            break

        else:
            candMetrics[len(candMetrics)-2][j] = noMatchCount
            candMetrics[len(candMetrics)-1][j] = (noMatchCount/total)*100

    np.savetxt('candMetrics.csv', candMetrics, fmt='%f', delimiter=',')

# Used for Simulator
def calcSimulatorMetrics(preference_file1, preference_file2, match_file1, match_file2, numberOfTopJobsToConsider, penalty):

    candPrefs = np.loadtxt(preference_file1, dtype='|S5', delimiter=',')
    employerPrefs = np.loadtxt(preference_file2, dtype='|S5', delimiter=',')
    candMatches = np.loadtxt(match_file1, dtype='|S5', delimiter=',')
    employerMatches = np.loadtxt(match_file2, dtype='|S5', delimiter=',')


    for i in range(len(candPrefs)):
        for j in range(len(candPrefs[i])):
            if (candPrefs[i][j] != '0'):
                candPrefs[i][j] = 'e' + candPrefs[i][j]
            else:
                candPrefs[i][j] = ''

    for i in range(len(employerPrefs)):
        for j in range(len(employerPrefs[i])):
            if (employerPrefs[i][j] == '0'):
                employerPrefs[i][j] = ''

    print candPrefs[0]
    print employerPrefs[0]
    print candMatches[0]
    print employerMatches[0]


    # Calculate Metric for Employer.

    # 100x100
    employerMetrics = np.zeros( (len(employerMatches)+4, numberOfTopJobsToConsider) , dtype=float)



    # Calc displacement for the first n matches

    for j in range(numberOfTopJobsToConsider):

        for i in range(len(employerMatches)):

            if (employerMatches[i][j] == '-2'):
                employerMetrics[i][j] = -2
                continue

            if (employerMatches[i][j] == '-1'):
                employerMetrics[i][j] = -1

            elif (employerMatches[i][j] == ''):
                employerMetrics[i][j] = -2

            else:

                # Calc penalty for no match

                totalPenalty = 0

                for k in range(j):
                    if (employerMatches[i][k] == '-1'):
                        totalPenalty += penalty


                for k in range(len(employerPrefs[i])):
                    if (employerMatches[i][j] == employerPrefs[i][k]):
                        distance = k
                        employerMetrics[i][j] = distance + totalPenalty

        sum = 0
        count = 0

        for i in range(len(employerMatches)):
            if (employerMetrics[i][j] != -1 and employerMetrics[i][j] != -2):
                sum += employerMetrics[i][j]
                count += 1

        employerMetrics[len(employerMetrics)-4][j] = sum
        employerMetrics[len(employerMetrics)-3][j] = sum/count

    # Count jobs that have no matches
    for j in range(numberOfTopJobsToConsider):
        total = 0.0
        noMatchCount = 0.0

        for i in range(len(employerMatches)):
            if (employerMatches[i][j] != ''):
                total += 1
            if (employerMatches[i][j] == '-1'):
                noMatchCount += 1

        if (total == 0):
            break

        else:
            employerMetrics[len(employerMetrics)-2][j] = noMatchCount
            employerMetrics[len(employerMetrics)-1][j] = (noMatchCount/total)*100

    np.savetxt('employerMetrics.csv', employerMetrics, fmt='%f', delimiter=',')




    # Calculate Metric for Candidate.

    # 100x100
    candMetrics = np.zeros( (len(candMatches)+4, numberOfTopJobsToConsider) , dtype=float)

    # Calc displacement for the first n matches

    for j in range(numberOfTopJobsToConsider):

        for i in range(len(candMatches)):

            if (candMatches[i][j] == '-2'):
                candMetrics[i][j] = -2
                continue

            if (candMatches[i][j] == '-1'):
                candMetrics[i][j] = -1

            elif (candMatches[i][j] == ''):
                candMetrics[i][j] = -2

            else:

                # Calc penalty for no match

                totalPenalty = 0

                for k in range(j):
                    if (candMatches[i][k] == '-1'):
                        totalPenalty += penalty


                for k in range(len(candPrefs[i])):
                    if (candMatches[i][j] == candPrefs[i][k]):
                        distance = k
                        candMetrics[i][j] = distance + totalPenalty

        sum = 0
        count = 0

        for i in range(len(candMatches)):
            if (candMetrics[i][j] != -1 and candMetrics[i][j] != -2):
                sum += candMetrics[i][j]
                count += 1

        candMetrics[len(candMetrics)-4][j] = sum
        candMetrics[len(candMetrics)-3][j] = sum/count

    # Count jobs that have no matches
    for j in range(numberOfTopJobsToConsider):
        total = 0.0
        noMatchCount = 0.0

        for i in range(len(candMatches)):
            if (candMatches[i][j] != ''):
                total += 1
            if (candMatches[i][j] == '-1'):
                noMatchCount += 1

        if (total == 0):
            break

        else:
            candMetrics[len(candMetrics)-2][j] = noMatchCount
            candMetrics[len(candMetrics)-1][j] = (noMatchCount/total)*100

    np.savetxt('candMetrics.csv', candMetrics, fmt='%f', delimiter=',')

def realMain():

    # ----- Data Prep -----
    #removeExtras('candidate_preferences.csv', 'employer_preferences.csv', 'real_employer_prefs.csv')
    #return

    # ----- Data Prep -----
    #convertDataFile('candidate_preferences.csv', 'dense_candidate_prefs.csv')
    #convertDataFile('real_employer_prefs.csv', 'dense_employer_prefs.csv')
    #return

    # ----- Data Prep -----
    #setUpInputFile('dense_candidate_prefs.csv', 'dense_employer_prefs.csv', 'testInput.txt')
    #return

    # ----- Metrics for Normal DAA or LMF -----
    #calcStabilityMetrics('dense_candidate_prefs.csv', 'dense_employer_prefs.csv', 'candidate_matches.csv', 'employer_matches.csv')
    #calcDisplacementMetrics('dense_candidate_prefs.csv', 'dense_employer_prefs.csv', 'candidate_matches.csv', 'employer_matches.csv', 143, 10)
    #return

    # ----- LMF Preserve Data Prep -----
    #preservePrefs('dense_candidate_prefs.csv', 'dense_original_candidate_prefs.csv', 'dense_preserved_candidate_prefs.csv')
    #preservePrefs('dense_employer_prefs.csv', 'dense_original_employer_prefs.csv', 'dense_preserved_employer_prefs.csv')
    #return

    # ----- LMF Preserve Data Prep -----
    #setUpInputFile('dense_preserved_candidate_prefs.csv', 'dense_preserved_employer_prefs.csv', 'testInput.txt')
    #return

    # ----- Metrics for LMF Preserve -----
    #calcStabilityMetrics('dense_preserved_candidate_prefs.csv', 'dense_preserved_employer_prefs.csv', 'candidate_matches.csv', 'employer_matches.csv')
    #calcDisplacementMetrics('dense_preserved_candidate_prefs.csv', 'dense_preserved_employer_prefs.csv', 'candidate_matches.csv', 'employer_matches.csv', 142, 10)
    #return

    # ----- Mixed Algo, requires Normal and LMF matches -----
    #mixedAlgo('candidate_matches.csv', 'employer_matches.csv', 'lmf_candidate_matches.csv', 'lmf_employer_matches.csv')
    # ----- Metrics for Mixed Algo -----
    #calcDisplacementMixedMetrics('dense_candidate_prefs.csv', 'dense_employer_prefs.csv', 'lmf_dense_candidate_prefs.csv', 'lmf_dense_employer_prefs.csv', 'new_candidate_matches.csv', 'new_employer_matches.csv', 18, 10)
    #return

    loadData('testInput2.txt')
    main()
    happyend()

    matchCount = 1

    while(True):
        removeTopMatch()

        if(len(males) == 0 or len(females) == 0):
            break;

        main()
        happyend()
        matchCount += 1

    print candidates
    print employers
    print matchCount

    writeOutput()
    writeOutputToCSV('candidate_matches.csv', 'employer_matches.csv', matchCount)

realMain()