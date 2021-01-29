# QAOA for MaxCut

## The MaxCut problem

The aim of MaxCut is to maximize the number of edges in a graph that are “cut” by a given partition of the vertices into two sets (see figure below).

![maximum cut example](./images/qaoa_maxcut_partition.png)

Consider a graph with <b>m</b> edges and ***n*** vertices. We seek the partition ***z*** of the vertices into two sets A and B which maximizes

![equation1](https://latex.codecogs.com/gif.latex?C(z)%20=%20\sum_{\alpha%20=1}^{m}C_{\alpha}(z))

where ***C*** counts the number of edges cut. <b><i>C</i></b><sub>&alpha;</sub>(***z***)=1 if ***z*** places one vertex from the
&alpha;<sup>th</sup> edge in set A and the other in set B, and ***C***<sub>&alpha;</sub>(***z***)=0 otherwise.
Finding a cut which yields the maximum possible value of ***_C_*** is an NP-complete problem, so our best hope for a
polynomial-time algorithm lies in an approximate optimization.
In the case of MaxCut, this means finding a partition ***z*** which
yields a value for ***C***(***z***) that is close to the maximum possible value.

We can represent the assignment of vertices to set A or B using a bitstring,
***z***=z<sub>1</sub>...z<sub>n</sub> where z<sub>i</sub>=0 if the i<sup>th</sup> vertex is in A and
z<sub>i</sub> = 1 if it is in B. For instance,
in the situation depicted in the figure above the bitstring representation is ***z***=0101,
indicating that the 0<sup>th</sup> and 2<sup>nd</sup> vertices are in A
while the 1<sup>st</sup> and 3<sup>rd</sup> are in
B. This assignment yields a value for the objective function
***C***=4, which turns out to be the maximum cut.

## QAOA for MaxCut

The Quantum Approximate Optimization Algorithm (QAOA) is a quantum algorithm which uses unitary evoltion of an intial state to find approximate solutions to a Constraints satisfaction problem (CSP).<br>
Firstly, denoting the partitions using computational basis states |***z***>, we can represent the terms in the
objective function as operators acting on these states

![equation2](https://latex.codecogs.com/gif.latex?C_\alpha%20=%20\frac{1}{2}\left(1-\sigma_{z}^j\sigma_{z}^k\right))

where the &alpha;<sup>th</sup> edge is between vertices (j,k).
***C***<sub>&alpha;</sub> has eigenvalue 1 if and only if the j<sup>th</sup> and k<sup>th</sup>
qubits have different z-axis measurement values, representing separate partitions.
The objective function ***C*** can be considered a diagonal operator with integer eigenvalues.

QAOA starts with a uniform superposition over the ***n*** bitstring basis states,

![equation3](https://latex.codecogs.com/gif.latex?|+_{n}\rangle%20=%20\frac{1}{\sqrt{2^n}}\sum_{z\in%20\{0,1\}^n}%20|z\rangle)

We aim to explore the space of bitstring states for a superposition which is likely to yield a
large value for the ***C*** operator upon performing a measurement in the computational basis.
Using the _2p_ angle parameters
![eq_par](https://latex.codecogs.com/svg.latex?\vec{\gamma}%20=%20\gamma_1\gamma_2...\gamma_p,%20\vec{\beta}%20=%20\beta_1\beta_2...\beta_p)
we perform a sequence of operations on our initial state:

![equation3](https://latex.codecogs.com/gif.latex?|\boldsymbol{\gamma},\boldsymbol{\beta}\rangle%20=%20U_{B_p}U_{C_p}U_{B_{p-1}}U_{C_{p-1}}...U_{B_1}U_{C_1}|+_n\rangle)

where the operators have the explicit forms

![equation4](https://latex.codecogs.com/gif.latex?U_{B_l}%20=%20e^{-i\beta_lB}%20=%20\prod_{j=1}^n%20e^{-i\beta_l\sigma_x^j},%20\\%20U_{C_l}%20=%20e^{-i\gamma_lC}%20=%20\prod_{\text{edge%20(j,k)}}%20e^{-i\gamma_l(1-\sigma_z^j\sigma_z^k)/2})

In other words, we make _p_ layers of parametrized ***U<sub>B</sub>U<sub>C</sub>*** gates.
These can be implemented on a quantum circuit using the gates depicted below, up to an irrelevant constant
that gets absorbed into the parameters.

Let ![equation5](https://latex.codecogs.com/svg.latex?F_p%20=%20\langle%20\vec{\gamma},\vec{\beta}%20|%20C%20|%20\vec{\gamma},\vec{\beta}%20\rangle) be the expectation of the objective operator.
In the next section, we will use PennyLane to perform classical optimization
over the circuit parameters ![eq6](https://latex.codecogs.com/svg.latex?(\vec{\gamma},\vec{\beta})).
This will specify a state ![eq7](https://latex.codecogs.com/svg.latex?|\vec{\gamma},\vec{\beta})\rangle) which is
likely to yield an approximately optimal partition $|z\rangle$ upon performing a measurement in the
computational basis.
In the case of the graph shown above, we want to measure either 0101 or 1010 from our state since these correspond to
the optimal partitions.

![QAOA optimal state](./images/qaoa_optimal_state.png)

Qualitatively, QAOA tries to evolve the initial state into the plane of the
|0101>, |1010> basis states (see figure above).

