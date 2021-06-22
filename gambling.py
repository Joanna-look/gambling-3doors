# Monty Hall problem
import random
import numpy as np
import matplotlib.pyplot as plt
import sys


class Monty:
    """Advanced usage: A class that implements the Monty Hall problem functionality"""
    def __init__(self):
        self.doors = [0, 1, 2]  # That's three doors' number
        self.states = self.init_doors()  # Randomly initialize three doors , [0 : goat , 1 : car , 2 : goat]
        self.chosen_door = None  # the door that the participant first chosen

    def init_doors(self):
        reward = ['car', 'goat', 'goat']
        random.shuffle(reward)  # disrupt the order

        # [0 : goat , 1 : car , 2 : goat]
        return dict(zip(self.doors, reward))
        # Advanced usage: Returns a dictionary with keys from self.doors and values from reward in order

    def first_choice(self, chosen_door):
        """
        The participant chooses a door for the first time
        From the remaining two doors, choose a door with a goat to open
        :param chosen_door: int, the door that the participant chosen. It has to be one of self.doors
        :return:
        """
        if chosen_door not in self.doors:
            # error handle
            raise ValueError(f'It has to be one of {self.doors}')
        print(f'You choose the door {chosen_door}')
        self.chosen_door = chosen_door  # store the chosen_door
        remain_doors = [door for door in self.doors if door != chosen_door]
        # Advanced usage: use list generation to get the list after removing chosen_door


        for door in remain_doors:
            if self.states[door] == 'goat':
                self.doors.remove(door)  # open the door with a goat,
                print(f'Now a door with a goat behind it was opened.')
                break  # jump out of the loop

    def final_choice(self, change):
        """
        Make the final choice and reveal the answer
        :param change: bool, choose another door or not
        :return: int, rhe victory scored a point, and zero points for failure
        """
        if not change:
            final_door = self.chosen_door
            print('You choose not to change')
        else:
            self.doors.remove(self.chosen_door)
            final_door = self.doors[0]
            print('You choose to switch to another door')

        if self.states[final_door] == 'car':
            print('You win a car!')
            return 1
        else:
            print('Uh oh!This is a goat!')
            return 0

    def get_doors(self):
        return self.doors


def play():
    """
    Game interaction function
    """
    # Instantiate class Monty
    monty = Monty()
    # Enter a number that represents a door on the keyboard
    first = int(input(f'Choose a door in {monty.get_doors()} :'))
    monty.first_choice(first)
    char = input('Do you choose to change the door? (y/n) :')
    if char not in ['y', 'n']:
        # error handle
        raise ValueError(f'It has to be "y" or "n"')
    change = True if char == 'y' else False
    # Advanced usage: ternary operator
    monty.final_choice(change)


def monte_carlo():
    """
    The monte Carlo method is used to calculate the benefits of no change, change and randomization
    """
    n = 2000  # The number of experiments for each strategy
    first = 0  # Let's say the participant pick 0 the first time in every experiment
    benefits = {
        'no_change': [],
        'change': [],
        'randomization': []
    }  # store the score for each game for each of the three strategies
    # no change
    for i in range(n):
        monty = Monty()
        monty.first_choice(first)
        point = monty.final_choice(False)  # always no change
        benefits['no_change'].append(point)
    # change
    for i in range(n):
        monty = Monty()
        monty.first_choice(first)
        point = monty.final_choice(True)  # always change
        benefits['change'].append(point)
    # randomization
    for i in range(n):
        monty = Monty()
        monty.first_choice(first)
        point = monty.final_choice(random.choice([True, False]))  # randomization
        benefits['randomization'].append(point)
    print()
    print('"no change" average benefit:', np.mean(benefits['no_change']))
    print('"change" average benefit:', np.mean(benefits['change']))
    print('"randomization" average benefit:', np.mean(benefits['randomization']))

    # Plot the average benefit curve
    plt.plot(average_benefit(benefits['no_change']), c='r')
    plt.plot(average_benefit(benefits['change']), c='b')
    plt.plot(average_benefit(benefits['randomization']), c='g')
    plt.legend(['no_change', 'change', 'randomization'])
    plt.title('Average Benefit Curve of Three strategies')
    plt.xlabel('number of experiment')
    plt.ylabel('average benefit')
    plt.show()


def average_benefit(lst):
    """
    Calculate the change in average benefit as the number of times increases , return a list
    """
    out = []
    for i in range(len(lst)):
        out.append(sum(lst[:i+1])/(i+1))
    return out


if __name__ == '__main__':
    # usage: 1 means to run an interactive game
    #        2 means to run the Monte Carlo function
    mode = input('Please choose your mode , 1 : people , 2 : experiment:')

    if mode == '1':
        play()
    if mode == '2':
        monte_carlo()


