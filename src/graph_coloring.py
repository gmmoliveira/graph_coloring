"""
	Author: (MSc) Guilherme Mendes Marques de Oliveira
	Contact: gmmoliveira@gmail.com / guilherme_1994@yahoo.com.br
	Creation Date: May 11, 2020
	Last updated: April 13, 2021
	---------------------------------------------------------------
	The purpose of this work is to have fun while practicing skills
	relevant to my fields of interest: computer science and mathematics
	(specially machine learning, combinatorial optimization
	and related topics)
	---------------------------------------------------------------
"""
"""
	Copyright 2021 Guilherme Mendes Marques de Oliveira
	SPDX-License-Identifier: Apache-2.0
"""
"""
	========================================================================================
	Below, I mention the credits for the original code snippets and/or libraries used in this
	work. Please, notice that NONE of the below mentioned institution(s)/company(ies)/
	developer(s)/etc endorse my work. I simply mentioned them to givem them credit for their
	original work (from which this work was, somehow, derived from) and also to THANK them!
	Please, refer to the "NOTICE.txt" file at the root directory for more information.
	========================================================================================

	This file is built using Google ORTools, all credits goes to Google LLC for the development
	of such library.
	----------------------------------------------------------------------------------------
	This file is built using the NumPy library (https://numpy.org/index.html)
	----------------------------------------------------------------------------------------
"""


from linear_programming_solver import solve_lp
import numpy as np


class GraphColoringMIP:
	def __init__(self, graph):
		'''
		input:
		-----
			* graph: an adjacency matrix representing the graph as a
				2D numpy array (note that the MIP algorithm has 
				non-polynomial nature, therefore, using adjacency list
				of lists doesn't accomplish meaningful results). Note
				that ONLY the upper diagonal of this matrix will be
				considered for the representation of the graph;
		'''
		self.graph = graph
		self.n = graph.shape[0]

		self.num_edges = 0
		for u in range(0, self.n - 1):
			for v in range(u + 1, self.n):
				if self.graph.item(u, v) != 0:
					self.num_edges += 1

		self.heuristic_min_chrom = self.n

		self.X_indexing = lambda v, k: (v * self.heuristic_min_chrom) + k
		self.W_indexing = lambda k: (self.n * self.heuristic_min_chrom) + k

	def _lpsolution2coloring(self):
		self.solution = np.zeros(shape=self.n, dtype=int)

		for v in range(0, self.n):
			for k in range(0, self.heuristic_min_chrom):
				if self.lp_solution.item(self.X_indexing(v, k)) != 0:
					self.solution.itemset(v, k)

		min_assignment = {}
		next_assignment = 0
		for v in range(0, self.n):
			color = self.solution.item(v)

			if color not in min_assignment:
				min_assignment[color] = next_assignment
				next_assignment += 1

			self.solution.itemset(v, min_assignment[color])

		self.min_chromatic_num = len(min_assignment.keys())

	def _update_heuristic_min_chrom(self):
		assigned_colors = [-1] * self.n
			
		for u in range(self.n):
			available_colors = [c for c in range(self.n)]
			for v in range(self.n):
				if (u != v) and (self.graph.item(u, v) == 1) and (assigned_colors[v] != -1) and (assigned_colors[v] in available_colors):
					available_colors.remove(assigned_colors[v])
			assigned_colors[u] = min(available_colors)

		self.heuristic_min_chrom = (max(assigned_colors) + 1)
		self.heuristic_certificate = assigned_colors

		return self.heuristic_min_chrom

	def model(self, ascopy=True, dtype=np.float64):
		self._update_heuristic_min_chrom()
		num_constraints = self.n  + self.n * self.heuristic_min_chrom + self.num_edges * self.heuristic_min_chrom
		num_vars = (self.n + 1) * self.heuristic_min_chrom

		self.A = np.zeros(shape=(num_constraints, num_vars), dtype=dtype)
		self.lb = np.zeros(shape=num_constraints, dtype=dtype)
		self.ub = np.ones(shape=num_constraints, dtype=dtype)
		self.C = np.zeros(shape=num_vars, dtype=dtype)

		constraint = 0

		# single color assigned per vertex
		for v in range(0, self.n):
			for k in range(0, self.heuristic_min_chrom):
				self.A.itemset(constraint, self.X_indexing(v, k), 1)
			self.lb.itemset(constraint, 1)
			self.ub.itemset(constraint, 1)
			constraint += 1

		# single color per neighbours
		for u in range(0, self.n - 1):
			for v in range(u + 1, self.n):
				if self.graph.item(u, v) != 0:
					for k in range(0, self.heuristic_min_chrom):
						self.A.itemset(constraint, self.X_indexing(u, k), 1)
						self.A.itemset(constraint, self.X_indexing(v, k), 1)
						self.lb.itemset(constraint, 0)
						self.ub.itemset(constraint, 1)

						constraint += 1

		# Wk constraints
		for v in range(0, self.n):

			for k in range(0, self.heuristic_min_chrom):
				self.A.itemset(constraint, self.X_indexing(v, k), -1)
				self.A.itemset(constraint, self.W_indexing(k), 1)
				self.lb.itemset(constraint, 0)
				self.ub.itemset(constraint, 1)

				constraint += 1
		
		for k in range(0, self.heuristic_min_chrom):
			self.C.itemset(self.W_indexing(k), 1)

		if ascopy:
			return self.A.copy(), self.lb.copy(), self.ub.copy(), self.C.copy()
		else:
			return self.A, self.lb, self.ub, self.C

	def solve(self):
		hint = [0] * ((self.n + 1) * self.heuristic_min_chrom)
		for v in range(self.n):
			k = self.heuristic_certificate[v]
			hint[self.X_indexing(v, k)] = 1
			hint[self.W_indexing(k)] = 1
		hint = []
		self.obj_value, self.lp_solution, self.status, time_spent = solve_lp(C=self.C, A=self.A, lb=self.lb, ub=self.ub, maximization=False, method='BOP', hint=hint, num_threads=8)

		self._lpsolution2coloring()

		print('MIP optimization time (milliseconds):', time_spent)

		return self.min_chromatic_num, self.solution


if __name__ == '__main__':
	n = 20
	g = np.zeros(shape=(n, n), dtype=int)
	num_edges = 0
	for u in range(0, n - 1):
		for v in range(u + 1, n):
			if np.random.uniform(low=0, high=1+1e-12) <= 0.4:
				g.itemset(u, v, 1)
				g.itemset(v, u, 1)
				num_edges += 1
	print('The input graph is:')
	print(g)
	print('It contains {:d} vertices and {:d} edges.'.format(n, num_edges))
	
	coloring = GraphColoringMIP(graph=g)
	coloring.model()
	print('HEURISTIC MIN CHROM =', coloring._update_heuristic_min_chrom())
	min_chrom, colors = coloring.solve()


	print('The minimum chromatic number for the given input is:', min_chrom)
	print('The color to assign to vertex k matches the k-th one in the following array:\n', colors)

	for u in range(0, n - 1):
		for v in range(u + 1, n):
			if g.item(u, v) == 1 and (colors.item(u) == colors.item(v)):
				#print('BAD answer! Counter example: '+str(u)+' and '+str(v))
				print('BAD answer! Counter example: {} and {}'.format(str(u), str(v)))
