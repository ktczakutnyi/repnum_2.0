###############################################################################
# This script is used to generate calibration report numbers for the
# calibrations performed at OEMA.
#
# Author:  K. Herminghuysen
# Author:  K. Zakutnyi
#
# Language:  Python 2.5
# Language:  Python 3
#
# Revision History:
#
# September, 2009:
#   - Version 1.0
# March, 2026:
#   - Version 2.0
#
###############################################################################

import os
import shutil
import time

<<<<<<< codex/update-report-number-generation-process-99aauc
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(BASE_DIR, 'repnum.txt')
TARGET_FILE = os.path.join(BASE_DIR, 'repnum2.txt')
=======
SOURCE_FILE = 'repnum.txt'
TARGET_FILE = 'repnum2.txt'
>>>>>>> main


def get_current_date_time():
    (yyyy, mm, dd, hr, minute, sec, wday, yday, isdst) = time.localtime()
    cur_date = str(mm).zfill(2) + '-' + str(dd).zfill(2) + '-' + str(yyyy)
    cur_time = str(hr).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(sec).zfill(2)
    return cur_date, cur_time


def read_last_report_number(file_path):
    if not os.path.exists(file_path):
        return 0

    last_number = 0
    with open(file_path, 'r') as report_file:
        for line in report_file:
            word = line.split()
            if len(word) >= 3 and word[2].isdigit():
                last_number = int(word[2])
    return last_number


def copy_existing_report_data(source_path, target_path):
    if os.path.exists(target_path):
        return

    if os.path.exists(source_path):
        shutil.copyfile(source_path, target_path)
    else:
        open(target_path, 'a').close()


def get_next_report_number(current_number):
    return current_number + 1


def append_report_number(file_path, report_number):
    cur_date, cur_time = get_current_date_time()
    with open(file_path, 'a') as report_file:
        report_file.write('%10s  %8s %6d\n' % (cur_date, cur_time, report_number))


def main():
    print('\nCalibration Report Number Generator - Version 2.0\n')
    print('How this works:')
    print('- Existing report history is copied from repnum.txt to repnum2.txt once (if needed).')
    print('- Press Enter to generate and save the next report number.')
    print('- Type q and press Enter to quit, or close the window to exit.\n')

    copy_existing_report_data(SOURCE_FILE, TARGET_FILE)
    report_number = read_last_report_number(TARGET_FILE)

    while True:
<<<<<<< codex/update-report-number-generation-process-99aauc
        try:
            user_input = input('Press Enter for next report number or type q to exit: ').strip().lower()
        except EOFError:
            print('\nNo input stream detected. Exiting program.')
            break
=======
        user_input = input('Press Enter for next report number or type q to exit: ').strip().lower()
>>>>>>> main

        if user_input == 'q':
            break

        if user_input == '':
            report_number = get_next_report_number(report_number)
            append_report_number(TARGET_FILE, report_number)
            print('\nThe next report number in the sequence is %d\n' % report_number)
            continue

        print("Please press Enter to generate the next number, or type 'q' to quit.")


if __name__ == '__main__':
    main()
