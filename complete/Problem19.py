#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 19

import sys
import re
import math

"""
You are given the following information, 
but you may prefer to do some research for yourself.

1 Jan 1900 was a Monday.
Thirty days has September, April, June and November.
All the rest have thirty-one,
Saving February alone,
Which has twenty-eight, rain or shine.
And on leap years, twenty-nine.

A leap year occurs on any year evenly divisible by 4, 
but not on a century unless it is divisible by 400.
How many Sundays fell on the first of the month during 
the twentieth century (1 Jan 1901 to 31 Dec 2000)?




"""

class date:
    def __init__(self):
        self.dayname = 1
        self.day = 1
        self.month = 'Jan'
        self.year = 1901
        self.suncount = 0
        self.dayweek = {1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat', 7:'Sun'}
        self.monthdays = {'Jan': 31, 'Feb' : 28, 'Mar' : 31,\
        'Apr' : 30, 'May' : 31, 'Jun':30, 'Jul':31, 'Aug':31,\
        'Sep':30, 'Oct':31, 'Nov':30, 'Dec':31}
        self.monthlist = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',\
        'Sep', 'Oct', 'Nov', 'Dec']
        
    def leapyear(self):
        if self.year%4 ==0 and self.year%100 ==0:
            if self.year%400 ==0:
                leap=True
            else:
                leap=False
        elif self.year%4 ==0 and self.year%100 !=0:
            leap=True
        else:
            leap=False
        return leap
    def count(self):
        if self.dayname==7 and self.day == 1:
            self.suncount += 1
            print self.suncount
    def Advance_weekday(self):
        if self.dayname==7:
            self.dayname = 1
        else:
            self.dayname +=1
    def Advance_day(self):
        self.day+=1
    def Advance_monthyear(self):
        numdays = self.monthdays[self.month]
        month = self.monthlist.index(self.month)
        if self.month == 'Feb' and self.leapyear():
            numdays+=1
        if self.day > numdays and self.month=='Dec':
            self.day = 1
            self.year +=1
            self.month = 'Jan'
        elif self.day > numdays and self.month!='Dec':
            self.day = 1
            month+=1
            self.month = self.monthlist[month]
    def printdate(self):
        print self.dayweek[self.dayname], self.month, self.day, ',', self.year

def main():
#    number = long(sys.argv[1])
    P19 = date()
    while P19.year < 2001:
        P19.Advance_weekday()
        P19.Advance_day()
        P19.Advance_monthyear()
        P19.printdate()
        P19.count()

    print P19.suncount
    print P19.monthlist
    print 1200/7
    



if __name__ == '__main__':
  main()
