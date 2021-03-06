# This file is part of Piper.
#
#    Piper is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Piper is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Piper.  If not, see <http://www.gnu.org/licenses/>.
#
# Piper Copyright (C) 2013  Christopher Cassano

import os
from subprocess import Popen, PIPE
import sqlite3

pubkey = ""
privkey = ""
keysAreValid = False


def genKeys():
    global pubkey, privkey, keysAreValid

    keysAreValid = False

    process = Popen(["./vanitygen", "-q", "-t", "1", "-s", "/dev/random", "1"], stdout=PIPE)

    results = process.stdout.read()
    addrs = results.split()
    pubkey = addrs[3]
    privkey = addrs[5]

    #we do a basic length sanity check on the public and private keys
    if len(privkey) == 51 and len(pubkey) >= 27:
        keysAreValid = True
    else:
        keysAreValid = False

