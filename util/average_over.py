"""
Average over the specified columns of the infile.
Write output to the outfile or to infile_out in output directory.
"""

import argparse
from datetime import datetime
from datetime import timedelta
import csv

parser = argparse.ArgumentParser()
parser.add_argument('-infile', '-in', required=True, help='Input file')
parser.add_argument('-timestamp', '-ts', required=True, help='Header of the column containing time. Case sensitive')
parser.add_argument('-format', nargs='*', required=True, help='Date format in the input file.')
parser.add_argument('-over', '-o', required=True, help='Average over this interval specified in hours:minutes:seconds')
parser.add_argument('-cols', '-c', nargs='*', help='Average these columns. Optional.')
parser.add_argument('-exclude', '-ex', nargs='*', help='Exclude these columns. '
                                                       'Space separated list of all non-numeric columns. '
                                                       'Optional')
parser.add_argument('-outfile', '-out', help='Name of the output file. Optional. '
                                             'Default is to write into datafile_out.csv')

args = parser.parse_args()
# Comfort messages
print('Reading input data from ' + args.infile)
print('Will average over ' + str(args.over))
print('the following columns ' + str(args.cols))
print('I will write the output to the file ' + str(args.outfile))
print('I will exclude these columns ' + str(args.exclude))
##################
infile = args.infile
timestamp = args.timestamp
ts_format = ' '.join(args.format)  # '%d/%m/%Y %H:%M:%S'
over = args.over.split(':')
delta = timedelta(hours=int(over[0]), minutes=int(over[1]), seconds=int(over[2]))
cols = args.cols
exclude = args.exclude

if args.outfile is None:
    outfile = '../output' + infile.split('.')[0] + '_out' + '.csv'
else:
    outfile = args.outfile

with open(infile) as raw_input, open(outfile, 'w', newline='') as out:
    inreader = csv.DictReader(raw_input)

    if cols is None:
        cols = list(filter(lambda x: x != timestamp, inreader.fieldnames))
    if exclude is not None:
        cols = list(filter(lambda x: x not in exclude, cols))

    outfieldnames = cols[:]  # Obtain a copy
    outfieldnames.insert(0, timestamp)
    writer = csv.DictWriter(out, fieldnames=outfieldnames)
    writer.writeheader()
    # Get the ball rolling
    row = next(inreader)
    ts = datetime.strptime(row[timestamp], ts_format)
    start = ts
    end = start + delta
    flag = True
    while flag:
        vals = {col: [float(row[col])] for col in cols}  # Make this empty if you don't want to include the first row.
        while ts < end:
            row = next(inreader, None)
            if row is not None:
                [vals[col].append(float(row[col])) for col in cols]
                ts = datetime.strptime(row[timestamp], ts_format)
            else:
                flag = False
                break

        if flag:
            row_out = {name: [] for name in outfieldnames}
            row_out[timestamp] = start.strftime(ts_format)
            for col in cols:
                if len(vals[col]) > 0:
                    row_out[col] = sum(vals[col]) / len(vals[col])
                else:
                    row_out[col] = sum(vals[col]) / len(vals[col])
            writer.writerow(row_out)

        start = ts
        end = start + delta
