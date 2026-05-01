"""Concrete witnesses for the bidict ETNA workload.

Each ``witness_<snake>_case_<tag>`` is a no-arg function that calls
``property_<snake>`` with frozen inputs. On the base tree every witness
returns PASS; with the corresponding patch reverse-applied, the witness
returns fail(...).
"""
from ._result import PropertyResult
from . import properties


def witness_bidict_none_rejected_case_basic() -> PropertyResult:
    return properties.property_bidict_none_rejected(0)


def witness_ior_preserves_identity_case_basic() -> PropertyResult:
    # Aliasing-sensitive: |= must mutate in place so `aliased` reflects the new items.
    return properties.property_ior_preserves_identity(([(1, 10), (2, 20)], [(3, 30)]))


def witness_or_does_not_mutate_self_case_basic() -> PropertyResult:
    return properties.property_or_does_not_mutate_self(([(1, 10), (2, 20)], [(3, 30)]))


def witness_popitem_keeps_inverse_consistent_case_basic() -> PropertyResult:
    return properties.property_popitem_keeps_inverse_consistent([(1, 10), (2, 20)])


def witness_forceput_overwrites_not_raises_case_dup_key() -> PropertyResult:
    # Duplicate KEY: forceput should silently drop the old (1 -> 10) mapping.
    return properties.property_forceput_overwrites_not_raises(([(1, 10), (2, 20)], 1, 99))


def witness_forceput_overwrites_not_raises_case_dup_val() -> PropertyResult:
    # Duplicate VALUE: forceput should silently drop the old (1 -> 10) mapping.
    return properties.property_forceput_overwrites_not_raises(([(1, 10), (2, 20)], 99, 10))


def witness_ordered_popitem_last_false_returns_first_case_basic() -> PropertyResult:
    return properties.property_ordered_popitem_last_false_returns_first(
        [(1, 10), (2, 20), (3, 30)]
    )
