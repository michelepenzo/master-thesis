#!/usr/bin/env python
# import pandas for reading csv file
import pandas as pd
from functions import filename_wrench_csv

# https://www.geeksforgeeks.org/python-math-operations-for-data-analysis/

# leggi i file csv delle due cartelle
# 	per ogni file wrench calcola il min, max, avg, std, tempo (0.1*#ripe)
# 	salva all'interno di un unico file csv

# reading csv file
s = pd.read_csv(filename_wrench_csv, squeeze=True)

n_values = s.count()

