'''
utils - console interface
'''

import sys, datetime

SPEED = 2.2

def welcome():
    print("\n")
    print("  ______             ______      _                  _ ")
    print(" |  ____|           |  ____|    | |                | |  ")
    print(" | |__ __ _  ___ ___| |__  __  _| |_ _ __ __ _  ___| |_ ___  _ __ ")
    print(" |  __/ _` |/ __/ _ \  __| \ \/ / __| '__/ _` |/ __| __/ _ \| '__|")
    print(" | | | (_| | (_|  __/ |____ >  <| |_| | | (_| | (__| || (_) | | ")
    print(" |_|  \__,_|\___\___|______/_/\_\\__|_|  \__,_|\___|\__\___/|_| ")
    print("\n")


def print_state(progress, file_count):
    eta = (file_count - progress) * SPEED
    eta = str(datetime.timedelta(seconds=eta))
    eta = ':'.join(str(eta).split(':')[:3])[:7]

    perc = int(progress / file_count * 100)
    done = ''.join(['#' for j in range(int(perc/2))])
    to_do = ''.join(['-' for j in range(50 - int(perc/2))])
    sys.stdout.write("\r{}[{}{}]{}".format(str(perc) + '%', done, to_do, str(100) + '%' + ' - eta : {}'.format(eta)))
    sys.stdout.flush()