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
