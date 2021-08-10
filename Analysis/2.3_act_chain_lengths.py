import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

bn_chains = pd.read_csv("results/data/BN_mix2_actchains.csv")
eq_chains = pd.read_csv("results/data/Eqasim_act_chains_2010_2017.csv")
mz_chains = pd.read_csv("results/data/MZ_act_chains.csv")
old_chains = pd.read_csv("results/data/MZ_act_chains2010.csv")

bn_chains = bn_chains[(bn_chains["Week_day"] != "Sunday") & (bn_chains["Week_day"] != "Saturday")]
mz_chains = mz_chains[(mz_chains["Week_day"] != "Sunday") & (mz_chains["Week_day"] != "Saturday")]
#eq_chains = eq_chains[(eq_chains["Week_day"] != "Sunday") & (eq_chains["Week_day"] != "Saturday")]
old_chains = old_chains[(old_chains["Week_day"] != "Sunday") & (old_chains["Week_day"] != "Saturday")]

bn_data = bn_chains["Activity_chain"].values.tolist()
eq_data = eq_chains["Activity_chain"].values.tolist()

mz_data = mz_chains["Activity_chain"].values.tolist()
mz_weights = mz_chains["weights"].values.tolist()

old_data = old_chains["Activity_chain"].values.tolist()
old_weights = old_chains["weights"].values.tolist()

total_weight = np.sum(mz_weights) #- np.sum(mz_chains[mz_chains["Activity_chain"] == "home"]["weights"].values.tolist())
told_weight = np.sum(old_weights)

counts = {}
for ac in bn_data:
    l = len(ac.split("-"))
    if not l in counts.keys():
        counts[l] = [0,0,0,0]
    counts[l][0] += 1

for ac in eq_data:
    l = len(ac.split("-"))
    if not l in counts.keys():
        counts[l] = [0,0,0,0]
    counts[l][1] += 1

for i in range(len(mz_data)):
    l = len(mz_data[i].split("-"))
    if not l in counts.keys():
        counts[l] = [0,0,0,0]
    counts[l][2] += mz_weights[i] 

for i in range(len(old_data)):
    l = len(old_data[i].split("-"))
    if not l in counts.keys():
        counts[l] = [0,0,0,0]
    counts[l][3] += old_weights[i] 

act_chain = []
bn_count = []
eq_count = []
mz_count = []
old_count = []

for k, v in counts.items():
    act_chain.append(k)
    bn_count.append(v[0] / len(bn_data) * 100)
    eq_count.append(v[1] / len(eq_data) * 100)
    mz_count.append(v[2] / total_weight * 100)
    old_count.append(v[3] / told_weight * 100)

reversed_dic = {"Chain length": act_chain, "BN Count": bn_count, "Eqasim Count": eq_count, "MZ Count": mz_count, "MZ old Count": old_count} 
df_act = pd.DataFrame.from_dict(reversed_dic)
df_act = df_act.sort_values(by=['MZ Count'], ascending=False)


#df_act.to_csv("results/data/Act_chain_comparison_statpop.csv", index = False)

top = 15
if not top is None:
    labels = df_act["Chain length"].values.tolist()[:top]
    bn_values = df_act["BN Count"].values.tolist()[:top]
    eq_values = df_act["Eqasim Count"].values.tolist()[:top]
    mz_values = df_act["MZ Count"].values.tolist()[:top]
    old_values = df_act["MZ old Count"].values.tolist()[:top]

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
ax.bar(r4, old_values, width = barWidth, label = "Microcensus 2010",edgecolor='white', color="#ABDBE3")

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
plt.savefig("results/figures/BN_mix2_actchains_3.png")


