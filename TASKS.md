# bidict — ETNA Tasks

Total tasks: 12

## Task Index

| Task | Variant | Framework | Property | Witness |
|------|---------|-----------|----------|---------|
| 001 | `bidict_none_silently_empty_678c007_1` | hypothesis | `BidictNoneRejected` | `witness_bidict_none_rejected_case_basic` |
| 002 | `bidict_none_silently_empty_678c007_1` | crosshair | `BidictNoneRejected` | `witness_bidict_none_rejected_case_basic` |
| 003 | `forceput_raises_on_dup_b1d1c71_1` | hypothesis | `ForceputOverwritesNotRaises` | `witness_forceput_overwrites_not_raises_case_dup_key` |
| 004 | `forceput_raises_on_dup_b1d1c71_1` | crosshair | `ForceputOverwritesNotRaises` | `witness_forceput_overwrites_not_raises_case_dup_key` |
| 005 | `ior_returns_new_bidict_6faf1ef_1` | hypothesis | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| 006 | `ior_returns_new_bidict_6faf1ef_1` | crosshair | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| 007 | `or_mutates_self_2074f4b_1` | hypothesis | `OrDoesNotMutateSelf` | `witness_or_does_not_mutate_self_case_basic` |
| 008 | `or_mutates_self_2074f4b_1` | crosshair | `OrDoesNotMutateSelf` | `witness_or_does_not_mutate_self_case_basic` |
| 009 | `ordered_popitem_last_swapped_b1d1c72_1` | hypothesis | `OrderedPopitemLastFalseReturnsFirst` | `witness_ordered_popitem_last_false_returns_first_case_basic` |
| 010 | `ordered_popitem_last_swapped_b1d1c72_1` | crosshair | `OrderedPopitemLastFalseReturnsFirst` | `witness_ordered_popitem_last_false_returns_first_case_basic` |
| 011 | `popitem_orphans_inverse_b1d1c70_1` | hypothesis | `PopitemKeepsInverseConsistent` | `witness_popitem_keeps_inverse_consistent_case_basic` |
| 012 | `popitem_orphans_inverse_b1d1c70_1` | crosshair | `PopitemKeepsInverseConsistent` | `witness_popitem_keeps_inverse_consistent_case_basic` |

## Witness Catalog

- `witness_bidict_none_rejected_case_basic` — bidict(None) must raise TypeError
- `witness_forceput_overwrites_not_raises_case_dup_key` — duplicate-key forceput must drop the old mapping
- `witness_forceput_overwrites_not_raises_case_dup_val` — duplicate-value forceput must drop the old mapping
- `witness_ior_preserves_identity_case_basic` — alias-after-|= must reflect the new items
- `witness_or_does_not_mutate_self_case_basic` — a | b must leave a unchanged
- `witness_ordered_popitem_last_false_returns_first_case_basic` — popitem(last=False) must return first; popitem(last=True) must return last
- `witness_popitem_keeps_inverse_consistent_case_basic` — popped value must vanish from inverse
