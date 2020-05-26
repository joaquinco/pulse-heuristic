Multi-facility network flow problem using Pulse
===============================================

## Introduction

Implement basic heuristic to solve multi-facility network flow problem between several origin-destination (OD) paris. That is, find the best assignment of facilities to build, so that the routing cost (user cost of traversing the network) of all the OD pairs is decreased. Nota that, building no facilities still yields a feasible solution, since the base graph is assumed to satisfy demand. Facilities are built on top of existing arcs, and its effect is decreasing the user perceived cost.

There's a discrete, fix number of facilities that can be build on each arc. Facilities can be constructed on existing arcs only, and the sum of all construction cost will not overcome the specified budget.

There are two kind of variables in this problem, one is where to build the facilities, if any. The other variable models the route of each OD pair. The former being discrete variables, basically chose which facility to build, note that there will be always a default facility with cost zero which represents the existing graph. The latter are real valued.

## Heuristic

The heuristic implemented here uses pulse algorithm which is an efficient shortest-path algorithm that can handle constraints.

The basic algorithm is the following:

1. Assign to each OD pair a budget, that is the fraction of the total demand of that OD pair, multiplied by the total budget.
2. Randomize the OD pair list.
3. For each OD pair, run the pulse algorithm using the source, target and budget of that OD pair.
4. If a solution is found, apply the constructed facilities in the current graph (that means that some arcs will decrease its user cost), and continue to the next OD.
5. After all ODs have been processed, find the objective function cost, which is the sum of the shortest path cost of each OD pair, multiplied by the demand.

## Running the heuristic

Requirements:
- python 3.6 or higher.

In order to get the most out of it, the pypy python interpreter is recommended.

### Install dependencies

```
pip install -r requirements.txt
```

### Run heruistic

The heuristic input is a single json file where parameters and configuration is specified.

```
./bin/run inputfile.json
```

This will run the pulse heuristic printing the intermediate and final result to the standar output. If output is overwhelming, you can specify the `-l info` option to reduce the log level.

And an examplel of inputfile.json

```
{
  "graph": "data/mdeo_med.yml",
  "infrastructures": {
    "cost_factors": [0.9, 0.5, 0.4],
    "construction_cost_factors": [1, 4, 8]
  },
  "budget": 15000,
  "demand": [
    { "source": "15155", "target": "7884", "value": 500 },
    { "source": "7310", "target": "15195", "value": 50 },
    { "source": "15239", "target": "7626", "value": 100 },
    { "source": "8867", "target": "12671", "value": 350 }
  ],
  "config": {
    "arc_weight_key": "weight",
    "budget_assignment_approach": "demand",
    "max_iter": 4,
    "solutions_per_od": 2,
    "od_budget_epsilon": 500,
    "pulse_queue_key_factor": 2,
    "pulse_primal_bound_factor": 0.97,
    "pulse_discard_faraway_nodes": true,
    "pulse_discard_faraway_delta": 0
  }
}
```

To see more configuration or documentation about it, check `proj/config.py`.


### Export instance to MathProg data format

In order to run the exact model, you can export a run configuration for the pulse heuristic to MathProg format. In order to do so run:

```
./bin/run -a export inputfile.json > inputfile.dat
```

> This will export graph, demand, infrastrucutres and budget. The conifguration parameters are ignored.

And then run GLPK (recommended with Cutting-Plane option):

```
glpsol --cuts -m exact/model.mod -d inputfile.dat
```
