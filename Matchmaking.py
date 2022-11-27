"""
Program for calculating best possible set based upon some teams and their skills.

TODO:
x Find out why we get a positive average for contestvalue (want 0). Logicerror?
x Deal with above point.
x Find an algorithm to calculate best match
x Deal with problem: When average goes too much, bad values get prioritized over good.

- Clean GUI Code
- Implement GUI better
- Solve when to end itterations
- Implement a way to blacklist teams
"""

import numpy as np
import random
from tqdm import tqdm
import matplotlib.pyplot as plt

class Team:
    def __init__(self, name: str, skill: float = 0):
        """
        Creates a new team.

        :param str name: Teamname
        :param float skill: The skill of the team. Can be a float between -10 and 10
        """
        self.name = name
        if abs(skill) > 10:
            self.skill = 0
            raise ValueError('Skill out of range(' + str(skill) + '). Changed the skill of ' + self.name + ' to 0')
        else:
            self.skill = skill
        
        #Used during optimization algorithm
        self.matchedWith:Team = None
        #Possible matches this team is part of. Used during optimization alhorithm
        self.matches = []

        #List of teams this team cannot be matched with
        self.blackList = []


    def addToBlackList(self, team):
        """Adds other to list of teams this team cannot be matched with"""
        if not isinstance(team, Team):
            raise TypeError('Object added to blaclist of ' + self.name + ' is not of type Team')
        elif team in self.blackList:
            raise RuntimeError('Team ' + team.name + ' already in blackList for ' + self.name)
        else:
            self.blackList.append(team)
            team.blackList.append(team)

    def isBlackListed(self, team):
        """Checks if team is blacklisted"""
        return team in self.blackList
    
    def addToMatches(self, match):
        """Adds match to list of teams this team cannot be matched with"""
        if not isinstance(match, Match):
            raise TypeError('Object added to matchlist of ' + self.name + ' is not of type Match')
        elif match in self.matches:
            raise RuntimeError('Match with ' + match.team.name + ' and ' + match.team2.name + ' already in matchlist for ' + self.name)
        else:
            self.matches.append(match)
    
    def getAvailableMatches(self):
        matches = []
        for match in self.matches:
            if not match.containsMatchedTeam():
                matches.append(match)
        return matches

class Match:
    def __init__(self, team1: Team, team2: Team, baseValue:float = None,):
        """
        Creates a Match with two teams. If no value is given one is calculated based on the skill of the teams.

        :param float baseValue: Match value, from -1 to 1
        """
        self.team1 = team1
        self.team2 = team2

        if baseValue == None:
            self.baseValue = 1 - abs(team1.skill - team2.skill)/10
        elif abs(baseValue) > 1:
            self.baseValue = 0
            raise ValueError('Value out of range(' + str(baseValue) + '). Changed the value of Match:' + team1.name + '-' + team2.name + ' to 0')
        else:
            self.baseValue = baseValue
        
        #A property used and manipulated by the optimization algorithm
        self.weigth:float = 1
    
    def getInfo(self) -> str:
        return (self.team1.name + ' with a skill of ' + str(self.team1.skill) + ' vs ' + self.team2.name + ' with a skill of ' + str(self.team2.skill) + '. Matchscore: '+ str(round(self.baseValue, 2)))

    def contains(self, team1:Team, team2:Team = None):
        containsTeam1 = (self.team1 == team1) or (self.team2 == team1)
        if team2 == None:
            return containsTeam1
        containsTeam2 = (self.team1 == team2) or (self.team2 == team2)
        return containsTeam1 or containsTeam2

    def containsMatchedTeam(self):
        team1Matched = self.team1.matchedWith != None
        team2Matched = self.team2.matchedWith != None
        return team1Matched or team2Matched
    
    def getOther(self, team):
        """Returns the other team of match if the passed in team exist in match"""
        if self.contains(team):
            if self.team1 == team:
                return self.team2
            else:
                return self.team1
        else:
            return None

    def resetWeigth(self):
        self.weigth = 1
    
    def addToWeigth(self, addition):
        """Adds/subtracts addition to the weigth. Weigth cannot go lower than 0.0001"""
        if(self.weigth + addition) < 0:
            self.weigth = 0.00001
        else:
            self.weigth += addition

