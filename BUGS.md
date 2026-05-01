# bidict — Injected Bugs

The bidirectional mapping library for Python — bug variants hand-crafted against modern HEAD, drawing from upstream history (jab/bidict).

Total mutations: 6

## Bug Index

| # | Variant | Name | Location | Injection | Fix Commit |
|---|---------|------|----------|-----------|------------|
| 1 | `bidict_none_silently_empty_678c007_1` | `bidict_none_silently_empty` | `bidict/_base.py:438` | `patch` | `678c007d39656fc2305d05fc2ee3c87c5833719e` |
| 2 | `forceput_raises_on_dup_b1d1c71_1` | `forceput_raises_on_dup` | `bidict/_bidict.py:118` | `patch` | `3d8812a1e3669e7083052cf356b00da1c0816a9b` |
| 3 | `ior_returns_new_bidict_6faf1ef_1` | `ior_returns_new_bidict` | `bidict/_bidict.py:176` | `patch` | `6faf1ef03f8fb2c72f289149edf598e5dda0bde1` |
| 4 | `or_mutates_self_2074f4b_1` | `or_mutates_self` | `bidict/_base.py:513` | `patch` | `2074f4b0d88c09cf02335231faf341930afcf400` |
| 5 | `ordered_popitem_last_swapped_b1d1c72_1` | `ordered_popitem_last_swapped` | `bidict/_orderedbidict.py:70` | `patch` | `3d8812a1e3669e7083052cf356b00da1c0816a9b` |
| 6 | `popitem_orphans_inverse_b1d1c70_1` | `popitem_orphans_inverse` | `bidict/_bidict.py:153` | `patch` | `3d8812a1e3669e7083052cf356b00da1c0816a9b` |

## Property Mapping

| Variant | Property | Witness(es) |
|---------|----------|-------------|
| `bidict_none_silently_empty_678c007_1` | `BidictNoneRejected` | `witness_bidict_none_rejected_case_basic` |
| `forceput_raises_on_dup_b1d1c71_1` | `ForceputOverwritesNotRaises` | `witness_forceput_overwrites_not_raises_case_dup_key`, `witness_forceput_overwrites_not_raises_case_dup_val` |
| `ior_returns_new_bidict_6faf1ef_1` | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| `or_mutates_self_2074f4b_1` | `OrDoesNotMutateSelf` | `witness_or_does_not_mutate_self_case_basic` |
| `ordered_popitem_last_swapped_b1d1c72_1` | `OrderedPopitemLastFalseReturnsFirst` | `witness_ordered_popitem_last_false_returns_first_case_basic` |
| `popitem_orphans_inverse_b1d1c70_1` | `PopitemKeepsInverseConsistent` | `witness_popitem_keeps_inverse_consistent_case_basic` |

## Framework Coverage

| Property | proptest | quickcheck | crabcheck | hegel |
|----------|---------:|-----------:|----------:|------:|
| `BidictNoneRejected` | ✓ | ✓ | ✓ | ✓ |
| `ForceputOverwritesNotRaises` | ✓ | ✓ | ✓ | ✓ |
| `IorPreservesIdentity` | ✓ | ✓ | ✓ | ✓ |
| `OrDoesNotMutateSelf` | ✓ | ✓ | ✓ | ✓ |
| `OrderedPopitemLastFalseReturnsFirst` | ✓ | ✓ | ✓ | ✓ |
| `PopitemKeepsInverseConsistent` | ✓ | ✓ | ✓ | ✓ |

## Bug Details

### 1. bidict_none_silently_empty

- **Variant**: `bidict_none_silently_empty_678c007_1`
- **Location**: `bidict/_base.py:438` (inside `BidictBase._update`)
- **Property**: `BidictNoneRejected`
- **Witness(es)**:
  - `witness_bidict_none_rejected_case_basic` — bidict(None) must raise TypeError
