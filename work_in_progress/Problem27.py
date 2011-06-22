#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 27

import sys
import re
import math
"""
Euler published the remarkable quadratic formula:

n^2+ n + 41

It turns out that the formula will produce 40 primes for the consecutive values
n = 0 to 39. However, when n = 40, 402 + 40 + 41 = 40(40 + 1) + 41 is divisible
by 41, and certainly when n = 41, 41^2 + 41 + 41 is clearly divisible by 41.

Using computers, the incredible formula  n^2  79n + 1601 was discovered, which 
produces 80 primes for the consecutive values n = 0 to 79. The product of the 
coefficients, 79 and 1601, is 126479.

Considering quadratics of the form:

n^2 + an + b, where |a| < 1000 and |b| < 1000

Find the product of the coefficients, a and b, for the quadratic expression 
that produces the maximum number of primes for consecutive values of n, 
starting with n = 0.

"""

def isprime(n):
    for x in range(2, n):
        if n % x == 0:
            prime=False
            break
    else:                                  
        prime=True
    #print prime
    return prime

def combinations():
    n = 0
    max_count = 0
    for a in range(-1000,1000):
        for b in range(-1000,1000):
            num = n*n + a*n + b
            if num>0:
                while isprime(num):
                    n+=1
                    num = n*n + a*n + b
               # print a,b,n
            if n>max_count:
                max_count = n
                max_a = a
                max_b = b
                print ""
                print max_count, max_a, max_b

            n = 0

    


def main():
  combinations()
 


if __name__ == '__main__':
  main()
