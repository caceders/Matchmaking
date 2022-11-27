"""
The GUI Element for 
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
                    amountOfTeams = input('How many teams (0-200): ')
                    if(not(amountOfTeams.isnumeric() and int(amountOfTeams) <= 200 and int(amountOfTeams) > 0)):
                        print('Input must be an integer between 0-200')
                        input()
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
                        print(team.name + ' with a skill of ' + str(team.skill))
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
                            name = input('Enter a team-name: ')
                            skill = input('Enter a skill level between -10 and 10: ')
                            skill = skill.replace(' ','').replace(',','.').replace("−", "-")
                            print(float(skill))
                            if ((not skill.replace('-','').isdigit()) or (float(skill)>float(10)) or (float(skill)<-10) or len(name)== 0):
                                print('Invalid input')
                                input()
                            else:
                                self.inputing = False
                        self.teams.append(Matchmaking.Team(name, float(skill)))
                        self.inputing = True

                    #Remove a team
                    elif(inp == str(2)):
                        while self.inputing:
                            name = input('Enter a team-name: ')
                            if (len(name)== 0):
                                print('Invalid input')
                                input()
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
                            oldname = input('Enter a team-name to change: ')
                            newname = input('Enter a new team-name: ')
                            skill = input('Enter a new skill level between -10 and 10: ')
                            skill = skill.replace(' ','').replace(',','.').replace("−", "-")
                            if ((not skill.replace('-','').isdigit()) or (float(skill)>float(10)) or (float(skill)<-10) or len(name)== 0):
                                print('Invalid input')
                                input()
                            else:
                                self.inputing = False
                        for i in range(len(self.teams)):
                            if self.teams[i].name == oldname:
                                self.teams[i].name = newname
                                self.teams[i].skill = float(skill)
                        self.inputing = True

                    elif(inp == str(4)):
                        if(len(self.teams) % 2 != 0):
                            print("Currently only supports an even amount of teams! Add or remove a team to continue.")
                            input("")
                        elif(len(self.teams) == 0):
                            print("Need at leat two teams!")
                            input("")
                        else:
                            self.inputing = False
                            self.state = 3
                        pass
                    else:
                        print('input not valid')
                        input()

            if(self.state == 3):
                set = Matchmaking.Set(self.teams)

                self.clearScreen()

                contests = []
                values = []
                averages = []
                bestContest = None
                bestValue = 0
                amountOfTeams = len(self.teams)
                for i in tqdm(range(amountOfTeams * set.numberOfValuesInAverage * 2), desc='Calculating best set of ' + str(amountOfTeams) + ' teams...'):
                    if( i > 999):
                        something = 0
                        pass
                    contests.append(set.createContest())
                    values.append(contests[-1].getScaledValue())

                    if (contests[-1].getScaledValue()) >= bestValue:
                        bestContest = contests[-1]
                        bestValue = contests[-1].getScaledValue()
                    set.updateAverageScaledValue()
                    averages.append(set.averageScaledValue)
                    contests[-1].averageScaledValue = set.averageScaledValue
                    contests[-1].updateMatchWeigths()
                
                print()
                print('Best set found:')
                for match in bestContest.matches:
                    print(match.getInfo())
                
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
                self.run = False
main = GUI()
main.begin()
