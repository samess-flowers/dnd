#!/opt/homebrew/bin/python3
'''Roll dice for D&D and such'''
import argparse
import random
import re
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

def print_rolls(total:int, results:list[int]) -> None:
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

def advantage() -> tuple[int,list]:
    '''Roll 2d20, return highest result'''
    result,results = roll(2,20)
    results = max(results)
    return result, results

def disadvantage() -> tuple[int, list]:
    '''Roll 2d20, return lowest result'''
    result,results = roll(2,20)
    results = min(results)
    return result, results

def lowest(count:int, dice:int) -> tuple[int, list]:
    '''Roll count dice'''
    total, result = roll(count,dice)
    result = sorted(result, reverse=True)
    dropped = result[0:(len(result)-1)]
    total = sum(dropped)
    return total, result

def roll_stats(straight:bool=False) -> tuple[dict, dict]:
    '''Roll 4d6, drop lowest for each D&D stat
    Optional argument straight changes to 3d6 straight
    Returns a dictionary of stats'''
    statnames = [
        "Strength",
        "Dexterity",
        "Constituion",
        "Intelligence",
        "Wisdom",
        "Charisma",
    ]
    stats = {}
    results = {
        "Strength":[],
        "Dexterity":[],
        "Constituion":[],
        "Intelligence":[],
        "Wisdom":[],
        "Charisma":[],
    }
    if straight:
        for stat in statnames:
            value,result = roll(3,6)
            new_stat = {stat:value}
            stats.update(new_stat)
            results[stat] = result
    else:
        for stat in statnames:
            value,result = lowest(4,6)
            new_stat = {stat:value}
            stats.update(new_stat)
            results[stat] = result
    return stats, results

def print_stats(
        results: dict[str,list[int]],
        stats: dict[str,int],
        print_results:bool=False,
        ):
    '''Print a characters stat block'''
    print("Stats:")
    for stat, value in stats.items():
        mod = (value-10)//2
        if value < 10:
            value = f" {value}"
        if mod > 0:
            mod = f"+{mod}"
        elif mod == 0:
            mod = f" {mod}"
        if stat == "Wisdom":
            print(f"{stat}:\t\t{value}\tMod: {mod}")
        else:
            print(f"{stat}:\t{value}\tMod: {mod}")
        if print_results:
            print("  Rolls:\t",results[stat])

def main() -> None:
    '''Parse args, roll di(c)e'''
    parser = argparse.ArgumentParser()
    parser.add_argument("dice", help="Something like 1d6", default="1d6dfault", nargs='?', type=str)
    options = parser.add_mutually_exclusive_group()
    options.add_argument("-a", "--advantage", help="advantage", action="store_true")
    options.add_argument("-d", "--disadvantage", help="disadvantage", action="store_true")
    options.add_argument("-l", "--lowest", help="drop lowest", action="store_true")
    options.add_argument("-c","--character", help="generate character stats", action="store_true")
    parser.add_argument("-s","--straight", help="roll straight", action="store_true")
    parser.add_argument("-r","--results", help="show results", action="store_true")
    args = parser.parse_args()

    if args.advantage:
        result, results = advantage()
        print_rolls(result, results)
        sys.exit(0)
    elif args.disadvantage:
        result, results = disadvantage()
        print_rolls(result,results)
        sys.exit(0)
    elif args.character:
        if args.straight:
            stats, results = roll_stats(straight = True)
        else:
            stats, results = roll_stats()
        print_stats(results, stats)
        sys.exit(0)

    try:
        dice = args.dice
        if len(dice) < 3 or not re.match(r'\d+d\d+',dice):
            print(re.match(r'/d+d/d+',dice))
            print(
            "ERROR: Incorrect input, expected 1d6 or something like that",
            file=sys.stderr
            )
            raise DumbassError
        count, die, *extras = dice.split('d')
        count = int(count)
        die = int(die)

        if not isinstance(count,int) or not isinstance(die,int):
            print("type",type(count),type(die))
            print(
            "ERROR: Incorrect input, expected 1d6 or something like that",
            file=sys.stderr
            )
            raise DumbassError
        if args.lowest and "fault" in extras:
            count, die = (4,6)
        if count < 2 and args.lowest:
            print(
            "ERROR: Incorrect input, expected '-l 4d6' or something like that",
            file=sys.stderr
            )
            raise DumbassError

    except DumbassError:
        sys.exit(10)
    if args.lowest:
        print(f"Rolling {count} d{die}, dropping lowest")
        total,result = lowest(count, die)
        print_rolls(total,result)
    else:
        print(f"Rolling {count} d{die}")
        total, result = roll(count,die)
        print_rolls(total, result)

if __name__ == "__main__":
    main()
