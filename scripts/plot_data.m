% plot data

% init instructions
clear;
clc;
path = '/home/michele/Desktop/tesi-robotica/csv_files/';


impedance_wrench = csvread(path + 'calibration_tests/test_wrench_impedance.csv',1,0)
position_wrench = csvread(path + 'calibration_tests/test_wrench_position.csv',1,0)

%wrench = csvread('/home/michele/Desktop/tesi-robotica/csv_files/kt/test_user/eros_1_wrench.csv',1,0)


