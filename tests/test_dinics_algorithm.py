import pytest
from src.dinics_algorithm import dinics_max_flow

def test_simple_flow():
    # Simple graph with one path
    graph = {
        's': {'a': 10},
        'a': {'t': 10},
        't': {}
    }
    assert dinics_max_flow(graph, 's', 't') == 10

def test_multiple_paths():
    # Graph with multiple paths
    graph = {
        's': {'a': 10, 'b': 10},
        'a': {'b': 2, 't': 4},
        'b': {'t': 8},
        't': {}
    }
    assert dinics_max_flow(graph, 's', 't') == 18

def test_complex_flow():
    # More complex graph
    graph = {
        's': {'a': 3, 'b': 2},
        'a': {'b': 1, 'c': 3},
        'b': {'c': 1, 't': 2},
        'c': {'t': 2},
        't': {}
    }
    assert dinics_max_flow(graph, 's', 't') == 5

def test_no_flow():
    # Graph with no path
    graph = {
        's': {},
        't': {}
    }
    assert dinics_max_flow(graph, 's', 't') == 0

def test_invalid_source_sink():
    # Test with non-existent source or sink
    graph = {
        's': {'a': 10},
        'a': {'t': 10}
    }
    with pytest.raises(ValueError):
        dinics_max_flow(graph, 'x', 't')
    
    with pytest.raises(ValueError):
        dinics_max_flow(graph, 's', 'x')

def test_self_loops():
    # Graph with potential self-loops
    graph = {
        's': {'a': 10, 's': 5},  # self-loop
        'a': {'t': 10, 'a': 2},  # self-loop
        't': {}
    }
    assert dinics_max_flow(graph, 's', 't') == 10