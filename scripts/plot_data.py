#!/usr/bin/python3

import pandas as pd
import csv
import matplotlib.pyplot as plt

#root_path = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/csv_files/'
root_path = '/home/michele/Documents/robotica/csv_files/'

filename = root_path + 'calibration_tests/test_wrench_impedance.csv'

infile = pd.read_csv(filename, squeeze=True)

plt.plot(infile['wrench_z'][2500:4500]/10 * -1)
plt.ylabel('Wrench impendance')
plt.show()
