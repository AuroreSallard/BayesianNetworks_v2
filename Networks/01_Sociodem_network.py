from pomegranate import *
import numpy as np
import pandas as pd
import networkx as nx
import itertools as it
from BNutils import *

# Import data, extract weights
df = pd.read_csv("/nas/asallard/BN/Data/data4bn_2015.csv")
X = df[["canton", "hhtype", "household_size_class", "municipality_type", "Work_time", "Sex", "Language","age_class", "Marital_status"]]
W = df["weights"].values.tolist()

snames = ["canton", "hhtype", "household_size_class", "municipality_type", "Work_time", "Sex", "Language","age_class", "Marital_status"]

# "Forbidden" edges: list of (parent, child) tuples. Doesn't work with state names, only with numbers.
statpop_nodes_indices = [2, 3, 5, 7, 8]
#exclude = [(i,j) for i,j in list(zip(range(len(snames)), statpop_nodes_indices))]
exclude = list(it.product(range(len(snames)), statpop_nodes_indices))
print(exclude)

# Estimate network from the data
model = BayesianNetwork.from_samples(X, algorithm = "exact", weights = W, state_names = snames, exclude_edges = exclude)

# Maybe the following line is not necessary, from the documentation I did not understand what is the purpose of the bake function.
model.bake()

# Plot the graph into a PDF. 
model.plot("/nas/asallard/BN/Results/090821/Net_socio_2.pdf")

# Sample using the function above
#S = sample_from_BN(model, 1000000)

#dic_sampled = {}
#for k in range(len(snames)):
#    att = [s[k] for s in S]
#    att_name = snames[k]
#    dic_sampled[att_name] = att

#df_sampled = pd.DataFrame.from_dict(dic_sampled)
#df_sampled.to_csv("/nas/asallard/BN/Results/090821/Net_socio_sampled_1.csv")


