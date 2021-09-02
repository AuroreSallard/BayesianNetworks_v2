import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

df = pd.read_csv("/nas/asallard/BN/Data/target_persons0109.csv")
df["age_class"] = np.digitize(df["Age"], range(6,100,3))
s2 = df.groupby("age_class")["Person_weight"].sum() / np.sum(df["Person_weight"]) * 100

statpop = pd.read_csv("/nas/asallard/BN/Data/statpop.csv")
statpop["age_class"] =  np.digitize(statpop["age"], range(6,100,3))
statpop = statpop[statpop["age_class"] > 0]
s1 = statpop.groupby("age_class")["person_id"].count() / len(statpop) * 100    

ages = pd.DataFrame([s1, s2])
ages = ages.transpose()
ages.columns = ["Statpop", "MZ"]
ages["diff"] = (ages["Statpop"] - ages["MZ"]) / ages["MZ"] * 100

print(ages)


