#!/opt/homebrew/bin/python3
'''Roll dice for D&D and such'''
import argparse
import random
import sys

class DumbassError(Exception):
    '''user was dumbass'''

def roll(count:int, die: int) -> tuple[int,list]:
    '''Roll count dice of die size,
    Returns a tuple with the total and the results'''
    results = []
    for each in range(count): # pylint: disable=W0612
        if die == 10:
            results.append(random.randrange(0,9))
        else:
            results.append(random.randrange(1,die))
    total = sum(results)
    return total, results

def print_results(total:int, results:list) -> None:
    '''Prints results of a die roll'''
    if len(results) <= 1:
        print(f"Result:\t{results[0]}")
    elif len(results) > 1:
        print("Results: ")
        i = 1
        for result in results:
            print(f"\t{i}:\t{result}")
            i += 1
        print(f"Total:\t{total}")

def main() -> None:
    '''Parse args, roll di(c)e'''
    parser = argparse.ArgumentParser()
    parser.add_argument("dice")
    args = parser.parse_args()
    try:
        dice = args.dice
        if len(dice) < 3 or 'd' not in dice:
            print("length")
            raise DumbassError
        count, die = dice.split('d')
        count = int(count)
        die = int(die)
        if not isinstance(count,int) or not isinstance(die,int):
            print("type",type(count),type(die))
            raise DumbassError
        print(f"Rolling {count} d{die}")
        total, result = roll(count,die)
        print_results(total, result)
    except DumbassError:
        print(
            "ERROR: Incorrect input, expected 1d4 or something like that",
            file=sys.stderr
            )
        sys.exit(10)

if __name__ == "__main__":
    main()
