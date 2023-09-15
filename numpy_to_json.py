import sys
numpy_file = sys.argv[1]
assert numpy_file[-4:] == ".npy"

VOL_NAME = numpy_file[:-4] 

import numpy as np
import jdata as jd
import json

vol = np.load(numpy_file)

# serialize volume
vol_encoded = jd.encode(vol, {'compression':'zlib','base64':1})
# manipulate binary string format so that it can be turned into json
vol_encoded["_ArrayZipData_"] = str(vol_encoded["_ArrayZipData_"])[2:-1]

# Load boilerplate json to dict
with open("colin27.json") as f:
    simjson = json.load(f) # the json dict that goes into simulation
    
# Replaced volume (and other attributes)
simjson["Shapes"] = vol_encoded
simjson["Session"]["ID"] = VOL_NAME 

# Save new dict to json file
with open(f"{VOL_NAME}.json","w") as f: 
    json.dump(simjson, f, indent=4)

print(f"Done writing serialized json config file at {VOL_NAME}.json")
