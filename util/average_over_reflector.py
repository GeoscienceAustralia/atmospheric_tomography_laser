from datetime import datetime
from datetime import timedelta
import csv

infile = str(input("Please enter name of the input data file : ")).strip()
start = str(input("Please enter the start time in the format DD/MM/YYYY Hour:Min:Sec AM/PM : ")).strip()
endtime = str(input("Please enter the end time in the format DD/MM/YYYY Hour:Min:Sec AM/PM : ")).strip()
delta = int(input("Please enter the averaging interval in minutes : "))
num_reflectors = int(input("Please enter the number of reflectors: "))

#format = '%d/%m/%Y %I:%M:%S %p'
format = '%d/%m/%Y %H:%M:%S'
start = datetime.strptime(start, format)
endtime = datetime.strptime(endtime, format)
delta = timedelta(minutes=delta)
intervals = []
ts = start
while ts <=endtime:
  intervals.append(ts)
  ts = ts + delta

vals = {k:{i:[0] for i in range(1, num_reflectors + 1)} for k in intervals}
with open(infile) as input:
  inreader = csv.DictReader(input)
  for row in inreader:
    ts = datetime.strptime(row['Date'], format)
    id = int(row['Reflector']) 
    earlier_ts = list(filter(lambda x : x < ts, intervals))
    reading = float(row['PPM'])
    vals[earlier_ts[-1]][id].append(reading)

fieldnames = ['Date']
[fieldnames.append("".join(("R", str(i)))) for i in range(1, num_reflectors + 1)]
#fieldnames = ['Date','R1','R2','R3','R4','R5','R6','R7']
row = {}
with open("output.csv", "w", newline='') as out:
  writer = csv.DictWriter(out, fieldnames=fieldnames)
  writer.writeheader()  
  for key in intervals:
    row['Date'] = key.strftime(format)
    val = vals[key]
    for reflector, readings in val.items():
      ref = 'R' + str(reflector)
      if sum(readings) > 0:
        row[ref] = str(sum(readings) / (len(readings) - 1))
      else:
        row[ref] = " "
    writer.writerow(row)  
    
print("\n Output has been written to output.csv.")
  