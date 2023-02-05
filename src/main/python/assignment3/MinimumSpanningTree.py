import numpy

###
# Required input:
#   num_vertices: Number of vertices in the input graph
#   graph: This is an adjacency matrix to depict the graph. Each cell represents edge and its traversal weight
#           Note: Weights in adjacency matrix should be positive.
###

###
# Output:
#   mst: minimum spanning tree as adjacency matrix
#   traversl_cost: cost of traversing all the vertices
###

###
# There are many ways to solve for minimum spanning tree
# 1. Prim's Algorith
# 2. Kruskal's Algorithm
# 3. Fibonacci Heaps
###


class UndirectedWeightedGraph:
    def __init__(self, num_vertices):
        self.vertex_count = num_vertices
        self.graph = numpy.zeros((num_vertices, num_vertices), dtype=int)

    ###
    # For this assignment I choose to implement using Prim's Algorithm
    # Prim's algorithm logic:
    #   1. Choose any vertex as source
    #   2. Find the minimum weight edge for traversal to next vertex such that there are no cycles and add it to tree.
    #   3. Keep repeating this process until we traverse all the vertices in the graph.
    ###
    def prims_algorithm(self):
        inf = float('inf')
        # For storing traversed vertices
        vertices_traversed = numpy.full(self.vertex_count, False, dtype=bool)

        # Result mst & cost
        mst = numpy.zeros((self.vertex_count, self.vertex_count), dtype=int)
        traversal_cost = 0

        while False in vertices_traversed:
            min_cost = inf
            start_vertex = 0
            end_vertex = 0

            for row in range(self.vertex_count):
                # If vertex is traversed, look its connections
                if vertices_traversed[row]:
                    # Find the min_cost to traverse to next non-traversed vertex
                    for col in range(self.vertex_count):
                        if not vertices_traversed[col] and self.graph[row][col] > 0:
                            if self.graph[row][col] < min_cost:
                                min_cost = self.graph[row][col]
                                start_vertex, end_vertex = row, col

            # Add vertex to traversed vertices
            vertices_traversed[end_vertex] = True

            # update cost in mst
            if min_cost == inf:
                mst[start_vertex][end_vertex] = 0
            else:
                mst[start_vertex][end_vertex] = min_cost
                traversal_cost = traversal_cost + min_cost

            mst[end_vertex][start_vertex] = mst[start_vertex][end_vertex]
        return mst, traversal_cost


if __name__ == "__main__":
    g1 = UndirectedWeightedGraph(5)
    g1.graph = [[0, 2, 0, 6, 0],
                [2, 0, 3, 8, 5],
                [0, 3, 0, 0, 7],
                [6, 8, 0, 0, 9],
                [0, 5, 7, 9, 0]]
    print(g1.prims_algorithm())

    g2 = UndirectedWeightedGraph(4)
    g2.graph = [[0, 2, 0, 6],
                [2, 0, 3, 8],
                [0, 3, 0, 0],
                [6, 8, 0, 0]]
    print(g2.prims_algorithm())

    g3 = UndirectedWeightedGraph(2)
    g3.graph = [[0, 2],
                [2, 0]]
    print(g3.prims_algorithm())

    g4 = UndirectedWeightedGraph(1)
    g4.graph = [[5]]
    print(g4.prims_algorithm())

