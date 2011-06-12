#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 14

import sys
import re

"""
The sequence of triangle numbers is generated by adding the natural numbers.
So the 7th triangle number would be 1 + 2 + 3 + 4 + 5 + 6 + 7 = 28. 
The first ten terms would be:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

Let us list the factors of the first seven triangle numbers:

 1: 1
 3: 1,3
 6: 1,2,3,6
10: 1,2,5,10
15: 1,3,5,15
21: 1,3,7,21
28: 1,2,4,7,14,28

We can see that 28 is the first triangle number to have over five divisors.

What is the value of the first triangle number to have over five hundred 
divisors?
"""

def num_div(n):
    count = 0
    for i in range(1, n+1):
#        print i, n%i
        if n%i == 0:
            count+=1
    return count
    

def triangle_nums(max):
  print "*****Triangle Numbers*****"
  count = 0
  max_count = count
  triangle = 1
  n = 1
  
  while count <=max:
      count = num_div(triangle)
      print triangle, count
      if count>max_count:
          max_count = count
      print max_count
      n+=1
      triangle = triangle + n 
       


def main():
  number = long(sys.argv[1])
  triangle_nums(number)


if __name__ == '__main__':
  main()
