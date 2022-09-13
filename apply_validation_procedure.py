import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import t
from math import *
from scipy.optimize import fsolve
from sklearn.linear_model import LinearRegression

##### User Input  #####
file_path = "./example_ct_scan/y_model_vs_y_real.xls"
fraction_of_data = 1
alpha = 0.01
##### User Input #####

def q(x, x_vec):
    n = len(x_vec)
    return np.sqrt((n + 1) / n + (x - np.mean(x_vec))**2 /
                   np.sum((x_vec - np.mean(x_vec))**2))


def s1(x_vec, y_vec, m, b):
    if len(x_vec) == len(y_vec):
        n = len(x_vec)
        pred_vec = m * x_vec + b
        return np.sqrt(sum((y_vec - pred_vec)**2) / (n - 2))


def LB_ConfInf(x, x_vec, y_vec, alpha, m, b):
    if len(x_vec) == len(y_vec):
        n = len(x_vec)
        t_val = t.ppf(1 - alpha, df=(n - 2))
        LB = m * x + b - s1(x_vec, y_vec, m, b) * t_val * q(x, x_vec)
        return LB


def UB_ConfInf(x, x_vec, y_vec, alpha, m, b):
    if len(x_vec) == len(y_vec):
        n = len(x_vec)
        t_val = t.ppf(1 - alpha, df=(n - 2))
        UB = m * x + b + s1(x_vec, y_vec, m, b) * t_val * q(x, x_vec)
        return UB


def lowerDifference(x):
    return LB_ConfInf(
        x, x_vec=real_val, y_vec=pred_val, alpha=alpha, m=m1,
        b=b1) - LB_ConfInf(
            x, x_vec=pred_val, y_vec=real_error, alpha=alpha, m=1, b=0)


def upperDifference(x):
    return UB_ConfInf(
        x, x_vec=real_val, y_vec=pred_val, alpha=alpha, m=m1,
        b=b1) - UB_ConfInf(
            x, x_vec=real_val, y_vec=pred_val, alpha=alpha, m=1, b=0)


def allowedRange(m):
    lb = fsolve(lowerDifference, x0=0)[0]
    ub = fsolve(upperDifference, x0=0)[0]
    if m < 1:
        if lb >= ub:
            x = [ub, lb]
            print("Allowed model range: %s" % x)
        else:
            print("No allowed range.")
    else:
        if lb <= ub:
            x = [lb, ub]
            print("Allowed model range : %s" % x)
        else:
            print("No allowed range.")
    return [lb, ub]


##### Load external data #####

data = pd.read_excel(file_path)
data = data.sample(int(fraction_of_data * len(data)))

real_val = data["y_Real"].to_numpy()  # real values
pred_val = data["y_Model"].to_numpy()  # predicted values

real_val = np.reshape(real_val, (len(real_val), 1))
pred_val = np.reshape(pred_val, (len(pred_val), 1))

##### Model validation via confidence intervals  ######

# confidence interval for perfect regression line

real_error = (1 - alpha / 2) * real_val
real_mean = np.mean(real_val)

LB_opt = LB_ConfInf(x=real_val,
                    x_vec=real_val,
                    y_vec=real_error,
                    alpha=alpha,
                    m=1,
                    b=0)
UB_opt = UB_ConfInf(x=real_val,
                    x_vec=real_val,
                    y_vec=real_error,
                    alpha=alpha,
                    m=1,
                    b=0)

# confidence interval for regression

reg = LinearRegression().fit(real_val, pred_val)

m1 = reg.coef_[0]
b1 = reg.intercept_

pred_line = m1 * real_val + b1

LB_pred = LB_ConfInf(x=real_val,
                     x_vec=real_val,
                     y_vec=pred_val,
                     alpha=alpha,
                     m=m1,
                     b=b1)
UB_pred = UB_ConfInf(x=real_val,
                     x_vec=real_val,
                     y_vec=pred_val,
                     alpha=alpha,
                     m=m1,
                     b=b1)

# plot confidence interval for regression
plt.plot(real_val, real_val, 'g', label="regression (ideal)")
plt.plot(real_val, LB_opt, 'lightgreen', label="confidence band (ideal)")
plt.plot(real_val, UB_opt, 'lightgreen')
plt.plot(real_val,
         pred_val,
         'ro',
         alpha=1,
         fillstyle='none',
         label="prediction")
plt.plot(real_val, pred_line, 'r', label="regression (prediction)")
plt.plot(real_val, LB_pred, 'lightcoral', label="confidence band (prediction)")
plt.plot(real_val, UB_pred, 'lightcoral')
plt.legend()

# calculate allowed range for model
[lb, ub] = allowedRange(m1)
plt.show()
