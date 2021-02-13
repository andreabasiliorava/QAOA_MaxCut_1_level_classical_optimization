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
![eq_par](https://latex.codecogs.com/svg.latex?\boldsymbol{\gamma}=(\gamma_1,\gamma_2,...,\gamma_p),%20\boldsymbol{\beta}=(\beta_1,%20\beta_2,...,%20\beta_p))
we perform a sequence of operations on our initial state:

![equation3](https://latex.codecogs.com/gif.latex?|\boldsymbol{\gamma},\boldsymbol{\beta}\rangle%20=%20U_{B_p}U_{C_p}U_{B_{p-1}}U_{C_{p-1}}...U_{B_1}U_{C_1}|+_n\rangle)

where the operators have the explicit forms

![equation4](https://latex.codecogs.com/gif.latex?U_{B_l}%20=%20e^{-i\beta_lB}%20=%20\prod_{j=1}^n%20e^{-i\beta_l\sigma_x^j},%20\\%20U_{C_l}%20=%20e^{-i\gamma_lC}%20=%20\prod_{\text{edge%20(j,k)}}%20e^{-i\gamma_l(1-\sigma_z^j\sigma_z^k)/2})

In other words, we make _p_ layers of parametrized ***U<sub>B</sub>U<sub>C</sub>*** gates.
These can be implemented on a quantum circuit using the gates depicted below, up to an irrelevant constant
that gets absorbed into the parameters.

Let **F<sub>p</sub>** = <**&gamma;**,**&beta;**|***C***|**&gamma;**,**&beta;**> be the expectation of the objective operator.
In the next section, we will use PennyLane to perform classical optimization
over the circuit parameters (**&gamma;**,**&beta;**).
This will specify a state |**&gamma;**,**&beta;**> which is
likely to yield an approximately optimal partition |z> upon performing a measurement in the
computational basis.
In the case of the graph shown above, we want to measure either 0101 or 1010 from our state since these correspond to
the optimal partitions.

![QAOA optimal state](./images/qaoa_optimal_state.png)

Qualitatively, QAOA tries to evolve the initial state into the plane of the
|0101>, |1010> basis states (see figure above).

## Parameters Optimization

The general steps in QAOA for parameters optimizations are:<br>
  * choose QAOA-level = p and pick p-pairs parameters (&gamma;<sub>1</sub>,...,&gamma;<sub>p</sub>,&beta;<sub>1</sub>,...,&beta;<sub>p</sub>)<sub>0</sub><br>
  * generate initial state |**s**> (usually is chosen to be easy to be prepeared) (which gives also $B$)<br>
  * evolve |**s**> in |**&gamma;**,**&beta;**> through 2p evolutions<br>
  * evaluate **F<sub>p</sub>** (or only certain terms of it) through N-times computational basis measurement on |**&gamma;**,**&beta;**>, obtained as the "classical" meanvalue of the N-outcomes
  * update the parameters through a chosen method, for example the stochastic gradient descent <br>    
* |**&gamma;**,**&beta;**> which optimize **F<sub>p</sub>** will be obtained after these iterations (and the solutions to the problem could be seen from outcome probabilities of strings obtained in the computational basis measurement for these angles)

However, for QAOA-level = 1, there's a theorem, which gives an analitical expression of the expectation of the cost function that has to be minimized, 
[here](https://arxiv.org/pdf/1706.02998.pdf) the paper with the theorem:

![eq_1](https://latex.codecogs.com/svg.latex?F_1(\gamma,\beta)%20%20=%20\frac{1}{2}%20+%20\frac{1}{4}%20(sin4\beta%20sin2\gamma)(cos^{d_u}\gamma%20+%20cos^{d_v}\gamma)%20-%20\frac{1}{4}(sin^2\beta%20cos^{d_u%20+%20d_v%20-%202\lambda_{uv}}\gamma))
![eq_3](https://latex.codecogs.com/svg.latex?(1-cos^{\lambda_{uv}}2\gamma))

so, for each edge <u,v>, we have to get:
* d<sub>u</sub>: degree of vertex u -1
* d<sub>v</sub>: degree of vertex v -1
* &lambda;<sub>uv</sub>: number common neighbours of vertices u and v

and in this special case the optimization steps are:

* get information of the graph
* parameter optimization:
    * evaluate analitical exspression of F<sub>1</sub>(&gamma;, &beta;) from graph informations
    * maximization of the function
* optimal (&gamma;, &beta;) will the ones that maximize F<sub>1</sub>
<hr>
## Structure of the project

Here follws the steps required to start the program and to plot the results:

1. First two packages has to be installed:
 * qutip
 * networkx <br>
that can be achieved by typying the command below in the working shell:
  
**python -m pip install -r requirements.txt**
 
2. Then, the user has to choose the graph for which this method find the maximum cuts. In the file configurations.txt three are already defined, any graph can be added using the syntax of [configuration](https://github.com/andreabasiliorava/QAOA_MaxCut_1_level_classical_optimization/blob/master/configuration.txt), giving the number of nodes, the edges and also the local paths to the folders where drawing of the graph and the probability distribution of the possible configurations must be saved. 

3. To obtain the final state, which contains the informations about the MaxCut solutions, and theyr probability distribution, the user has to launch the file 
[execution](https://github.com/andreabasiliorava/QAOA_MaxCut_1_level_classical_optimization/blob/master/execution.py), which imports its parameters from [configuration](https://github.com/andreabasiliorava/QAOA_MaxCut_1_level_classical_optimization/blob/master/configuration.txt) using ConfigParser library.<br>
The user has to specify the graph he wants to obtain solution of when launching the simulation file from the command line with the syntax:
 
**python execution.py configuration.txt *graph_name***

The obtained probability distributions are saved automatically in the ***prob_dist*** folder using their local paths.

4. To obtain the plots of the graph and it's respective histogram with the probability distributions of the final state with the maximum cuts be the more probable configurations, the user has to launch the [plots](https://github.com/andreabasiliorava/QAOA_MaxCut_1_level_classical_optimization/blob/master/plots.py) file with the graphs he wants.<br>
From command line the syntax is:
 
**python plots.py configuration.txt *graph_name***

The data are loaded from the configuration file through their local paths and then they are saved in the ***plots*** folder automatically.

Here follows how I've structured this project:

* All the quantum objects are initialized through the Qobj() class defined in the ***qutip*** library, here the [qutip documentation](http://qutip.org/docs/latest/index.html), in the documentation there are also the required packages for running qutip.<br>
The graphs are initialized through the Graph() class defined in the ***networkx*** library, here the [networkx documentation](https://networkx.org/documentation/stable//index.html).
The file [requirements](https://github.com/andreabasiliorava/QAOA_MaxCut_1_level_classical_optimization/blob/master/requirements.txt) must be executed for the installation of these two packages.

* In the file [qucompsys](https://github.com/andreabasiliorava/QAOA_MaxCut_1_level_classical_optimization/blob/master/qucompsys.py) I've defined functions needed to operate with composite systems of multiple qubits (obtained through the *tensor()* function of qutip), three that operates the Pauli matrices &sigma;<sub>y</sub>, &sigma;<sub>y</sub>, &sigma;<sub>z</sub> on the *i*-th qubit of a n-qubits tensor and one that apply the identity. There's also a function that, given a quantum state, it returns an array containing the probability distribution of the computational basis vectors of the space it belongs to. A function that generates n-random qubits, used for testing proper behaviour of other defined functions.

* In the file [graphs](https://github.com/andreabasiliorava/QAOA_MaxCut_1_level_classical_optimization/blob/master/graphs.py) I've defined two functions needed to get information about a graph, one which returns the degree of a node and one which returns the number of common neighbours of an edge. Thre's also another function which generates a random graph, used for testing proper behaviour of other defined functions.

* In the file [qaoa](https://github.com/andreabasiliorava/QAOA_MaxCut_1_level_classical_optimization/blob/master/qaoa.py) I've defined all the function needed for the QAOA steps to obtain the final state |**&gamma;**,**&beta;**>, a function which evaluates the classical cost function given a configuration and the graph information, a function that evaluates the analitical expression of **F<sub>1</sub>** for a given pair of &gamma; and &beta;. Also, it contains the functions needed to obtain the final state: one which initialize the intial state (it returns a quantum object obtained as the tensor product of the single qubit states |+>), two which define the mixing and problem Hamiltonians and another one which returns the evolution oprator U(**&gamma;**,**&beta;**), that has to be applyed to the intial state.

* In the file [testing](https://github.com/andreabasiliorava/QAOA_MaxCut_1_level_classical_optimization/blob/master/testing.py) I've tested all the qucompsys, graphs and qaoa functions to ensure that all of them work properly, using pytest testing, with the aid of hypothesis testing.

* In the file [configuration](https://github.com/andreabasiliorava/QAOA_MaxCut_1_level_classical_optimization/blob/master/configuration.txt) there are the definition of three graphs (butterfly, square and house graphs). Furthermore, there are the local paths in order to load the array data and to save them as images and graphs. It's a .txt file that is imported in execution file.

* In the file [execution](https://github.com/andreabasiliorava/QAOA_MaxCut_1_level_classical_optimization/blob/master/execution.py) there is the main part of the code, where the steps of the 1-level QAOA for MAxCut are performed using functions defined in the qaoa, qucompsys and graphs files. First is defined the graph, then the optimal parameters are obtain through a grid search method and, after have intialized the initial state, the final state is obtained by applying the evolution operator to the intial state with the optimal parameters obtained in the grid search step. The probability distribution of the configurations contained in the final state are saved in a file. Here I used the ConfigParser library in order to import the configuration file from command line, and passing its parameters to the program. 

* In the file [plots](https://github.com/andreabasiliorava/QAOA_MaxCut_1_level_classical_optimization/blob/master/plots.py) there are two functions that respectively plot the graph and the probability distributions of all the possible configurations of a cut applyed to the graph, loading the data of the graph from command line.

### Examples of results for the square graph used as the introductory example:

<img src="./images/square_graph.png" alt="drawing" width="400" class="center">

<img src="./images/square_prob_dist.png" alt="drawing" width="600" class="center">

and it can be seen that the most probable configuration is the one corresponding to the maximum cut of the graph.
