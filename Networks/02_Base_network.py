from pomegranate import *
import numpy as np
import pandas as pd
import networkx as nx
import itertools as it
from BNutils import *

# Import data, extract weights
df = pd.read_csv("/nas/asallard/BN/Data/data4bn_2015.csv")

colnames = ["canton", "hhtype", "household_size_class", "municipality_type", "Work_time", "Sex", "Language","age_class", "Marital_status"] + ["activity"+str(k) for k in range(1, 22)]

X = df[colnames]
W = df["weights"].values.tolist()

snames = colnames
statpop_nodes_indices = [2, 3, 5, 7, 8]
sociodem_nodes_indices = range(9)
activities_nodes_indices = range(9, 30)
all_nodes_indices = range(len(snames))

# "Forbidden" edges: list of (parent, child) tuples. Doesn't work with state names, only with numbers.
exclude_all_to_statpop = list(it.product(all_nodes_indices, statpop_nodes_indices))
exclude_act_to_socio = list(it.product(activities_nodes_indices, sociodem_nodes_indices))
exclude = exclude_all_to_statpop + exclude_act_to_socio

include = [(i, i1) for i, i1 in list(zip(activities_nodes_indices[:-1], activities_nodes_indices[1:]))]

# Estimate network from the data
model = BayesianNetwork.from_samples(X, algorithm = "exact", weights = W, state_names = snames, exclude_edges = exclude, max_parents = 3, include_edges = include)

# Maybe the following line is not necessary, from the documentation I did not understand what is the purpose of the bake function.
model.bake()

# Plot the graph into a PDF. 
model.plot("/nas/asallard/BN/Results/090821/Net_base_1.pdf")

# Sample using the function above
#S = sample_from_BN(model, 1000000)

#dic_sampled = {}
#for k in range(len(snames)):
#    att = [s[k] for s in S]
#    att_name = snames[k]
#    dic_sampled[att_name] = att

#df_sampled = pd.DataFrame.from_dict(dic_sampled)
#df_sampled.to_csv("/nas/asallard/BN/Results/090821/Net_socio_sampled_1.csv")


