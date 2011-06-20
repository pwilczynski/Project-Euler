#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 14

import sys
import re

"""
The following iterative sequence is defined for the set of positive integers:

n  n/2 (n is even)
n  3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:

13  40  20  10  5  16  8  4  2  1

It can be seen that this sequence (starting at 13 and finishing at 1) contains 
10 terms. Although it has not been proved yet (Collatz Problem), it is thought
that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.
"""

def iteration(n):
    if n%2==0:
        n_new = n/2
    else:
        n_new = 3*n+1
    return n_new

def counting(n):
    i = 0
    while n>0:
      n = iteration(n)
      i += 1
#      print n, i
      if n == 1:
          break
    return i
    

def large_sequence(max):
  print "SEQUENCE!!!"
  count = 0
  large_count = [count, 1]
  for n in range(1, max):
       count = counting(n)
       if count>large_count[0]:
           large_count = [count, n]
           print "New Large Count!!:", large_count


  
  
  
  
  
  print large_count
  
  
  
 

def main():
  number = long(sys.argv[1])
  large_sequence(number)



if __name__ == '__main__':
  main()
