#!/usr/bin/python

import sys, getopt, csv, math

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('disjointIntervals.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('disjointIntervals.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print('Input file is "', inputfile)
   print('Output file is "', outputfile)

   intervals = []
   output = []
   results = []

   with open(inputfile, 'r') as file:
       reader = csv.reader(file)
       drawAction([])
       drawOutput([])
       for row in reader:
            action = row[0]
            start = row[1]
            end = row[2]
            newInterval = [start, end]
            drawAction(row)
            if len(intervals) == 0:
                newList = []
                newList.append(newInterval[0])
                newList.append(newInterval[1])
                intervals.append(newList)
                drawOutput(intervals)
                continue
            if action == 'add':
                output = addInterval(output, intervals, newInterval)
            elif action == 'remove':
                output = removeInterval(output, intervals, newInterval)
            intervals = output
            drawOutput(intervals)
            results.append(intervals)
            output = []


   with open(outputfile, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in results:
            csvwriter.writerow(row)

def isIntersect(a, b):
    left = max(a[0], b[0])
    right = max(a[1], b[1])
    return left <= right

def drawAction(row):
    print("Action >> ", row)

def drawOutput(intervals):
    print(" OUTPUT Intervals >> ", intervals)

def getList(start, end):
    newList = []
    newList.insert(0, start)
    newList.insert(1, end)
    return newList

def addInterval(output, intervals, newInterval):
    overlap = []
    flag = 0
    for interval in intervals:
        if len(interval) >= 2:
            if newInterval[0] > interval[1]:
                flag = 1
                output.append(getList(interval[0], interval[1]))
            elif interval[0] > newInterval[1]:
                flag = 0
                output.append(getList(newInterval[0], newInterval[1]))
                output.append(getList(interval[0], interval[1]))
            else:
                flag = 0
                overlap.append(getList(min(interval[0], newInterval[0]), max(interval[1], newInterval[1])))
                overlap.sort()
                output = getList(overlap[0][0], overlap[len(overlap) - 1][1])
        else:
            output = intervals

    if flag == 0:
        return output
    else:
        output.append(getList(newInterval[0], newInterval[1]))
        return output

def removeInterval(output, intervals, newInterval):
    for interval in intervals:
        if len(interval) >= 2:
            if isIntersect(interval, newInterval) :
                if interval[0] < newInterval[0]:
                    output.append(getList(interval[0], min(interval[1], newInterval[0])))
                if interval[1] > newInterval[1]:
                    output.append(getList(max(interval[0], newInterval[1]), interval[1]))
            else:
                output.append(getList(interval[0], interval[1]))
        else:
            output = intervals
    return output

if __name__ == "__main__":
   main(sys.argv[1:])