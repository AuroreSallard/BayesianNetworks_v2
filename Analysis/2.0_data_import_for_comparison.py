import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

#mz_path = "/nas/asallard/BN/Data/data4bn_2015.csv"
#mz_data = pd.read_csv(mz_path)

#mz_data = mz_data.fillna("stop")
#mz_data = mz_data[mz_data["Age"] >= 6]
#mz_data = mz_data[mz_data["activity10"] == "stop"]
#nb_max_activities = 9
#activities_columns = ["activity"+str(i) for i in range(nb_max_activities + 1)]

#chains = []
#for i in tqdm(range(len(mz_data)), desc = "MZ data exploration"):
#    row = mz_data.iloc[i][activities_columns]
#    chain = ""
#    for act_nb in range(nb_max_activities + 1):
#        act = row["activity" + str(act_nb)]
#        if act != "stop":
#            chain += act
#            chain += "-"
#        else:
#            break
#    if chain[-1] == "-":
#        chain = chain[:-1]
 #   chains.append(chain)

#mz_data["Activity_chain"] = chains
#mz_data.drop(columns = activities_columns, inplace = True)

#mz_data.to_csv("/nas/asallard/BN/Results/090821/MZ_act_chains_2015.csv", index = False)
#exit()

#eqasim_output_path = "/home/aurore/Servers/Switzerland/output_2010_new/"
#eq_households = pd.read_csv(eqasim_output_path + "households.csv", sep = ";")
#eq_persons = pd.read_csv(eqasim_output_path + "persons.csv", sep = ";")
#eq_trips = pd.read_csv(eqasim_output_path + "trips.csv", sep = ";")
#eq_persons = eq_persons[eq_persons["age"] >= 6]

#eq_persons = pd.merge(eq_persons, eq_households, on = "household_id", how = "inner")
#nb_max_activities = np.max(eq_trips["trip_id"].values.tolist())
#act_0 = eq_trips[eq_trips["trip_id"] == 0][["person_id", "preceding_purpose"]]
#act_0.rename(columns = {"preceding_purpose": "activity0"}, inplace = True)
#eq_persons = pd.merge(eq_persons, act_0, on = "person_id", how = "left")
#for i in range(nb_max_activities):  
#    colname = 'activity' + str(i+1)  
#    trips_act = eq_trips.groupby(['person_id'], as_index=False).nth(i).copy()[
#        ['person_id', 'following_purpose']
#    ].rename(columns={'following_purpose': colname}) 
#    eq_persons = pd.merge(eq_persons, trips_act, on='person_id', how='left')
#activities_columns = ["activity" + str(i) for i in range(nb_max_activities + 1)]
#eq_persons = eq_persons.fillna("stop")

#chains = []
#for i in tqdm(range(len(eq_persons)), desc = "Eqasim data exploration"):
#    row = eq_persons.iloc[i][activities_columns]
#    chain = ""
#    for act_nb in range(nb_max_activities + 1):
#        act = row["activity" + str(act_nb)]
#        if act == "shop":
#            act = "shopping"
#        if act != "stop":
#            chain += act
#            chain += "-"
#        else:
#            break
#    if chain == "":
#        chain = "home"
#    if chain[-1] == "-":
#        chain = chain[:-1]
#    chains.append(chain)
#eq_persons["Activity_chain"] = chains
#eq_persons = eq_persons[eq_persons["age"] >= 6]

bn_data_path = "/nas/asallard/BN/Results/010921/Net_9act_income.csv"

activities_columns = []

for i in range(1, 10):
    activities_columns.append("activity"+str(i))

bn_data = pd.read_csv(bn_data_path, encoding = "latin1")
bn_data["activity0"] = "home"

activities_columns.append("activity0")
chains = []
for i in tqdm(range(len(bn_data)), desc = "BN data exploration"):
    row = bn_data.iloc[i][activities_columns]
    chain = ""
    for act_nb in range(10):
        act = row["activity" + str(act_nb)]
        if act != "stop":
            chain += act
            chain += "-"
        else:
            break
    if chain[-1] == "-":
        chain = chain[:-1]
    chains.append(chain)

bn_data["Activity_chain"] = chains
bn_data.drop(columns = activities_columns, inplace = True)

bn_data.to_csv("/nas/asallard/BN/Results/010921/Net_9actchains_income.csv", index = False)
#eq_persons.to_csv("results/Eqasim_act_chains_2010_2017.csv", index = False)
#mz_data.to_csv("results/MZ_act_chains.csv", index = False)





