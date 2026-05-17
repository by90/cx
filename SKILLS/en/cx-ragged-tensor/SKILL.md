---
name: cx-ragged-tensor
description: Use when handling variable-length tensors, padding, masks, lengths, pack or unpack operations, nested tensor-like collections, or distributed-safe batch collation in PyTorch.
version: 1.0.0
---

# cx Ragged Tensor Utilities

## Purpose

Design and maintain reusable utilities for variable-length tensor collections. The goal is to avoid rewriting fragile padding, mask, length, and collation logic across training, evaluation, and metrics code.

Before adding variable-length tensor, indexed tensor series, or batch-packing utilities, use `$cx-common-module` to search the current project, the target documentation set registry, and existing skills for reusable components to extend.

## Preferred API shape

Create small functions before classes:

```python
def lengths_to_mask(lengths, *, max_length=None): ...
def pad_tensor_sequence(tensors, *, padding_value=0, batch_first=True): ...
def unpad_tensor_sequence(padded, lengths, *, batch_first=True): ...
def collate_ragged_tensors(items, *, padding_value=0): ...
```

## Requirements

- Preserve dtype and device unless documented otherwise.
- Validate dimensions early with clear errors.
- Support empty sequence cases intentionally, not accidentally.
- Keep masks boolean.
- Return lengths alongside padded tensors.
- Avoid hidden CPU copies.
- Be cautious in distributed contexts where gathered tensors may need matching shapes.

## Tests

Use `unittest` and cover one item, multiple items, empty cases, zero-length sequences if supported, mismatched feature dimensions, dtype/device preservation, pad to unpad round trips, and mask correctness.
