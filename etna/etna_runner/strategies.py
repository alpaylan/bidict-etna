"""Hypothesis strategies for the bidict ETNA workload.

CrossHair-compatible: only ``st.integers``, ``st.lists``, ``st.tuples``,
``st.booleans``. No custom ``@composite`` strategies, no ``st.data``.
"""
from hypothesis import strategies as st


_INT = st.integers(min_value=-50, max_value=50)
_PAIR = st.tuples(_INT, _INT)
_PAIR_LIST = st.lists(_PAIR, max_size=6)


def strategy_bidict_none_rejected():
    return _INT


def strategy_ior_preserves_identity():
    return st.tuples(_PAIR_LIST, _PAIR_LIST)


def strategy_or_does_not_mutate_self():
    return st.tuples(_PAIR_LIST, _PAIR_LIST)


def strategy_popitem_keeps_inverse_consistent():
    return _PAIR_LIST


def strategy_forceput_overwrites_not_raises():
    return st.tuples(_PAIR_LIST, _INT, _INT)


def strategy_ordered_popitem_last_false_returns_first():
    return _PAIR_LIST
