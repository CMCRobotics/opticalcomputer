import numpy as np
import json
import sys

filename = sys.argv[1]

with open(filename, 'r') as file:
	values = np.array(json.load(file))

values_list = (255/values).tolist()
with open('calibration_factors.json', 'w') as file:
	json.dump(values_list, file)
