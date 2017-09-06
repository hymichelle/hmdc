#!/usr/bin/env python

import time
import sys

def debug(category='', message=''):
    ''' custom debugging function.
    + category {str} -- INFO, DEBUG, WARN
    + message {str} -- message to print.
    '''

    # colors
    c_rst = '\033[39m' # reset
    c_w = '\033[97m' # white
    c_p = '\033[95m' # purple
    c_g = '\033[92m' # green
    c_r = '\033[91m' # red
    c_b = '\033[96m' # blue

    timestamp = '%s[%s]%s' % (c_w, time.asctime(), c_rst)
    template = ' '.join([timestamp, '%s[%s%s%s] %s'])

    category = category.strip().lower()

    # INFO
    if category in ['i', 'info']:
        sys.stdout.write(template % (c_w, c_g, 'info', c_w, message))

    # DEBUG
    elif category in ['d', 'debug']:
        sys.stdout.write(template % (c_w, c_p, 'debug', c_w, message))

    # WARN
    elif category in ['w', 'warn']:
        sys.stderr.write(template % (c_w, c_r, 'warn', c_w, message))

    # BUG
    elif category in ['b', 'bug']:
        sys.stderr.write(template % (c_w, c_b, 'bug', c_w, message))

    # default
    else:
        sys.stdout.write(template % (c_w, c_w, 'log', c_w, message))
