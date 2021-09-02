import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

def fill(s, length, char = " "):
    if len(s) < length:
        s += char*(length - len(s))
    return s

bn_data = pd.read_csv("/nas/asallard/BN/Results/010921/Net_9actchains_income.csv")
mz_data = pd.read_csv("/nas/asallard/BN/Data/data4bn_2015.csv")

sociodem_of_interest = ["age_class", "Sex", "Work_time", "nb_cars"]

for socio in sociodem_of_interest:
    print(fill(socio, 80, char = "_"))

    bn_val = set(bn_data[socio].values.tolist())
    mz_val = set(bn_data[socio].values.tolist())
    all_val = list(bn_val.union(mz_val))
    maxl = np.max([len(str(v)) for v in all_val])

    print(fill("", maxl + 5) + fill("BN", 10) + fill("MZ", 10) + "relative difference")

    for v in all_val:
        bn_current = bn_data[bn_data[socio] == v]
        mz_current = mz_data[mz_data[socio] == v]
        bn_score = len(bn_current) / len(bn_data) * 100
        mz_score = np.sum(mz_current["Person_weight"]) / np.sum(mz_data["Person_weight"]) * 100
        rel_diff = (bn_score - mz_score) / mz_score * 100

        w = str(v)
        b = '{:.2f}'.format(bn_score)
        m = '{:.2f}'.format(mz_score)
        r = '{:.2f}'.format(rel_diff)

        print(fill(w, maxl + 5, char = " ") + fill(b, 10) + fill(m, 10) + r)


    print("\n")

    
    