- **Source**: [#295](https://github.com/jab/bidict/pull/295), internal — bugfix + rewrite tests + misc. improvements (#295) — Fix bidict(None) bug (should raise TypeError)
  > ``bidict(None)`` should raise TypeError, but pre-fix code in ``BidictBase._update`` skipped the type check and short-circuited on ``not arg`` first, so ``bidict(None)`` silently produced an empty bidict.
- **Fix commit**: `678c007d39656fc2305d05fc2ee3c87c5833719e` — bugfix + rewrite tests + misc. improvements (#295) — Fix bidict(None) bug (should raise TypeError)
- **Invariant violated**: Constructing ``bidict(arg)`` with a non-iterable, non-Maplike ``arg`` (e.g. ``None``) raises TypeError; it must not return an empty bidict.
- **How the mutation triggers**: The mutation removes the ``isinstance(arg, (Iterable, Maplike))`` early-raise from ``_update``, letting the ``if not arg and not kw: return`` short-circuit fire on ``None`` and silently produce an empty bidict.

### 2. forceput_raises_on_dup

- **Variant**: `forceput_raises_on_dup_b1d1c71_1`
- **Location**: `bidict/_bidict.py:118` (inside `MutableBidict.forceput`)
- **Property**: `ForceputOverwritesNotRaises`
- **Witness(es)**:
  - `witness_forceput_overwrites_not_raises_case_dup_key` — duplicate-key forceput must drop the old mapping
  - `witness_forceput_overwrites_not_raises_case_dup_val` — duplicate-value forceput must drop the old mapping
- **Source**: internal — hand-crafted: forceput's contract is unconditional override — must drop_old, not raise
  > ``b.forceput(k, v)`` always overwrites any existing item that duplicates ``k`` or ``v``, by passing ``ON_DUP_DROP_OLD``. A buggy implementation that passes ``ON_DUP_RAISE`` instead turns ``forceput`` into ``put``, raising DuplicationError on the very inputs forceput is supposed to handle.
- **Fix commit**: `3d8812a1e3669e7083052cf356b00da1c0816a9b` — hand-crafted: forceput's contract is unconditional override — must drop_old, not raise
- **Invariant violated**: ``b.forceput(k, v)`` always succeeds without raising; afterwards ``b[k] == v`` and ``b.inv[v] == k``.
- **How the mutation triggers**: The mutation flips ``forceput``'s ``on_dup`` argument from ``ON_DUP_DROP_OLD`` to ``ON_DUP_RAISE``, so any duplicate key or duplicate value triggers a DuplicationError instead of being silently overwritten.

### 3. ior_returns_new_bidict

- **Variant**: `ior_returns_new_bidict_6faf1ef_1`
- **Location**: `bidict/_bidict.py:176` (inside `MutableBidict.__ior__`)
- **Property**: `IorPreservesIdentity`
- **Witness(es)**:
  - `witness_ior_preserves_identity_case_basic` — alias-after-|= must reflect the new items
- **Source**: internal — Fix updating orderedbidict.inv
  > ``b |= other`` must mutate ``b`` in place and return ``b`` itself, mirroring ``dict.__ior__``. A buggy ``__ior__`` that delegates to ``__or__`` rebinds ``b`` to a new bidict — any aliased reference to ``b`` is left pointing at the pre-update contents.
- **Fix commit**: `6faf1ef03f8fb2c72f289149edf598e5dda0bde1` — Fix updating orderedbidict.inv
- **Invariant violated**: After ``b |= other``, ``b`` is the same object as before (``id(b)`` unchanged) and contains the union; any aliased reference observes the new contents.
- **How the mutation triggers**: The mutation replaces ``self.update(other); return self`` with ``return self.__or__(other)``, returning a fresh bidict instead of mutating self. Aliased references to ``b`` continue to see the original contents.

### 4. or_mutates_self

- **Variant**: `or_mutates_self_2074f4b_1`
- **Location**: `bidict/_base.py:513` (inside `BidictBase.__or__`)
- **Property**: `OrDoesNotMutateSelf`
- **Witness(es)**:
  - `witness_or_does_not_mutate_self_case_basic` — a | b must leave a unchanged
- **Source**: internal — implement stricter 1-to-1 checking + many fixes + improvements
  > ``a | b`` must not mutate ``a``. A buggy ``__or__`` that updates ``self`` in place (skipping the ``new = self.copy()`` step) clobbers ``a`` with every union expression.
- **Fix commit**: `2074f4b0d88c09cf02335231faf341930afcf400` — implement stricter 1-to-1 checking + many fixes + improvements
- **Invariant violated**: Computing ``a | b`` returns a fresh bidict and leaves ``a`` unchanged: ``dict(a)`` before and after the ``|`` are equal.
- **How the mutation triggers**: The mutation removes the ``self.copy()`` call from ``__or__``, so the union is applied to ``self`` directly. The expression returns the now-mutated ``self`` instead of a separate result.

### 5. ordered_popitem_last_swapped

- **Variant**: `ordered_popitem_last_swapped_b1d1c72_1`
- **Location**: `bidict/_orderedbidict.py:70` (inside `OrderedBidict.popitem`)
- **Property**: `OrderedPopitemLastFalseReturnsFirst`
- **Witness(es)**:
  - `witness_ordered_popitem_last_false_returns_first_case_basic` — popitem(last=False) must return first; popitem(last=True) must return last
- **Source**: internal — hand-crafted: OrderedBidict.popitem(last=False) must return first item
  > ``OrderedBidict.popitem(last=False)`` must return the first inserted item (LRU-style); ``popitem(last=True)`` returns the most recently inserted item. The mapping is the same as ``collections.OrderedDict.popitem``.
- **Fix commit**: `3d8812a1e3669e7083052cf356b00da1c0816a9b` — hand-crafted: OrderedBidict.popitem(last=False) must return first item
- **Invariant violated**: For an ``OrderedBidict`` with at least two items, ``popitem(last=False)`` returns the first inserted item and ``popitem(last=True)`` returns the most recent.
- **How the mutation triggers**: The mutation flips the ``'prv' if last else 'nxt'`` ternary inside ``OrderedBidict.popitem`` to ``'prv' if not last else 'nxt'``, so the head/tail selection is inverted.

### 6. popitem_orphans_inverse

- **Variant**: `popitem_orphans_inverse_b1d1c70_1`
- **Location**: `bidict/_bidict.py:153` (inside `MutableBidict.popitem`)
- **Property**: `PopitemKeepsInverseConsistent`
- **Witness(es)**:
  - `witness_popitem_keeps_inverse_consistent_case_basic` — popped value must vanish from inverse
- **Source**: internal — hand-crafted: popitem must remove from the inverse mapping
  > ``b.popitem()`` must remove the popped item from both ``_fwdm`` and ``_invm`` so the bidict's two backing dicts stay in sync. A buggy implementation that updates only ``_fwdm`` leaves the popped value as a stale reverse-edge in ``b.inv``.
- **Fix commit**: `3d8812a1e3669e7083052cf356b00da1c0816a9b` — hand-crafted: popitem must remove from the inverse mapping
- **Invariant violated**: After ``b.popitem()`` returns ``(k, v)``, ``k`` is no longer a key of ``b``, ``v`` is no longer a key of ``b.inv``, and ``len(b) == len(b.inv)``.
- **How the mutation triggers**: The mutation drops the ``del self._invm[val]`` line from ``popitem``. ``_fwdm`` shrinks by one, ``_invm`` does not, and the inverse mapping retains a stale reverse-edge for the popped value.
