from pomegranate import *
import numpy as np
import pandas as pd
import networkx as nx
import itertools as it
from BNutils import *
import math
#!/usr/bin/env python

import sys
sys.setrecursionlimit(50000)

# Import data, extract weights. Impossible to use 21 activities so we can restrict the study to 9 activities.
df = pd.read_csv("/nas/asallard/BN/Data/2015/data/data4bn_2015.csv")
#df = pd.read_csv("/home/aurore/Servers/BN/Data/2015/data/data4bn_2015.csv")
df = df[df["activity8"] == "stop"]
#df = df[np.logical_and(df["Week_day"] != "Saturday", df["Week_day"] != "Sunday")]
#df = df[:1000]

colnames = ["age_class", "Sex", "Marital_status", "household_size_class", "Work_time", "Week_day"] + ["activity"+str(k) for k in range(1,8)] + ["duration"+str(k) for k in range(1,8)]

X = df[colnames]
W = df["Person_weight"].values.tolist()

for cname in ["duration"+str(k) for k in range(1,8)]:
    df[cname] = [math.floor(d/60) for d in df[cname].values]
    df[cname] = [max(d, 111) for d in df[cname].values]

snames = colnames
statpop_nodes_indices = range(4)
sociodem_nodes_indices = range(5)
socioday_nodes_indices = range(6)
activities_nodes_indices = range(6, 13)
durations_nodes_indices = range(13, 20)
all_nodes_indices = range(len(snames))

# "Forbidden" edges: list of (parent, child) tuples. Doesn't work with state names, only with numbers.
exclude_all_to_statpop = list(it.product(all_nodes_indices, statpop_nodes_indices))
exclude_all_to_weekday = list(it.product(all_nodes_indices, [5]))
exclude_act_to_socio = list(it.product(activities_nodes_indices, socioday_nodes_indices))
exclude_dur_to_socio = list(it.product(durations_nodes_indices, socioday_nodes_indices))
exclude_dur_to_act = list(it.product(durations_nodes_indices, activities_nodes_indices))
exclude = exclude_all_to_statpop + exclude_all_to_weekday + exclude_act_to_socio + exclude_dur_to_socio + exclude_dur_to_act

include = [(k-7, k) for k in durations_nodes_indices]
include += [(5,6), (4,6)]
include += [(k, k+1) for k in activities_nodes_indices[:-1]]
include += [(k, k-8) for k in durations_nodes_indices[:-1]]
#include =[]

print([[colnames[c[0]], colnames[c[1]]] for c in include])
#print([[colnames[c[0]], colnames[c[1]]] for c in exclude])
#exit()

# Estimate network from the data
print("Starting to estimate the network")
model = BayesianNetwork.from_samples(X, algorithm = "greedy", max_parents=3, weights = W, state_names = snames, exclude_edges = exclude, include_edges = include)
print("Network estimated")

# Maybe the following line is not necessary, from the documentation I did not understand what is the purpose of the bake function.
model.bake()

# Plot the graph into a PDF. 
model.plot("/nas/asallard/BN/Results/21_10_08/Net_9act_durations5.pdf")
exit()
model = impute_dist_from_statpop(model)

# Sample using the function above
S = sample_from_BN(model, 800000)

dic_sampled = {}
for k in range(len(snames)):
    att = [s[k] for s in S]
    att_name = snames[k]
    dic_sampled[att_name] = att

df_sampled = pd.DataFrame.from_dict(dic_sampled)
df_sampled.to_csv("/nas/asallard/BN/Results/21_10_08/Net_9act_durations3.csv")


