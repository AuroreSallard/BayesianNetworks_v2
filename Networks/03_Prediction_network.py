from pomegranate import *
import numpy as np
import pandas as pd
import networkx as nx
import itertools as it
from BNutils import *

# Import data, extract weights. Impossible to use 21 activities so we can restrict the study to 9 activities.
df = pd.read_csv("/nas/asallard/BN/Data/data/data4bn_2010.csv")
df = df[df["activity10"] == "stop"]
#df = df[np.logical_and(df["Week_day"] != "Saturday", df["Week_day"] != "Sunday")]

colnames = ["canton", "hhtype", "household_size_class", "municipality_type", "Work_time", "Sex", "Language","age_class", "Marital_status",  "hhl_income10", "nb_bikes", "nb_cars", "Week_day"] + ["activity"+str(k) for k in range(1,10)]

X = df[colnames]
W = df["Person_weight"].values.tolist()

snames = colnames
statpop_nodes_indices = [2, 3, 5, 7, 8]
sociodem_nodes_indices = range(12)
socioday_nodes_indices = range(13)
activities_nodes_indices = range(13, 33)
all_nodes_indices = range(len(snames))

# "Forbidden" edges: list of (parent, child) tuples. Doesn't work with state names, only with numbers.
exclude_all_to_statpop = list(it.product(all_nodes_indices, statpop_nodes_indices))
exclude_act_to_socio = list(it.product(activities_nodes_indices, socioday_nodes_indices))
exclude = exclude_all_to_statpop + exclude_act_to_socio

#include = [(9, i) for i in activities_nodes_indices]

# Estimate network from the data
model = BayesianNetwork.from_samples(X, algorithm = "exact", weights = W, state_names = snames, exclude_edges = exclude, max_parents = 3, include_edges = [])

# Maybe the following line is not necessary, from the documentation I did not understand what is the purpose of the bake function.
model.bake()

# Plot the graph into a PDF. 
model.plot("/nas/asallard/BN/Results/060921/Net_9act_predict.pdf")

#for s in model.states:
#    if s.name == "age_class":
#        print(s.distribution)

model = impute_dist_from_statpop(model)

#for s in model.states:
#    if s.name == "age_class":
#        print(s.distribution)

# Sample using the function above
S = sample_from_BN(model, 800000)

dic_sampled = {}
for k in range(len(snames)):
    att = [s[k] for s in S]
    att_name = snames[k]
    dic_sampled[att_name] = att

df_sampled = pd.DataFrame.from_dict(dic_sampled)
df_sampled.to_csv("/nas/asallard/BN/Results/060921/Net_9act_predict.csv")


