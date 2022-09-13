import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

##### User Input  #####
file_path = "./example_ct_scan/y_model_vs_y_real.xls"
n_features = 4
##### User Input #####

data = pd.read_excel(file_path)
y_real = data["y_Real"]
y_model = data["y_Model"]

# count number of data points & features
n_data = len(y_real)

# compute RMSE
rmse = np.sqrt(mean_squared_error(y_real, y_model))

# compute R^2 values
r2 = r2_score(y_real, y_model)
r2_adjusted = 1-(1-r2)*(n_data-1)/(n_data-n_features-1)

# print results
print("RMSE = ", rmse)
print("R2 = ", r2)
print("R2_adjusted = ", r2_adjusted)
