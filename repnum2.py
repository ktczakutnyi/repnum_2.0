###############################################################################
# This script is used to generate calibration report numbers for the
# calibrations performed at OEMA.
#
# Author:  K. Herminghuysen
#
# Language:  Python 2.5
#
# Revision History:
#
# September, 2009:
#   - Version 1.0
#
###############################################################################

import time

print('\nCalibration Report Number Generator - Version 1.0\n')

(yyyy, mm, dd, hr, min, sec, wday, yday, isdst) = time.localtime()
cur_date = str(mm).zfill(2) + '-' + str(dd).zfill(2) + '-' + str(yyyy)
cur_time = str(hr).zfill(2) + ':' + str(min).zfill(2) + ':' + str(sec).zfill(2)

FILE = open('repnum.txt', 'r+')

for line in FILE:
   word = line.split()
   date = word[0]
   time = word[1]
   rnum = int(word[2])

rnum += 1
print('\nThe next report number in the sequence is %d\n' % (rnum))
FILE.write('%10s  %8s %6d\n' % (cur_date, cur_time, rnum))
FILE.close()

ans = input('\nPress any key to exit.\n')
