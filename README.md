# graph_coloring
Solving (undirected) graph coloring as a Mixed Integer Programming problem

<hr>

<h3>Documentation of the source-code</h3>

Implements a class
<code class="inline_code">GraphColoringMIP</code>,
with the following methods:

<ul>
	<li>
		<code class="inline_code">GraphColoringMIP.__init__(self, graph=None, n=None)</code>:
		<ul>
			<li><code class="inline_code">graph</code>:
				an adjacency matrix representing the graph as a
				2D numpy array of dimensions
				<code class="inline_code">|V|</code> by
				<code class="inline_code">|V|</code> where
				the value at row i and column j
				set to 0 indicates the absence of an edge
				and 1 indicates the presence of an edge,
				between the vertices indexed by i and j.
				Note that only the upper diagonal of this matrix will be
				considered for the representation of the graph, also,
				the MIP algorithm has
				non-polynomial nature, therefore, using adjacency list
				of lists doesn't accomplish meaningful results;
			</li>
		</ul>

	</li>

	<li>
		<code class="inline_code">GraphColoringMIP._lpsolution2coloring(self)</code>:
		decodes the linear programming optimal solution vector
		<code class="inline_code">X*</code>
		into a human friendly format consisting of an array
		of <code class="inline_code">|V|</code>
		elements each representing a vertex of
		<code class="inline_code">G</code>
		with a color (integer number) assigned to it;
	</li>

	<li>
		<code class="inline_code">GraphColoringMIP._update_heuristic_min_chrom(self)</code>:
		updates an internal representation of the minimum chromatic number and
		it's certificate using a heuristic
		(algorithm which doesn't offer any guarantees of finding the optimum solution)
		consisting of a greedy algorithm. Returns the chromatic number found by the heuristic;
	</li>

	<li>
		<code class="inline_code">GraphColoringMIP.model(self, ascopy=True, dtype=np.float64)</code>:
		instantiates internal arrays to be used for the linear programming and fill them up.
		The
		heuristic from the method
		<code class="inline_code">GraphColoringMIP._update_heuristic_min_chrom(self)</code>
		is used
		to find an upper limit on the amount of colors that may be used, this simple technique
		reduces a the number of required variables in the final MIP model, therefore,
		a solution may be found faster. Returns the LP data arrays;
		<ul>
			<li><code class="inline_code">ascopy</code>:
				return copies of the LP data structures which may be safely modified outside
				the scope of this object;
			</li>
			<li><code class="inline_code">dtype</code>:
				sets the data type for the LP data arrays;
			</li>
		</ul>
	</li>

	<li>
		<code class="inline_code">GraphColoringMIP.solve(self)</code>:
		solves the LP built by
		<code class="inline_code">GraphColoringMIP.model(self, ascopy=True, dtype=np.float64)</code>.
		Returns a 2-tuple containing the (guaranteed) minimum chromatic number and
		the optimum solution vector
		<code class="inline_code">X*</code> in a decoded (human-friendly) format;
	</li>
</ul>

<h3>Running an example</h3>

<pre><code class="lang-shell">The input graph is:
[[0 1 0 0 0 1 0 1 1 0 0 1 1 0 1 0 1 0 1 1]
 [1 0 0 1 1 0 0 1 1 1 0 0 0 0 0 1 1 0 0 0]
 [0 0 0 1 1 1 1 1 1 1 1 0 0 1 1 0 0 1 1 0]
 [0 1 1 0 0 0 0 0 0 0 0 0 0 1 1 0 0 1 0 1]
 [0 1 1 0 0 1 0 1 0 1 1 1 0 0 0 0 1 0 1 0]
 [1 0 1 0 1 0 0 0 0 0 1 0 0 1 1 0 1 1 1 1]
 [0 0 1 0 0 0 0 1 0 1 0 0 0 1 0 0 1 1 0 1]
 [1 1 1 0 1 0 1 0 1 0 0 0 0 1 0 0 1 1 0 1]
 [1 1 1 0 0 0 0 1 0 1 1 1 1 1 0 0 0 1 1 0]
 [0 1 1 0 1 0 1 0 1 0 0 0 1 1 0 1 0 1 0 0]
 [0 0 1 0 1 1 0 0 1 0 0 1 1 0 0 1 1 0 0 0]
 [1 0 0 0 1 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0]
 [1 0 0 0 0 0 0 0 1 1 1 0 0 0 1 0 0 0 1 1]
 [0 0 1 1 0 1 1 1 1 1 0 0 0 0 0 0 0 0 1 1]
 [1 0 1 1 0 1 0 0 0 0 0 0 1 0 0 1 0 0 0 0]
 [0 1 0 0 0 0 0 0 0 1 1 0 0 0 1 0 0 0 0 0]
 [1 1 0 0 1 1 1 1 0 0 1 0 0 0 0 0 0 0 0 0]
 [0 0 1 1 0 1 1 1 1 1 0 0 0 0 0 0 0 0 1 0]
 [1 0 1 0 1 1 0 0 1 0 0 0 1 1 0 0 0 1 0 1]
 [1 0 0 1 0 1 1 1 0 0 0 0 1 1 0 0 0 0 1 0]]
It contains 20 vertices and 81 edges.
<hr>
HEURISTIC MIN CHROM = 6
<hr>
MIP optimization time (milliseconds): 82
The minimum chromatic number for the given input is: 5

The color to assign to vertex k matches the k-th one in the following array:
 [0 1 0 2 3 1 1 2 4 2 2 1 1 3 4 0 4 3 2 4]
</code></pre>

Further reference on the problem formulation may be found here: https://gmmoliveira.github.io/blog/graph_coloring.html.
