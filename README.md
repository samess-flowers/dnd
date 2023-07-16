# Sam's D&D Utilities
This is where Sam stores his Dungeons & Dragons scripts

## roller.py
Roller is a dice rolling utility.  It includes library functions for rolling arbitrary dice and rolling stats, as well as an argparse CLI frontend for rolling dice on the commamndline.

```
>/roller.py -h
usage: roller.py [-h] [-a | -d | -l | -c] [-s] [-r] [dice]

positional arguments:
  dice                Something like 1d6

options:
  -h, --help          show this help message and exit
  -a, --advantage     advantage
  -d, --disadvantage  disadvantage
  -l, --lowest        drop lowest
  -c, --character     generate character stats
  -s, --straight      roll straight
  -r, --results       show results
```