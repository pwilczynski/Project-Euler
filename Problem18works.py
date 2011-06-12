#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 18

import sys
import re
import random

"""
By starting at the top of the triangle below and moving
to adjacent numbers on the row below, the maximum total 
from top to bottom is 23.

    3
   7 4
  2 4 6
 8 5 9 3

That is, 3 + 7 + 4 + 9 = 23.

Find the maximum total from top to bottom of the triangle below:

75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23

NOTE: As there are only 16384 routes, it is possible to 
solve this problem by trying every route. However, Problem 67, 
is the same challenge with a triangle containing one-hundred rows; 
it cannot be solved by brute force, and requires a clever method! ;o)
"""
def nextline(randomnum, location, linenumber, digits):
    #this function decides where the ball falls
    print digits
    choiceL = float(digits[location])
    choiceR = float(digits[location+1])
    weight = choiceL + choiceR
    choiceL = choiceL/weight
    choiceR = choiceR/weight
    if randomnum > choiceL:
        new_location = 0
    else:
        new_location = 1
    #print (choiceR+choiceL), choiceL, choiceR
    #print new_location
    return new_location

def sortedDictValues(adict):
    keys = adict.keys()
    keys.sort()
    return [dict[key] for key in keys]
    
    
def max_path(filename):
  f = open(filename, 'r')
  number = 0
  location = 0
  max_sum = 0
  num_rows = 0
  summation = 0
  lines = []
  new_path = [0]
  location = 0
  path_dict = {}
  for line in f:
      line = line.rstrip("\n")
      lines.append(line)  
  num_rows = len(lines)
  f.close()
  print "There are", num_rows, " rows in this triangle"
  print lines
  for line in lines:
      for i in range(num_rows):
          location +=i
          summation += int(line[location])
          print summation    
      summation = 0

  print "Completed analysis"
  print summation        


  
  

def main():
  filename = sys.argv[1]
  max_path(filename)
  
  


if __name__ == '__main__':
  main()
