# bidict — ETNA Tasks

Total tasks: 24

## Task Index

| Task | Variant | Framework | Property | Witness |
|------|---------|-----------|----------|---------|
| 001 | `bidict_none_silently_empty_678c007_1` | proptest | `BidictNoneRejected` | `witness_bidict_none_rejected_case_basic` |
| 002 | `bidict_none_silently_empty_678c007_1` | quickcheck | `BidictNoneRejected` | `witness_bidict_none_rejected_case_basic` |
| 003 | `bidict_none_silently_empty_678c007_1` | crabcheck | `BidictNoneRejected` | `witness_bidict_none_rejected_case_basic` |
| 004 | `bidict_none_silently_empty_678c007_1` | hegel | `BidictNoneRejected` | `witness_bidict_none_rejected_case_basic` |
| 005 | `forceput_raises_on_dup_b1d1c71_1` | proptest | `ForceputOverwritesNotRaises` | `witness_forceput_overwrites_not_raises_case_dup_key` |
| 006 | `forceput_raises_on_dup_b1d1c71_1` | quickcheck | `ForceputOverwritesNotRaises` | `witness_forceput_overwrites_not_raises_case_dup_key` |
| 007 | `forceput_raises_on_dup_b1d1c71_1` | crabcheck | `ForceputOverwritesNotRaises` | `witness_forceput_overwrites_not_raises_case_dup_key` |
| 008 | `forceput_raises_on_dup_b1d1c71_1` | hegel | `ForceputOverwritesNotRaises` | `witness_forceput_overwrites_not_raises_case_dup_key` |
| 009 | `ior_returns_new_bidict_6faf1ef_1` | proptest | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| 010 | `ior_returns_new_bidict_6faf1ef_1` | quickcheck | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| 011 | `ior_returns_new_bidict_6faf1ef_1` | crabcheck | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| 012 | `ior_returns_new_bidict_6faf1ef_1` | hegel | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| 013 | `or_mutates_self_2074f4b_1` | proptest | `OrDoesNotMutateSelf` | `witness_or_does_not_mutate_self_case_basic` |
| 014 | `or_mutates_self_2074f4b_1` | quickcheck | `OrDoesNotMutateSelf` | `witness_or_does_not_mutate_self_case_basic` |
| 015 | `or_mutates_self_2074f4b_1` | crabcheck | `OrDoesNotMutateSelf` | `witness_or_does_not_mutate_self_case_basic` |
| 016 | `or_mutates_self_2074f4b_1` | hegel | `OrDoesNotMutateSelf` | `witness_or_does_not_mutate_self_case_basic` |
| 017 | `ordered_popitem_last_swapped_b1d1c72_1` | proptest | `OrderedPopitemLastFalseReturnsFirst` | `witness_ordered_popitem_last_false_returns_first_case_basic` |
| 018 | `ordered_popitem_last_swapped_b1d1c72_1` | quickcheck | `OrderedPopitemLastFalseReturnsFirst` | `witness_ordered_popitem_last_false_returns_first_case_basic` |
| 019 | `ordered_popitem_last_swapped_b1d1c72_1` | crabcheck | `OrderedPopitemLastFalseReturnsFirst` | `witness_ordered_popitem_last_false_returns_first_case_basic` |
| 020 | `ordered_popitem_last_swapped_b1d1c72_1` | hegel | `OrderedPopitemLastFalseReturnsFirst` | `witness_ordered_popitem_last_false_returns_first_case_basic` |
| 021 | `popitem_orphans_inverse_b1d1c70_1` | proptest | `PopitemKeepsInverseConsistent` | `witness_popitem_keeps_inverse_consistent_case_basic` |
| 022 | `popitem_orphans_inverse_b1d1c70_1` | quickcheck | `PopitemKeepsInverseConsistent` | `witness_popitem_keeps_inverse_consistent_case_basic` |
| 023 | `popitem_orphans_inverse_b1d1c70_1` | crabcheck | `PopitemKeepsInverseConsistent` | `witness_popitem_keeps_inverse_consistent_case_basic` |
| 024 | `popitem_orphans_inverse_b1d1c70_1` | hegel | `PopitemKeepsInverseConsistent` | `witness_popitem_keeps_inverse_consistent_case_basic` |

## Witness Catalog

- `witness_bidict_none_rejected_case_basic` — bidict(None) must raise TypeError
- `witness_forceput_overwrites_not_raises_case_dup_key` — duplicate-key forceput must drop the old mapping
- `witness_forceput_overwrites_not_raises_case_dup_val` — duplicate-value forceput must drop the old mapping
- `witness_ior_preserves_identity_case_basic` — alias-after-|= must reflect the new items
- `witness_or_does_not_mutate_self_case_basic` — a | b must leave a unchanged
- `witness_ordered_popitem_last_false_returns_first_case_basic` — popitem(last=False) must return first; popitem(last=True) must return last
- `witness_popitem_keeps_inverse_consistent_case_basic` — popped value must vanish from inverse
