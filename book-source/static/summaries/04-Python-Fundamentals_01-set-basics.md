---
original_path: docs/04-Python-Fundamentals/19-set-frozenset-gc/01-set-basics.md
chapter: 04-Python-Fundamentals
difficulty: beginner
read_time: 50 minutes
generated: 2025-11-15
---

# Summary

Sets are Python's solution for storing unique, unordered collections with O(1) lookup time through hash-based storage. This lesson introduces set creation using literal syntax `{1, 2, 3}` and the `set()` constructor, emphasizing proper type hints like `set[int]`. Sets automatically eliminate duplicates, making them ideal for deduplication tasks. The key constraint is hashability - sets can only contain immutable elements (integers, strings, tuples, frozensets) because hash values must remain stable. The lesson covers three modification methods: `.add()` to insert elements, `.remove()` which raises errors if the element doesn't exist, and `.discard()` which silently does nothing for missing elements. Through practical examples like deduplicating email lists and tracking unique user IDs, students learn when to choose sets over lists based on uniqueness requirements.

## Key Concepts

- Sets store unique elements using hash-based storage for O(1) average lookup performance
- Create sets with literal syntax `{1, 2, 3}` or constructor `set()` with proper type hints
- Only immutable (hashable) types can be set elements - lists and dicts are forbidden
- `.add()` inserts elements, `.remove()` errors on missing elements, `.discard()` does not
- Automatic duplicate elimination makes sets ideal for uniqueness requirements