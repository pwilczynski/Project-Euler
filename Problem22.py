#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 22

import sys
import re
import math

"""
Using names.txt (right click and 'Save Link/Target As...'), a 
46K text file containing over five-thousand first names, begin
by sorting it into alphabetical order. Then working out the alphabetical
value for each name, multiply this value by its alphabetical position in 
the list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN,
which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list.
So, COLIN would obtain a score of 938  53 = 49714.

What is the total of all the name scores in the file?
"""

def makealphadict():
    alpha_dict = {}
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(len(alphabet)):
        alpha_dict[alphabet[i]]=i+1
    return alpha_dict

def namescore(filename):
    total_score = 0
    alpha_dict = makealphadict()
    f = open(filename, 'r')
    text = f.read()
    print text
    names = re.findall(r'"(\w+)"', text)        
    names.sort()
    #this section of code creates a dictionary with the score of each name
    score_dict = {}
    for name in names:
        score_letters = 0
        score_rank = 0
        score = 0
        for i in range(len(name)):
            score_letters += alpha_dict[name[i]]
        score_rank = names.index(name)+1
        score = score_rank*score_letters
        score_dict[name] = score
    for finalname in score_dict:
        total_score+=score_dict[finalname]
        print total_score
        
            
        
        
  

def main():
  filename = (sys.argv[1])
  namescore(filename)



if __name__ == '__main__':
  main()
