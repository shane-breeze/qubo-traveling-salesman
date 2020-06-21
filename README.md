# QUBO Traveling salesman

Following the problem set out in 7.2 of
https://www.frontiersin.orqug/articles/10.3389/fphy.2014.00005/full
using the open-source PyQUBO software.

## Traveling salesman

This problem involves minimizing the sum of edge weights $W_{uv}$ associated
with each edge $uv$ in a graph $G=(V,E)$ under the constraint that the sum over
edges is restricted to a set of $E$ which are connected by vertices and each
vertex is used exactly once in joining the edges.

Let $\nu$ represent the vertex and $i$ represent its order in a prospective
cycle, then $x_{\nu,i}$ represents a possible states of the system: one if the
vertex $\nu$ is the $i$-th order in the cycle and zero otherwise. The
Hamiltonian for such a problem has four terms:

1. Self-interaction for vertices with a higher energy state if they appear in
the cycle more than once, $H_{\mathrm{v-self}}$.
1. Self-interaction for edges with a higher energy state if the appear in the
cycle more than once, $H_{\mathrm{e-self}}$.
1. Interaction between vertex $u$ and $v$ if they appear in subsequent orders
$j$ and $j+1$ if such an edge does not exist within the graph $G$,
$H_{\mathrm{uv-graph}}$.
1. Interaction between vertex $u$ and $v$ weighted by their distance $W_{uv}$,
$H_{\mathrm{uv-dist}}$.

with

$H = H_{\mathrm{v-self}} + H_{\mathrm{e-self}} + H_{\mathrm{uv-graph}} + H_{\mathrm{uv-dist}}$,

$H_{\mathrm{v-self}} = A\sum_{\nu=1}^{n}\left(1-\sum_{j=1}^{N}x_{\nu,j}\right)^2$,

$H_{\mathrm{e-self}} = A\sum_{j=1}^{n}\left(1-\sum_{\nu=1}^{N}x_{\nu,j}\right)^2$,

$H_{\mathrm{uv-graph}} = A\sum_{(uv)\notin E \sum_{j=1}^{N} x_{u,j}x_{\nu,j+1}$

and

$H_{\mathrm{uv-dist}} = B\sum_{(uv)\notin E W_{uv} \sum_{j=1}^{N} x_{u,j}x_{\nu,j+1}$.

The parameter $B$ must be small enough that it is never favourable to violate
the other constraints: e.g. $0<B\max(W_{uv})<A$.

The very first node may be fixed to appear first in the cycle to reduce the
problem by one dimension, where $x_{1,i} = \delta_{1,i}$
