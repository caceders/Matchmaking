"""
The GUI Element for matchmaking.

I am so sorry for this mess
"""

import numpy as np
import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import Matchmaking
import time
import os

class GUI():
    def __init__(self) -> None:
       
       self.run = True
       self.inputing = False
       self.state = 0
       self.teams = []

    def clearScreen(self):
        os.system('cls')

    def displayStartScreen(self):
        print("""

        ░█▀▀█ 
        ▒█▄▄█ 
        ▒█░▒█

        ███╗░░░███╗░█████╗░████████╗░█████╗░██╗░░██╗███╗░░░███╗░█████╗░██╗░░██╗██╗███╗░░██╗░██████╗░
        ████╗░████║██╔══██╗╚══██╔══╝██╔══██╗██║░░██║████╗░████║██╔══██╗██║░██╔╝██║████╗░██║██╔════╝░
        ██╔████╔██║███████║░░░██║░░░██║░░╚═╝███████║██╔████╔██║███████║█████═╝░██║██╔██╗██║██║░░██╗░
        ██║╚██╔╝██║██╔══██║░░░██║░░░██║░░██╗██╔══██║██║╚██╔╝██║██╔══██║██╔═██╗░██║██║╚████║██║░░╚██╗
        ██║░╚═╝░██║██║░░██║░░░██║░░░╚█████╔╝██║░░██║██║░╚═╝░██║██║░░██║██║░╚██╗██║██║░╚███║╚██████╔╝
        ╚═╝░░░░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝╚═╝░░╚══╝░╚═════╝░

        ▒█▀▀█ █▀▀█ █▀▀█ █▀▀▀ █▀▀█ █▀▀█ █▀▄▀█ 
        ▒█▄▄█ █▄▄▀ █░░█ █░▀█ █▄▄▀ █▄▄█ █░▀░█ 
        ▒█░░░ █░▀█ █▄▄█ █▄▄█ █░▀█ █░░█ █░░░█
        """)
        print("Press enter to continue")
        input()

    def displayInfoScreen(self):
        print("""
        This program was made to optimize matchmaking.
        The optimization is based on ACO-algorithms:
        https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms
        Documentation can be found here: TBA
        The program generates a high-value set of matches from a set of teams.
        In a set of matches, every team is matched with one, and only one other team.

        Each match has a base-value varying from -1 (worst match) to 1 (perfect match)
        The value of the set of matches (set-values) is the average of all the base-values.
        These have the same variations from -1 (worst set) to 1 (perfect set)

        The match-values can be calculated through the skill level of the each team or be set manually.
        """)
        print("Press enter to continue")
        input()

    def displayMenyScreen(self):
        print("""
        Please select an option:

        [1]: Run demo (Generate teams with random skill)

        [2]: Run calculations (Set up teams manually)

        [3]: Show info
        """)

    def begin(self):
        while(self.run):
            #Intro state
            if(self.state == 0):
                self.displayStartScreen()
                self.clearScreen()
                self.displayInfoScreen()
                self.clearScreen()
                self.inputing = True
                while(self.inputing):
                    self.displayMenyScreen()
                    inp = input()
                    self.clearScreen()
                    if(inp == str(1)):
                        self.state = 1
                        self.inputing = False
                    elif(inp == str(2)):
                        self.state = 2
                        self.inputing = False
                    elif(inp == str(3)):
                        self.inputing = False
                        pass
                    else:
                        print('input not valid')
                        input()
            
            #Random teams state
            if(self.state == 1):
                self.inputing = True
                while(self.inputing):
                    self.clearScreen()
                    amountOfTeams = input('How many teams: ')
                    if(not(amountOfTeams.isnumeric() and int(amountOfTeams) > 0)):
                        print('Input must be a whole positive number')
                        input()
                    elif(int(amountOfTeams) > 100):
                        print('Are you sure? anything over 100 teams might take over 30 minutes to calculate. [y/n]')
                        if(input(':') == 'y'):
                            amountOfTeams = int(amountOfTeams)
                            self.inputing = False

                    else:
                        amountOfTeams = int(amountOfTeams)
                        self.inputing = False
                print()
                #Create teams
                for i in range(amountOfTeams):
                    team = Matchmaking.Team('Team ' + str(i+1), random.randint(-10, 10))
                    self.teams.append(team)
                self.state = 2

            #Team manipulation state
            if(self.state == 2):
                self.inputing = True
                while self.inputing:
                    self.clearScreen()
                    print('Created teams:')
                    print()
                    for team in self.teams:
                        print(team.getInfo(True))
                    print()
                    print("""
        Please select an option:

        [1]: Add Team

        [2]: Remove Team

        [3]: Edit Team

        [4]: Continue
        """)
                    inp = input('')

                    #Add a team
                    if(inp == str(1)):
                        while self.inputing:
                            self.clearScreen()
                            print('Created teams:')
                            print()
                            for team in self.teams:
                                print(team.getInfo(True))
                            print()
                            name = input('Enter a team-name: ')
                            skill = input('Enter a skill level between -10 and 10: ')
                            skill = skill.replace(' ','').replace(',','.').replace("−", "-")
                            if ((not skill.replace('-','').isdigit()) or (float(skill)>float(10)) or (float(skill)<-10) or len(name)== 0):
                                print('Invalid input')
                            else:
                                self.inputing = False
                        self.teams.append(Matchmaking.Team(name, float(skill)))
                        self.inputing = True

                    #Remove a team
                    elif(inp == str(2)):
                        while self.inputing:
                            self.clearScreen()
                            print('Created teams:')
                            print()
                            for team in self.teams:
                                print(team.getInfo(True))
                            print()
                            name = input('Enter a team-name: ')
                            if (len(name)== 0):
                                print('Invalid input')
                            else:
                                self.inputing = False
                        for i in range(len(self.teams)):
                            if self.teams[i].name == name:
                                if(i == len(self.teams)):
                                    self.teams.pop(-1)
                                else:
                                    self.teams.pop(i)
                        self.inputing = True

                    #Edit a team
                    elif(inp == str(3)):
                        while self.inputing:
                            self.clearScreen()
                            print('Created teams:')
                            print()
                            for team in self.teams:
                                print(team.getInfo(True))
                            print()
                            oldname = input('Enter a team-name to change: ')
                            newname = input('Enter a new team-name: ')
                            skill = input('Enter a new skill level between -10 and 10: ')
                            skill = skill.replace(' ','').replace(',','.').replace("−", "-")
                            if ((not skill.replace('-','').isdigit()) or (float(skill)>float(10)) or (float(skill)<-10) or len(newname)== 0):
                                print('Invalid input')
                            else:
                                self.inputing = False
                        for i in range(len(self.teams)):
                            if self.teams[i].name == oldname:
                                self.teams[i].name = newname
                                self.teams[i].skill = float(skill)
                        self.inputing = True

                    elif(inp == str(4)):
                        if(len(self.teams) == 0):
                            print("Need at leat two teams!")
                            input("")
                        else:
                            self.inputing = False
                            self.state = 3
                        pass
                    else:
                        print('invalid input')
                        input()

                self.inputing = True
                while(self.inputing):
                    self.clearScreen()
                    print('Created teams:')
                    print()
                    for team in self.teams:
                        print(team.getInfo(True))
                    print()
                    print("""
    All teams can be matched with eachother by default
    Please select an option:

    [1]: Input teams that CAN play against eachother

    [2]: Input teams that CAN NOT play against eachother

    [3]: Continue
    """)        
                    inp = input(':')

                    ##Can only play against eachother
                    if inp == '1':
                        self.inputing = True
                        while(self.inputing):
                            self.clearScreen()
                            print('Created teams:')
                            print()
                            for team in self.teams:
                                print(team.getInfo(True))
                            print()
                            print('Input the name of teams that are able to play with eachother, seperated by a comma.')
                            print('I.E: Team 1, Team 2, Team 3, Team 4')
                            print('When done, press enter without inputing anything')
                            teamNames = input(':')
                            if(teamNames == ''):
                                self.inputing = False
                            else:
                                if(not ', ' in teamNames):
                                    print('Invalid input')
                                else:
                                    teamNames = teamNames.split(', ')
                                    teamNames.reverse()
                                    teamsToNotBlackList = []
                                    InvalidInput = False

                                    #Check if given names exists then prepares the teams for blacklisting
                                    for name in teamNames:
                                        found = False
                                        for team in self.teams:
                                            if name == team.name:
                                                teamsToNotBlackList.append(team)
                                                found = True
                                        if(not found):
                                            teamsToNotBlackList = []
                                            print('invalid input. Could not find team "' + name + '".')
                                            input('')
                                            InvalidInput = True
                                            break
                                    if(not InvalidInput):
                                        for team in teamsToNotBlackList:
                                            for otherTeam in self.teams:
                                                if (otherTeam in teamsToNotBlackList):
                                                    if(team.isBlackListed(otherTeam)):
                                                        team.RemoveFromBlackList(otherTeam)
                                                        otherTeam.RemoveFromBlackList(team)
                                                else:
                                                    team.addToBlackList(otherTeam)
                                                    otherTeam.addToBlackList(team)
                        self.inputing = True

                    
                    #Can not play against eachother
                    elif inp == '2':
                        self.inputing = True
                        while(self.inputing):
                            self.clearScreen()
                            print('Created teams:')
                            print()
                            for team in self.teams:
                                print(team.getInfo(True))
                            print()
                            print('Input the name of teams that are unable to play with eachother, seperated by a comma.')
                            print('I.E: Team 1, Team 2, Team 3, Team 4')
                            print('When done, press enter without inputing anything')
                            teamNames = input(':')
                            if(teamNames == ''):
                                self.inputing = False
                            else:
                                if(not ', ' in teamNames):
                                    print('Invalid input')
                                else:
                                    teamNames = teamNames.split(', ')
                                    teamNames.reverse()
                                    teamsToBlackList = []
                                    InvalidInput = False

                                    #Check if given names exists then prepares the teams for blacklisting
                                    for name in teamNames:
                                        found = False
                                        for team in self.teams:
                                            if name == team.name:
                                                found = True
                                                teamsToBlackList.append(team)
                                        if(not found):
                                            teamsToBlackList = []
                                            print('invalid input. Could not find team "' + name + '".')
                                            input('')
                                            InvalidInput = True
                                            break
                                    if(not InvalidInput):
                                        for team in teamsToBlackList:
                                            for otherTeam in teamsToBlackList:
                                                if not (team == otherTeam):
                                                    team.addToBlackList(otherTeam)
                                                    otherTeam.addToBlackList(team)
                        self.inputing = True

                    elif inp == '3':
                        self.inputing = False
                    else:
                        print('Invalid input')

                
                self.clearScreen()
                print('')
                                


            if(self.state == 3):
                set = Matchmaking.Set(self.teams)

                self.clearScreen()

                contests = []
                values = []
                averages = []
                bestContest = None
                bestValue = -10
                amountOfTeams = len(self.teams)
                foundError = False
                for i in tqdm(range(amountOfTeams * set.numberOfValuesInAverage * 2), desc='Calculating best set of ' + str(amountOfTeams) + ' teams...'):
                    
                    try:
                        contests.append(set.createContest())
                    except RuntimeError:
                        (print(' ERROR: Could not make a set of matches with this configuration!'))
                        input('')
                        foundError = True
                        newGui = GUI()
                        newGui.begin()
                        del self
                        break

                    values.append(contests[-1].getScaledValue())

                    if (contests[-1].getScaledValue()) >= bestValue:
                        bestContest = contests[-1]
                        bestValue = contests[-1].getScaledValue()
                    set.updateAverageScaledValue()
                    averages.append(set.averageScaledValue)
                    contests[-1].averageScaledValue = set.averageScaledValue
                    contests[-1].updateMatchWeigths()
                
                if(not foundError):
                    print()
                    print('Best set found:')
                    for match in bestContest.matches:
                        print(match.getInfo())
                    if(bestContest.hasUnpairedTeam()):
                        print('One team without a match: ' + bestContest.unpairedTeam.getInfo())
                    
                    print()
                    print('Set value: ' + str(bestContest.getScaledValue()))
                    print('Average of last ' + str(set.numberOfValuesInAverage) + ' generated contests:' + str(set.averageScaledValue))
                    print()
                    print('Press enter to display graph')
                    input()
                    plt.plot([i for i in range(len(contests))], values, label = 'Set-score.')
                    plt.plot([i for i in range(len(contests))], averages, label = 'Moving average of ' + str(set.numberOfValuesInAverage) + ' sets.')
                    plt.legend()
                    plt.title('Set-scores and average of optimization')
                    plt.grid(axis='y')
                    plt.xlabel('Itteration')
                    plt.ylabel('Score')
                    plt.show()
                    print('Press enter to exit')
                    input()
            self.state = 0
            
main = GUI()
main.begin()
