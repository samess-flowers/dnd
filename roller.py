#!/opt/homebrew/python3
'''Roll dice for D&D and such'''
import argparse
import random
import sys

class DumbassError(Exception):
    '''user was dumbass'''

def roll(count:int, die: int) -> tuple:
    '''Roll count dice of die size,
    Returns a tuple with the total and the results'''
    results = []
    for i in range(count): # pylint: disable=W0612
        if die == 10:
            results.append(random.randrange(0,9))
        else:
            results.append(random.randrange(1,die))
    total = sum(results)
    return total, results

while __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dice")
    args = parser.parse_args()
    try:
        if len(args.dice) not in [3,4]:
            raise DumbassError
        dice = args.dice
        args = dice.split()
        print(args)
    except DumbassError as error:
        print("ERROR: Incorrect input", file=sys.stderr)
        sys.exit(10)
    