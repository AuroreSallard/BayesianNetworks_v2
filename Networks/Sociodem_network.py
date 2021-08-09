from pomegranate import *
import numpy as np
import pandas as pd
import networkx as nx
import itertools as it
from BNutils import *

# Import data, extract weights
df = pd.read_csv("Data/data4bn_2015.csv")
X = df[["age_class", "Sex", "Work_time"]]
W = df["weights"].values.tolist()

snames = ["age_class", "Sex", "Work_time"]

# "Forbidden" nodes: list of (parent, child) tuples. Doesn't work with state names, only with numbers.
exclude = [(i, 0) for i in range(len(snames))] + [(i, 1) for i in range(len(snames))]

# Estimate network from the data
model = BayesianNetwork.from_samples(X, algorithm = "exact", weights = W, state_names = snames, exclude_edges = exclude)

# Maybe the following line is not necessary, from the documentation I did not understand what is the purpose of the bake function.
model.bake()

# Sample using the function above
S = BNutils.sample_from_BN(model, 1000000)
age_class_sampled = [s[0] for s in S]
sex_sampled = [s[1] for s in S]
work_sampled = [s[2] for s in S]
df_sampled = pd.DataFrame.from_dict({"age_class": age_class_sampled, "Sex": sex_sampled, "Work_time": work_sampled})

# Plot the graph into a PDF. 
model.plot("/nas/asallard/BN/Results/050821/BNtry01.pdf")

# Check if the distribution of sociodem is the same in the data and in the samples. From the 3 examples below it seems to be fine!
is_female = np.array(X["Sex"] == "Female")
W = np.array(W)
X_female = np.sum(W[is_female]) / np.sum(W)
S_female = len(df_sampled[df_sampled["Sex"] == "Female"]) / len(df_sampled)
print("Female: " + str(X_female) + " vs " + str(S_female))

is_retired = np.array(X["Work_time"] == "Retired")
X_female = np.sum(W[is_retired]) / np.sum(W)
S_female = len(df_sampled[df_sampled["Work_time"] == "Retired"]) / len(df_sampled)
print("Retired: " + str(X_female) + " vs " + str(S_female))

is_retired = np.array(X["Work_time"] == "Houseperson")
X_female = np.sum(W[is_retired]) / np.sum(W)
S_female = len(df_sampled[df_sampled["Work_time"] == "Houseperson"]) / len(df_sampled)
print("Houseperson: " + str(X_female) + " vs " + str(S_female))

