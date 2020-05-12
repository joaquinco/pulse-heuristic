### Parameters ###

/* Graph  */
set nodes;
set edges;

/* Topology */
set inbound{nodes} within edges;
set outbound{nodes} within edges;

/* Set of infrastructures */
set infras;

/* Arcs weight */
param weight{edges, infras} >= 0;

/* Demand */
set ods within nodes cross nodes;
param demand{ods} > 0;

/* Construction cost per arc */
param construction_cost{edges, infras};

param budget >= 0;

### Variables ###

/* Binary variable decides which layer is active on each edge */
var y{edges, infras} binary;

/* Variable which models where the flow from origin to destination goes through */
var x{edges, ods, infras} >= 0;

### Objective ###

minimize flows_cost:
  sum{(o, d) in ods, i in infras}
    sum{e in edges} (
      x[e, o, d, i] * weight[e, i]
    );

### Constraints ###

subject to at_most_one_infra_active {e in edges}: sum{i in infras} y[e, i] <= 1;

subject to satisfy_demand {n in nodes, (o, d) in ods}:
  sum{e in outbound[n], i in infras} x[e, o, d, i] - sum{e in inbound[n], i in infras} x[e, o, d, i] =
    if n = o then demand[o, d]
    else if n = d then -demand[o, d]
    else 0;

subject to respect_budget: sum{e in edges, i in infras} y[e, i] * construction_cost[e, i] <= budget;

subject to respect_active_infra {e in edges, i in infras, (o, d) in ods}: 
x[e, o, d, i] <= demand[o, d] * y[e, i];

end;