class Contest:
    def __init__(self, teams, matches):
        """
        Creates a contest with the teams and matches. Each team can only be in one match.
        """

        self.teams = []
        self.matches = []
        self.value = 0

        #List used to check if team already exist in a match
        self.matchedTeams = []

        #Constant used in recursive optimisation. Found programatically - is problematic? idc
        self.averageScaledValue = 0.3

        for team in teams:
            #Check if teams-parameter is passed correctly
            if not isinstance(team, Team):
                raise TypeError('Element in team list parameter of contest not of Team type')
            else:
                self.teams.append(team)

        for match in matches:
            #Check if match-parameter is passed correctly
            if not isinstance(match, Match):
                raise TypeError('Element in team list parameter of contest not of Team type')
            else:
                for team in self.matchedTeams:
                    if match.contains(team):
                        raise RuntimeError('Tried to create a contest where a team is in multiple matches')
                #Add objects to lists and update value
                self.matches.append(match)
                self.matchedTeams.append(match.team1)
                self.matchedTeams.append(match.team2)
                self.value += match.baseValue
    
    def getValue(self):
        return self.value

    def getScaledValue(self):
        """Returns a value scaled with the inverse of number of matches"""
        return self.value / len(self.matches)

    def updateMatchWeigths(self):
        for match in self.matches:
            match.addToWeigth((self.getScaledValue()-self.averageScaledValue
            ))

    def getInfo(self):
        infostring = ''
        for match in self.matches:
            infostring += match.getInfo()
            infostring += '\n'
        infostring += 'Total value: ' + str(self.value)

class Set:
    def __init__(self, teams:list):
        """
        Creates a set of teams and matches

        :param list teams: teams to be used in set.
        :param list matches: matches to be used if teams are not passed.
        """

        self.teams = []
        self.EvenNumberTeams = False

        #Every possible match in this set
        self.matches = []

        #List of generated contests
        self.contests = []

        #Average of scaled values in contests
        self.averageScaledValue = 0

        #Number of values in average of last values
        self.numberOfValuesInAverage = 1000

        #Check if teams-parameter is passed correctly
        for team in teams:
            if not isinstance(team, Team):
                raise TypeError('Element in team list parameter of set not of Team type')
            else:
                self.teams.append(team)
        self.EvenNumberTeams = (len(self.teams) % 2 == 0)

        #Create all matches through construction
        self.createMatches()
    
    def createMatches(self):
        """Creates all matches for the teams in this set"""
        if len(self.matches) != 0:
            raise RuntimeError('Tried to create matches multiple times')
        else:
            lastTeamIndex = len(self.teams)
            for i in range(lastTeamIndex):
                team1 = self.teams[i]
                teamindex = self.teams.index(team1)
                for i in range(teamindex + 1, lastTeamIndex):
                    team2 = self.teams[i]
                    if team1.isBlackListed(team2):
                        pass
                    else:
                        match = Match(team1=team1, team2=team2)
                        self.matches.append(match)
                        team1.addToMatches(match)
                        team2.addToMatches(match)
        
    def resetMatching(self):
        for team in self.teams:
            team.matchedWith = None

    def createContest(self, weighted:bool = True) -> Contest:
        """Creates a contest, randomly or based on matchweigth"""
        matches = []
        #Shuffles team list to unbias the startingteams
        random.shuffle(self.teams)
        for team in self.teams:
            if team.matchedWith == None:
                availableMatches = team.getAvailableMatches()
                match = None
                if not weighted:
                    match = random.choice(availableMatches)
                else:
                    weights = []
                    for match in availableMatches:
                        weights.append(match.weigth)
                    match = random.choices(availableMatches, weights, k=1)[0]
                other = match.getOther(team)
                team.matchedWith = other
                other.matchedWith = team
                matches.append(match)
        contest = Contest(self.teams, matches)
        self.resetMatching()
        if weighted:
            self.contests.append(contest)
        return contest

    def updateAverageScaledValue(self) -> float:

        if(len(self.contests) < self.numberOfValuesInAverage):
            #Multiplies with last n, then divides with the new n
            #Won't loop to save processing power
            self.averageScaledValue *= (len(self.contests) - 1) / len(self.contests)
            #Adds newest contest value
            self.averageScaledValue += self.contests[-1].getScaledValue() / len(self.contests)

        elif(len(self.contests) == self.numberOfValuesInAverage):
            self.averageScaledValue *= (len(self.contests) - 1) / self.numberOfValuesInAverage
            #Adds newest contest value
            self.averageScaledValue += self.contests[-1].getScaledValue() / self.numberOfValuesInAverage
            #Removes oldest value
            self.averageScaledValue -= self.contests[-self.numberOfValuesInAverage].getScaledValue() / self.numberOfValuesInAverage

        else:
            #Adds newest contest value
            self.averageScaledValue += self.contests[-1].getScaledValue() / self.numberOfValuesInAverage
            #Removes oldest value
            self.averageScaledValue -= self.contests[-self.numberOfValuesInAverage].getScaledValue() / self.numberOfValuesInAverage