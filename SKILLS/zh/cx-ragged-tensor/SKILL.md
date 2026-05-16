---
name: cx-ragged-tensor
description: 用于 variable-length tensors、padding、masks、lengths、pack/unpack、nested tensor-like collections 和 PyTorch distributed-safe batch collation。
version: 1.0.0
---

# cx 变长 Tensor 工具

## 目的

设计和维护变长 tensor 集合的可复用工具。目标是避免在训练、评估和 metrics 中反复写脆弱的 padding、mask、length 和 collation 逻辑。

## 推荐 API 形态

先写小函数，再考虑类：

```python
def lengths_to_mask(lengths, *, max_length=None): ...
def pad_tensor_sequence(tensors, *, padding_value=0, batch_first=True): ...
def unpad_tensor_sequence(padded, lengths, *, batch_first=True): ...
def collate_ragged_tensors(items, *, padding_value=0): ...
```

## 要求

- 除非文档明确说明，否则保留 dtype 和 device。
- 尽早验证维度，并给出清晰错误。
- 有意支持或拒绝空序列，不要让行为偶然发生。
- mask 保持 boolean。
- 返回 padded tensor 的同时返回 lengths。
- 避免隐藏的 CPU copy。
- 分布式场景要注意 collective 操作可能需要相同 shape。

## 测试

使用 `unittest`，覆盖单项、多项、空输入、支持时的零长度序列、feature 维度不匹配、dtype/device 保留、pad 到 unpad 的 round trip，以及 mask 正确性。
