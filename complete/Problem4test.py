#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 4

import sys
import re

"""
A palindromic number reads the same both ways.
The largest palindrome made from the product of
two 2-digit numbers is 9009 = 91  99.

Find the largest palindrome made from the
product of two 3-digit numbers.


"""

def pal(string):
  pal_y_or_n = False
  final_num_chars = len(string)%2
  if final_num_chars == 0:
    n_steps = len(string)/2
  else:
    n_steps = (len(string) - 1)/2
  print n_steps
  for i in range(n_steps):
    if string[0] == string[-1]:
      string = string.strip(string[0])
      print string
      if i+1 == n_steps:
        pal_y_or_n = True
    else:
      break

  return pal_y_or_n
    
def palindrome(max):
  i = max
  k = max
  end = False
  product_string = ''
  while i >0:
    k = max
    while k >= 0:
      product = i*k
      product_string = str(product)
      if pal(product_string):
        end = True
        break        
      k = k-1
    if end:
      break
    i = i-1


  



def main():
  number = str(sys.argv[1])
  print pal(number)



if __name__ == '__main__':
  main()
