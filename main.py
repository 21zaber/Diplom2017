#!/usr/bin/python3.5

from Vector import Vector
from Hadamard import HadamardMatrix
from SSS import HSSS

import sys
import argparse


def read_hadamard(fname):
    fin = open(fname, 'r')
    n = int(fin.readline())
    h = HadamardMatrix.new(n=n, m=0)
    for i in range(n):
        t = fin.readline()[:n]
        h[i] = Vector([[1, -1][j!='+'] for j in t])
        
    h.check()

    return h

def cover_secret(h, s):
    print("Secret to cover:", s)
    scheme = HSSS(h)
    u = scheme.cover(s)
    print("Parts of secret:")
    for i in range(len(u)):
        print("{} {}".format(str(i+1).rjust(3, ' '), u[i]))

def recover_secret(h, parts):
    scheme = HSSS(h)
    s = scheme.recover(parts)
    print("Recovered secret:", int(s+0.000001))



parser = argparse.ArgumentParser(description="Secret-sharing scheme base on Hadamard matrix.")
parser.add_argument("hmatrix", help="path to file with Hadamard matrix.")
group = parser.add_mutually_exclusive_group()
group.add_argument("-c", "--cover", type=int, help="integer secret to cover. Example: 12345.")
group.add_argument("-r", "--recover", nargs='*', type=float, help="parts generated by that programm. Example 1 3 4 7.")
args = parser.parse_args()


try:
    H = read_hadamard(args.hmatrix)
    if args.cover is not None:
        cover_secret(H, args.cover)
    else:
        parts = args.recover
        if len(parts) % 2 == 1:
            raise Exception("Error: wrong parametr parts")
        parts = [(int(parts[i]), parts[i+1]) for i in range(0, len(parts), 2)]
        recover_secret(H, parts)

except Exception as e:
    print(e)
