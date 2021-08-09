from pomegranate import *
import numpy as np
import pandas as pd
import networkx as nx
import itertools as it

# Copied and slightly modified from https://github.com/jmschrei/pomegranate/blob/master/pomegranate/BayesianNetwork.pyx
def sample_from_BN(model, nsamples = 1, evidences = [{}], min_prob=0.01,random_state=None):
    model.bake()
    samples = []
    node_dict = {node.name:node.distribution for node in model.states}

    G = nx.DiGraph()
    for state in model.states:
        G.add_node(state)

    for parent, child in model.edges:
        G.add_edge(parent, child)

    iter_ = it.cycle(enumerate(nx.topological_sort(G)))

    for evidence in evidences:
        count = 0
        safeguard = 0
        state_dict = evidence.copy()
        args = {node_dict[k]:v for k,v in evidence.items()}

        while count < nsamples:
            safeguard +=1
            if safeguard > nsamples/min_prob:
                # raise if P(X|Evidence) < 1%
                raise Exception('Maximum iteration limit. Make sure the state configuration hinted at by evidence is reasonably reachable for this network or lower min_prob')

                # Rejection sampling
                # If the predicted value is not the one given in evidence, we start over until we reach the expected number of samples by evidence
            j, node = iter_.__next__()
            name = node.name

            if node.distribution.name == "DiscreteDistribution":
                if name in evidence :
                    val = evidence[name]
                else :
                    val = node.distribution.sample(random_state=random_state)

            else :
                val = node.distribution.sample(args,random_state=random_state)

            # rejection sampling
            if node.distribution.name != "DiscreteDistribution" and (name in evidence):
                if evidence[name] != val:
                    # make sure we start with the first node in the topoplogical order
                    [iter_.__next__() for i in range(model.node_count() - j - 1)]
                    args = {node_dict[k]:v for k,v in evidence.items()}
                    state_dict = evidence.copy()
                    continue

            else:
                state_dict[name] = val
                args[node_dict[name]] = val

            if (j + 1) == model.node_count():
                samples.append(state_dict)
                args = {node_dict[k]:v for k,v in evidence.items()}
                state_dict = evidence.copy()
                count += 1

        # make sure we start with the first node in the topoplogical order
        [iter_.__next__() for i in range(model.node_count() - j - 1)]

    keys = node_dict.keys()
    return  numpy.array([[r[k] for k in keys ] for i,r in enumerate(samples)])


