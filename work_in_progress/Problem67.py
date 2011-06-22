#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 67

import sys
import re

"""
By starting at the top of the triangle below and moving
to adjacent numbers on the row below, the maximum total 
from top to bottom is 23.

3
7 4
2 4 6
8 5 9 3

That is, 3 + 7 + 4 + 9 = 23.

Find the maximum total from top to bottom in triangle.txt 
(right click and 'Save Link/Target As...'), a 15K text file 
containing a triangle with one-hundred rows.

NOTE: This is a much more difficult version of Problem 18.
It is not possible to try every route to solve this problem, 
as there are 299 altogether! If you could check one trillion (1012)
routes every second it would take over twenty billion years 
to check them all. There is an efficient algorithm to solve it. ;o)
"""


def max_path(filename):
  f = open(filename, 'r')
  number = 0
  location = 0
  max_sum = 0
  path_list = []
  for line in f:
      print line
      nums = line.split()
      if len(nums)>1:
          if nums[location]>nums[location+1]:
          #    print nums[location]
              number = nums[location]
              location = location
          else:
          #    print nums[location+1]
              number = nums[location+1]
              location = location +1
      else:
          location = 0
      #    print nums[location]
          number = nums[location]
      path_list.append(number)
      #print max_sum
  print "Completed analysis"
  print path_list
  for num in path_list:
      max_sum+=int(num) 
  print max_sum
  f.close()
  
  
  
  

def main():
  filename = (sys.argv[1])
  max_path(filename)



if __name__ == '__main__':
  main()
