#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 8

import sys
import re
import math

"""
A Pythagorean triplet is a set of three natural numbers, a  b  c, for which,

a2 + b2 = c2
For example, 32 + 42 = 9 + 16 = 25 = 52.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.
"""

def int_eval(num):
    if num%2 == 0:
        tmp_int = True
    else:
        tmp_int = False    
    return tmp_int
        
def pythag_sum(number):
    sum = 0
    end = False
    print number
    for i in range(1,2*number):
        for k in range(1,2*number):
            a = k*k - i*i
            b = 2*k*i
            c = k*k + i*i
            sum = a + b + c
            print a, b, c, " is a pythagorean triple"
            print "   Sum: ", sum
            if sum == number:
                print "DONE"
                end = True
                product = a*b*c
                break
        if end:
            break
    return product
        
                    
                
    
    
        
   
        
  
 

def main():
    number = long(sys.argv[1])
    print pythag_sum(number)



if __name__ == '__main__':
  main()
