"""Property functions for the bidict ETNA workload.

Each property is pure, total, deterministic. Returns PropertyResult.
PASS when the invariant holds, fail(...) when violated, DISCARD when the
input does not satisfy the precondition the property checks.
"""
from __future__ import annotations

from typing import List, Tuple

from bidict import OrderedBidict, bidict

from ._result import DISCARD, PASS, PropertyResult, fail


def _dedupe_keep_unique(pairs: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Keep only pairs whose key and value are both unique across the list.

    bidict refuses inserts that duplicate any existing key or value, so any
    tuple list must already be 1-to-1 for property bodies to call bidict()
    without raising. Used to filter Hypothesis-generated data.
    """
    seen_keys: set = set()
    seen_vals: set = set()
    out: List[Tuple[int, int]] = []
    for k, v in pairs:
        if k in seen_keys or v in seen_vals:
            continue
        seen_keys.add(k)
        seen_vals.add(v)
        out.append((k, v))
    return out


# ---------------------------------------------------------------------------
# BidictNoneRejected (variant: bidict_none_silently_empty_678c007_1)
# ---------------------------------------------------------------------------
def property_bidict_none_rejected(args: int) -> PropertyResult:
    """``bidict(None)`` must raise TypeError; it must not silently produce an empty bidict.

    Bug (mined from #295 / commit 678c007): the pre-fix ``_update`` did not
    type-check ``arg`` before the ``if not arg and not kw: return`` guard,
    so ``bidict(None)`` returned an empty bidict instead of raising.
    """
    # The argument is a single int we ignore — it merely seeds Hypothesis.
    _ = args
    try:
        result = bidict(None)  # type: ignore[arg-type]
    except TypeError:
        return PASS
    return fail(f"bidict(None) did not raise TypeError; got {result!r}")


# ---------------------------------------------------------------------------
# IorPreservesIdentity (variant: ior_returns_new_bidict_6faf1ef_1)
# ---------------------------------------------------------------------------
def property_ior_preserves_identity(args: Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]) -> PropertyResult:
    """``b |= other`` must mutate ``b`` in place and return ``b`` itself.

    Bug (synthetic, inspired by 6faf1ef "Fix updating orderedbidict.inv"):
    binding ``__ior__`` to a non-mutating implementation rebinds ``b`` to a
    fresh bidict, leaving any aliased reference pointing at the old contents.
    """
    initial_pairs, addition_pairs = args
    initial = _dedupe_keep_unique(initial_pairs)
    additions_uniq = _dedupe_keep_unique(addition_pairs)

    # Drop additions whose key or value already lives in initial under a
    # different mapping — bidict's default ON_DUP raises on value duplication
    # so feeding such inputs would obscure the test signal.
    init_keys = {k for k, _ in initial}
    init_vals = {v for _, v in initial}
    additions: List[Tuple[int, int]] = []
    for k, v in additions_uniq:
        if k in init_keys and v in init_vals:
            # exact-or-compatible no-op only — skip (bidict raises on key+val
            # duplication that doesn't match an existing item).
            continue
        if v in init_vals:
            # value duplication: would raise ValueDuplicationError under
            # default on_dup. Skip.
            continue
        additions.append((k, v))

    b = bidict(initial)
    aliased = b
    snapshot_id = id(b)
    b |= dict(additions)

    if id(b) != snapshot_id:
        return fail(
            f"ior_preserves_identity({initial!r}, {additions!r}): "
            f"|= rebound to a new object; aliased ref now stale: "
            f"aliased={dict(aliased)!r}, b={dict(b)!r}"
        )

    expected = dict(initial)
    for k, v in additions:
        expected[k] = v
    if dict(aliased) != expected:
        return fail(
            f"ior_preserves_identity({initial!r}, {additions!r}): "
            f"aliased contents {dict(aliased)!r} != expected {expected!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# OrDoesNotMutateSelf (variant: or_mutates_self_2074f4b_1)
# ---------------------------------------------------------------------------
def property_or_does_not_mutate_self(args: Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]) -> PropertyResult:
    """``a | b`` must not mutate ``a``. The dict ``|`` operator is non-mutating.

    Bug (synthetic, inspired by upstream "stricter 1-to-1 checking" rewrite):
    a buggy ``__or__`` that updates ``self`` instead of a fresh copy leaves
    ``a`` clobbered after every ``a | b``.
    """
    initial_pairs, other_pairs = args
    initial = _dedupe_keep_unique(initial_pairs)
    other_uniq = _dedupe_keep_unique(other_pairs)

    init_vals = {v for _, v in initial}
    other: List[Tuple[int, int]] = []
    for k, v in other_uniq:
        if v in init_vals and (k, v) not in initial:
            # value duplication that would raise — skip.
            continue
        other.append((k, v))

    a = bidict(initial)
    snapshot = dict(a)
    _ = a | dict(other)
    after = dict(a)

    if after != snapshot:
        return fail(
            f"or_does_not_mutate_self({initial!r}, {other!r}): "
            f"a was mutated by `a | b`: before={snapshot!r}, after={after!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# PopitemKeepsInverseConsistent (variant: popitem_orphans_inverse_b1d1c70_1)
# ---------------------------------------------------------------------------
def property_popitem_keeps_inverse_consistent(args: List[Tuple[int, int]]) -> PropertyResult:
    """After ``b.popitem()``, the popped value must no longer be a key of ``b.inv``.

    Bug (synthetic): a buggy ``popitem`` that removes from ``_fwdm`` but not
    ``_invm`` leaves the inverse mapping with an orphaned reverse-edge.
    """
    pairs = _dedupe_keep_unique(args)
    if not pairs:
        return DISCARD

    b = bidict(pairs)
    k, v = b.popitem()

    if k in b:
        return fail(
            f"popitem_keeps_inverse_consistent({pairs!r}): popped key {k!r} still in fwd: {dict(b)!r}"
        )
    if v in b.inv:
        return fail(
            f"popitem_keeps_inverse_consistent({pairs!r}): "
            f"popped value {v!r} still in inverse: inv={dict(b.inv)!r}"
        )
    if len(b) != len(b.inv):
        return fail(
            f"popitem_keeps_inverse_consistent({pairs!r}): "
            f"len mismatch after popitem: fwd={len(b)} inv={len(b.inv)}"
        )
    return PASS


# ---------------------------------------------------------------------------
# ForceputOverwritesNotRaises (variant: forceput_raises_on_dup_b1d1c71_1)
# ---------------------------------------------------------------------------
def property_forceput_overwrites_not_raises(args: Tuple[List[Tuple[int, int]], int, int]) -> PropertyResult:
    """``b.forceput(k, v)`` must always succeed; it must never raise DuplicationError.

    Bug (synthetic): if forceput passes ON_DUP_RAISE instead of ON_DUP_DROP_OLD,
    a forceput onto an existing key or value raises instead of overwriting.
    """
    pairs_list, k, v = args
    pairs = _dedupe_keep_unique(pairs_list)
    b = bidict(pairs)
    try:
        b.forceput(k, v)
    except Exception as e:
        return fail(
            f"forceput_overwrites_not_raises({pairs!r}, {k!r}, {v!r}): "
            f"forceput raised {type(e).__name__}: {e}"
        )
    if b.get(k) != v:
        return fail(
            f"forceput_overwrites_not_raises({pairs!r}, {k!r}, {v!r}): "
            f"after forceput, b[{k!r}]={b.get(k)!r} expected {v!r}"
        )
    if b.inv.get(v) != k:
        return fail(
            f"forceput_overwrites_not_raises({pairs!r}, {k!r}, {v!r}): "
            f"after forceput, b.inv[{v!r}]={b.inv.get(v)!r} expected {k!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# OrderedPopitemLastFalseReturnsFirst (variant: ordered_popitem_last_swapped_b1d1c72_1)
# ---------------------------------------------------------------------------
def property_ordered_popitem_last_false_returns_first(
    args: List[Tuple[int, int]],
) -> PropertyResult:
    """``OrderedBidict.popitem(last=False)`` must return the first inserted item;
    ``popitem(last=True)`` must return the most recently inserted item.

    Bug (synthetic): swapping the ``'prv' if last else 'nxt'`` ternary inverts
    the relationship — popitem(last=False) returns the last-inserted item.
    """
    pairs = _dedupe_keep_unique(args)
    if len(pairs) < 2:
        return DISCARD

    ob_first = OrderedBidict(pairs)
    expected_first = pairs[0]
    got_first = ob_first.popitem(last=False)
    if got_first != expected_first:
        return fail(
            f"ordered_popitem_last_false_returns_first({pairs!r}): "
            f"popitem(last=False) returned {got_first!r}, expected {expected_first!r}"
        )

    ob_last = OrderedBidict(pairs)
    expected_last = pairs[-1]
    got_last = ob_last.popitem(last=True)
    if got_last != expected_last:
        return fail(
            f"ordered_popitem_last_false_returns_first({pairs!r}): "
            f"popitem(last=True) returned {got_last!r}, expected {expected_last!r}"
        )
    return PASS
