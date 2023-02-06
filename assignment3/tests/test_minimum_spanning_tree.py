import numpy as np
import pytest
from assignment3 import MinimumSpanningTree


class TestMinimumSpanningTree:

    def test_prims_algorithm_fail1(self):
        # fail scenario: num_vertices = 0
        with pytest.raises(ValueError):
            mst_obj = MinimumSpanningTree.UndirectedWeightedGraph(0)

    def test_prims_algorithm_fail2(self):
        # fail scenario: input graph is None
        with pytest.raises(ValueError):
            input_graph = None
            mst_obj = MinimumSpanningTree.UndirectedWeightedGraph(5)
            mst_obj.graph = input_graph
            graph, cost = mst_obj.prims_algorithm()

    def test_prims_algorithm_fail3(self):
        # fail scenario: test for graph with all weights = zero
        with pytest.raises(ValueError):
            input_graph = [[0, 0],
                           [0, 0]]
            mst_obj = MinimumSpanningTree.UndirectedWeightedGraph(2)
            mst_obj.graph = input_graph
            mst, cost = mst_obj.prims_algorithm()

    def test_prims_algorithm_fail4(self):
        # success scenario: test for cost with -ve weights
        with pytest.raises(ValueError):
            input_graph = [[0, 2, 0, -6, 0],
                           [2, 0, 3, 8, 5],
                           [0, 3, 0, 0, 7],
                           [6, 8, 0, 0, 9],
                           [0, 5, 7, 9, 0]]
            mst_obj = MinimumSpanningTree.UndirectedWeightedGraph(5)
            mst_obj.graph = input_graph
            mst, cost = mst_obj.prims_algorithm()

    def test_prims_algorithm_success1(self):
        # success scenario: test for cost
        input_graph = [[0, 2, 0, 6, 0],
                       [2, 0, 3, 8, 5],
                       [0, 3, 0, 0, 7],
                       [6, 8, 0, 0, 9],
                       [0, 5, 7, 9, 0]]
        mst_obj = MinimumSpanningTree.UndirectedWeightedGraph(5)
        mst_obj.graph = input_graph
        mst, cost = mst_obj.prims_algorithm()
        assert cost == 16

    def test_prims_algorithm_success2(self):
        # success scenario: test for graph
        input_graph = [[0, 2, 0, 6, 0],
                       [2, 0, 3, 8, 5],
                       [0, 3, 0, 0, 7],
                       [6, 8, 0, 0, 9],
                       [0, 5, 7, 9, 0]]
        expected_graph = [[0, 2, 0, 6, 0],
                          [2, 0, 3, 0, 5],
                          [0, 3, 0, 0, 0],
                          [6, 0, 0, 0, 0],
                          [0, 5, 0, 0, 0]]
        mst_obj = MinimumSpanningTree.UndirectedWeightedGraph(5)
        mst_obj.graph = input_graph
        mst, cost = mst_obj.prims_algorithm()
        compare_result = np.allclose(mst, expected_graph)
        assert compare_result

    def test_prims_algorithm_success3(self):
        # success scenario: test for graph with one vertex
        input_graph = [[5]]
        mst_obj = MinimumSpanningTree.UndirectedWeightedGraph(1)
        mst_obj.graph = input_graph
        mst, cost = mst_obj.prims_algorithm()
        assert cost == 0


if __name__ == '__main__':
    pytest.main()

