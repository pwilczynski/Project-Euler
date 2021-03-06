#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 18

import sys
import re
import math
"""
Consider all integer combinations of ab for 2  a  5 and 2  b  5:

22=4, 23=8, 24=16, 25=32
32=9, 33=27, 34=81, 35=243
42=16, 43=64, 44=256, 45=1024
52=25, 53=125, 54=625, 55=3125
If they are then placed in numerical order, with any repeats removed,
we get the following sequence of 15 distinct terms:

4, 8, 9, 16, 25, 27, 32, 64, 81, 125, 243, 256, 625, 1024, 3125

How many distinct terms are in the sequence generated by ab for 2  a
100 and 2  b  100?

"""


def combinations(max):
    nums=range(2,max+1)
    print nums
    final_term_list=[]
    for x in nums:
        for y in range(2,max+1): 
            
            result = int(math.pow(x,y))
            print result
            if result not in final_term_list:
                print "       " + str(result)
                final_term_list.append(result)
          
    final_term_list.sort()    
    print final_term_list
    print len(final_term_list)
  
  
  

def main():
  max = int(sys.argv[1])
  combinations(max)
  h=set()
  for a in range(2,101):
    for b in range(2,101):
      h.add(a**b)
 
  print "Answer to PE29 = ",len(h);



if __name__ == '__main__':
  main()
