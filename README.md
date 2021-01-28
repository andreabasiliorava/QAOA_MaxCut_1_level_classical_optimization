# QAOA for MaxCut

## The MaxCut problem 

The aim of MaxCut is to maximize the number of edges in a graph that are “cut” by a given partition of the vertices into two sets (see figure below).

![maximum cut example](./images/qaoa_maxcut_partition.png)

Consider a graph with $m$ edges and $n$ vertices. We seek the partition $z$ of the vertices into two sets A and B which maximizes

<img src="http://www.sciweavers.org/tex2img.php?eq=%24%24C%28z%29%20%3D%20%5Csum_%7B%5Calpha%20%3D1%7D%5E%7Bm%7DC_%7B%5Calpha%7D%28z%29%24%24&bc=White&fc=Black&im=jpg&fs=12&ff=modern&edit=0" align="center" border="0" alt="$$C(z) = \sum_{\alpha =1}^{m}C_{\alpha}(z)$$" width="143" height="21" />

where $C$ counts the number of edges cut. $C_\alpha(z)=1$ if $z$ places one vertex from the
$\alpha^\text{th}$ edge in set $A$ and the other in set $B$, and $C_\alpha(z)=0$ otherwise.
Finding a cut which yields the maximum possible value of $C$ is an NP-complete problem, so our best hope for a
polynomial-time algorithm lies in an approximate optimization.
In the case of MaxCut, this means finding a partition $z$ which
yields a value for $C(z)$ that is close to the maximum possible value.

We can represent the assignment of vertices to set $A$ or $B$ using a bitstring,
$z=z_1...z_n$ where $z_i=0$ if the $i^\text{th}$ vertex is in $A$ and
$z_i = 1$ if it is in $B$. For instance,
in the situation depicted in the figure above the bitstring representation is $z=0101\text{,}$
indicating that the $0^{\text{th}}$ and $2^{\text{nd}}$ vertices are in $A$
while the $1^{\text{st}}$ and $3^{\text{rd}}$ are in
$B$. This assignment yields a value for the objective function
$C=4$, which turns out to be the maximum cut.

## QAOA for MaxCut

The Quantum Approximate Optimization Algorithm (QAOA) is a quantum algorithm which uses unitary evoltion of an intial state to find approximate solutions to a Constraints satisfaction problem (CSP).<br>
Firstly, denoting the partitions using computational basis states $|z\rangle$, we can represent the terms in the
objective function as operators acting on these states

<img src="https://bit.ly/2MByHhj" align="center" border="0" alt="\begin{align}C_\alpha = \frac{1}{2}\left(1-\sigma_{z}^j\sigma_{z}^k\right),\end{align}" width="143" height="36" />
where the $\alpha\text{th}$ edge is between vertices $(j,k)$.
$C_\alpha$ has eigenvalue 1 if and only if the $j\text{th}$ and $k\text{th}$
qubits have different z-axis measurement values, representing separate partitions.
The objective function $C$ can be considered a diagonal operator with integer eigenvalues.

QAOA starts with a uniform superposition over the $n$ bitstring basis states,

\begin{align}|+_{n}\rangle = \frac{1}{\sqrt{2^n}}\sum_{z\in \{0,1\}^n} |z\rangle.\end{align}


We aim to explore the space of bitstring states for a superposition which is likely to yield a
large value for the $C$ operator upon performing a measurement in the computational basis.
Using the $2p$ angle parameters
$\boldsymbol{\gamma} = \gamma_1\gamma_2...\gamma_p$, $\boldsymbol{\beta} = \beta_1\beta_2...\beta_p$
we perform a sequence of operations on our initial state:

\begin{align}|\boldsymbol{\gamma},\boldsymbol{\beta}\rangle = U_{B_p}U_{C_p}U_{B_{p-1}}U_{C_{p-1}}...U_{B_1}U_{C_1}|+_n\rangle\end{align}

where the operators have the explicit forms

\begin{align}U_{B_l} &= e^{-i\beta_lB} = \prod_{j=1}^n e^{-i\beta_l\sigma_x^j}, \\
  U_{C_l} &= e^{-i\gamma_lC} = \prod_{\text{edge (j,k)}} e^{-i\gamma_l(1-\sigma_z^j\sigma_z^k)/2}.\end{align}

In other words, we make $p$ layers of parametrized $U_bU_C$ gates.
These can be implemented on a quantum circuit using the gates depicted below, up to an irrelevant constant
that gets absorbed into the parameters.

Let $F_p = \langle \boldsymbol{\gamma},
\boldsymbol{\beta} | C | \boldsymbol{\gamma},\boldsymbol{\beta} \rangle$ be the expectation of the objective operator.
In the next section, we will use PennyLane to perform classical optimization
over the circuit parameters $(\boldsymbol{\gamma}, \boldsymbol{\beta})$.
This will specify a state $|\boldsymbol{\gamma},\boldsymbol{\beta}\rangle$ which is
likely to yield an approximately optimal partition $|z\rangle$ upon performing a measurement in the
computational basis.
In the case of the graph shown above, we want to measure either 0101 or 1010 from our state since these correspond to
the optimal partitions.

![QAOA optimal state](./images/qaoa_optimal_state.png)

Qualitatively, QAOA tries to evolve the initial state into the plane of the
$|0101\rangle$, $|1010\rangle$ basis states (see figure above).

