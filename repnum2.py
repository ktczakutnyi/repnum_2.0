###############################################################################
# This script is used to generate calibration report numbers for the
# calibrations performed at OEMA.
#
# Author:  K. Herminghuysen
# Author:  K. Zakutnyi
#
# Language:  Python 2.5
# Language:  Python 2.5
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
import errno
import sys

if sys.version_info[0] < 3:
    import __builtin__ as builtins
else:
    import builtins

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(BASE_DIR, 'repnum.txt')
TARGET_FILE = os.path.join(BASE_DIR, 'repnum2.txt')
LOCK_FILE = TARGET_FILE + '.lock'
LOCK_TIMEOUT_SECONDS = 30
LOCK_STALE_SECONDS = 120


def get_current_date_time():
    est_seconds = time.time() - (5 * 60 * 60)
    (yyyy, mm, dd, hr, minute, sec, wday, yday, isdst) = time.gmtime(est_seconds)
    cur_date = str(mm).zfill(2) + '-' + str(dd).zfill(2) + '-' + str(yyyy)
    cur_time = str(hr).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(sec).zfill(2)
    return cur_date, cur_time


def read_last_report_number(file_path):
    if not os.path.exists(file_path):
        return 0

    last_number = 0
    report_file = open(file_path, 'r')
    try:
        for line in report_file:
            word = line.split()
            if len(word) >= 3 and word[2].isdigit():
                last_number = int(word[2])
    finally:
        report_file.close()
    return last_number


def copy_existing_report_data(source_path, target_path):
    if os.path.exists(target_path):
        return

    if os.path.exists(source_path):
        shutil.copyfile(source_path, target_path)
    else:
        open(target_path, 'a').close()


def write_lock_owner(lock_fd):
    try:
        lock_owner = str(os.getpid())
        try:
            os.write(lock_fd, lock_owner.encode('utf-8'))
        except AttributeError:
            os.write(lock_fd, lock_owner)
    except Exception:
        pass


def try_create_lock(lock_path):
    try:
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except OSError:
        if getattr(sys.exc_info()[1], 'errno', None) == errno.EEXIST:
            return False
        raise

    try:
        write_lock_owner(lock_fd)
    finally:
        os.close(lock_fd)
    return True


def is_lock_stale(lock_path, stale_seconds):
    try:
        lock_age_seconds = time.time() - os.path.getmtime(lock_path)
    except OSError:
        return False
    return lock_age_seconds > stale_seconds


def acquire_file_lock(lock_path, timeout_seconds, stale_seconds):
    start_time = time.time()
    while True:
        if try_create_lock(lock_path):
            return True

        if is_lock_stale(lock_path, stale_seconds):
            try:
                os.remove(lock_path)
            except OSError:
                pass

        if (time.time() - start_time) >= timeout_seconds:
            return False

        time.sleep(0.2)


def release_file_lock(lock_path):
    try:
        os.remove(lock_path)
    except OSError:
        pass


def get_next_report_number(current_number):
    return current_number + 1


def append_report_number(file_path, report_number):
    cur_date, cur_time = get_current_date_time()
    report_file = open(file_path, 'a')
    try:
        report_file.write('%10s  %8s %6d\n' % (cur_date, cur_time, report_number))
    finally:
        report_file.close()


def get_and_append_next_report_number(source_path, target_path, lock_path):
    if not acquire_file_lock(lock_path, LOCK_TIMEOUT_SECONDS, LOCK_STALE_SECONDS):
        return None

    try:
        copy_existing_report_data(source_path, target_path)
        current_number = read_last_report_number(target_path)
        next_number = get_next_report_number(current_number)
        append_report_number(target_path, next_number)
        return next_number
    finally:
        release_file_lock(lock_path)


def get_last_saved_report_number(source_path, target_path, lock_path):
    if not acquire_file_lock(lock_path, LOCK_TIMEOUT_SECONDS, LOCK_STALE_SECONDS):
        return None

    try:
        copy_existing_report_data(source_path, target_path)
        return read_last_report_number(target_path)
    finally:
        release_file_lock(lock_path)


def get_text_input(prompt):
    if hasattr(builtins, 'raw_input'):
        return builtins.raw_input(prompt)
    return builtins.input(prompt)


def read_windows_key(msvcrt_module):
    if hasattr(msvcrt_module, 'getwch'):
        return msvcrt_module.getwch()

    key = msvcrt_module.getch()
    if not key:
        return ''
    try:
        return key.decode('utf-8', 'ignore')
    except Exception:
        return key


def read_user_command():
    try:
        return get_text_input('Press Enter for next report number or type q to exit: ').strip().lower()
    except EOFError:
        if os.name != 'nt':
            print('\nNo interactive input stream detected. Exiting program.')
            return 'q'

        print('\nStandard input is unavailable. Using keyboard mode.')
        print('Press Enter to generate a number, or press q to quit.')

        import msvcrt

        while True:
            key = read_windows_key(msvcrt).lower()
            if key in ('\r', '\n'):
                print('')
                return ''
            if key == 'q':
                print('q')
                return 'q'


def main():
    print('\nCalibration Report Number Generator - Version 2.0\n')
    print('How this works:')
    print('- Existing report history is copied from repnum.txt to repnum2.txt once (if needed).')
    print('- Press Enter to generate and save the next report number.')
    print('- Type q and press Enter to quit, or close the window to exit.\n')

    report_number = get_last_saved_report_number(SOURCE_FILE, TARGET_FILE, LOCK_FILE)
    if report_number is None:
        print('Unable to acquire shared lock at startup. Please restart the program.')
        return

    print('Working log file: %s' % TARGET_FILE)
    print('Last saved report number: %d\n' % report_number)

    while True:
        user_input = read_user_command()

        if user_input == 'q':
            break

        if user_input == '':
            next_report_number = get_and_append_next_report_number(SOURCE_FILE, TARGET_FILE, LOCK_FILE)
            if next_report_number is None:
                print('\nUnable to acquire shared lock. Please try again.\n')
                continue
            print('\nThe next report number in the sequence is %d\n' % next_report_number)
            continue

        print("Please press Enter to generate the next number, or type 'q' to quit.")

    print('Program closed.')


if __name__ == '__main__':
    main()
