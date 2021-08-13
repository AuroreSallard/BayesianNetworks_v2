import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

bn_chains = pd.read_csv("/nas/asallard/BN/Results/130821/Net_9actchains_forcing.csv")
eq_chains = pd.read_csv("/nas/asallard/BN/Results/090821/Eqasim_act_chains.csv")
mz_chains = pd.read_csv("/nas/asallard/BN/Results/090821/MZ_act_chains_2015.csv")
#old_chains = pd.read_csv("results/data/MZ_act_chains2010.csv")

bn_chains = bn_chains[(bn_chains["Week_day"] != "Sunday") & (bn_chains["Week_day"] != "Saturday")]
mz_chains = mz_chains[(mz_chains["Week_day"] != "Sunday") & (mz_chains["Week_day"] != "Saturday")]
#old_chains = old_chains[(old_chains["Week_day"] != "Sunday") & (old_chains["Week_day"] != "Saturday")]

bn_data = bn_chains["Activity_chain"].values.tolist()
eq_data = eq_chains["Activity_chain"].values.tolist()

mz_data = mz_chains["Activity_chain"].values.tolist()
mz_weights = mz_chains["weights"].values.tolist()

#old_data = old_chains["Activity_chain"].values.tolist()
#old_weights = old_chains["weights"].values.tolist()

total_weight = np.sum(mz_weights) #- np.sum(mz_chains[mz_chains["Activity_chain"] == "home"]["weights"].values.tolist())
#told_weight = np.sum(old_weights)

counts = {}
for ac in bn_data:
    if ac != None:
        if not ac in counts.keys():
            counts[ac] = [0,0,0,0]
        counts[ac][0] += 1

for ac in eq_data:
    if ac != None:
        if not ac in counts.keys():
            counts[ac] = [0,0,0,0]
        counts[ac][1] += 1

for i in range(len(mz_data)):
    ac = mz_data[i]
    if ac != None:
        if not ac in counts.keys() and ac != "home":
            counts[ac] = [0,0,0,0]
        counts[ac][2] += mz_weights[i] 

#for i in range(len(old_data)):
#    ac = old_data[i]
#    if ac != None:
#        if not ac in counts.keys() and ac != "home":
#            counts[ac] = [0,0,0,0]
#        counts[ac][3] += old_weights[i] 

act_chain = []
bn_count = []
eq_count = []
mz_count = []
#old_count = []

len_bn = len(bn_data) #- len(bn_chains[bn_chains["Activity_chain"] == "home"])
len_eq = len(eq_data) #- len(eq_chains[eq_chains["Activity_chain"] == "home"])

for k, v in counts.items():
    act_chain.append(k)
    bn_count.append(v[0] / len_bn * 100)
    eq_count.append(v[1] / len_eq * 100)
    mz_count.append(v[2] / total_weight * 100)
    #old_count.append(v[3] / told_weight * 100)

reversed_dic = {"Chain": act_chain, "BN Count": bn_count, "Eqasim Count": eq_count, "MZ Count": mz_count} 
df_act = pd.DataFrame.from_dict(reversed_dic)
df_act = df_act.sort_values(by=['MZ Count'], ascending=False)

#df_act.to_csv("results/data/BN_mix2_comp.csv", index = False)

top = 15
if not top is None:
    labels = df_act["Chain"].values.tolist()[:top]
    bn_values = df_act["BN Count"].values.tolist()[:top]
    eq_values = df_act["Eqasim Count"].values.tolist()[:top]
    mz_values = df_act["MZ Count"].values.tolist()[:top]
    #old_values = df_act["MZ old Count"].values.tolist()[:top]

x = np.arange(len(labels))
barWidth = 0.2  

r1 = np.arange(len(eq_values))
r2 = [r + barWidth for r in r1]
r3 = [r + barWidth for r in r2]
r4 = [r + barWidth for r in r3]

plt.rcParams['axes.facecolor'] = "#ffffff"
plt.rcParams['figure.figsize'] = (20,15)

fig, ax = plt.subplots()
fig.set_facecolor("#ffffff")

ax.bar(r1, mz_values, width = barWidth, label = "Microcensus 2015", edgecolor='white', color="#00205B")
ax.bar(r2, eq_values, width = barWidth, label = "Stat. matching", edgecolor='white', color="#D3D3D3")
ax.bar(r3, bn_values, width = barWidth, label = "BN forecast",edgecolor='white', color="#B3B3B3")
#ax.bar(r4, old_values, width = barWidth, label = "Microcensus 2010",edgecolor='white', color="#ABDBE3")

ylabel = "Percentage"
xlabel = "Activity chains"
plottitle = "Comparison between the microcensus, the Eqasim output and the Bayesian network output"

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel(ylabel)
ax.set_title(plottitle)
ax.set_xlabel(xlabel)
ax.set_xticks(x)

xticksrot = True

if xticksrot:
    ax.set_xticklabels(labels, rotation = 45, ha = "right")
else:
    ax.set_xticklabels(labels)

ax.legend(loc = 'lower right')
plt.xticks(rotation=30)
#fig.tight_layout()
plt.plot()
plt.savefig("/nas/asallard/BN/Results/130821/9act_weekday_forcing.png")



