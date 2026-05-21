# VERSIONS.md

本文件记录完成一组功能后的版本发布。版本条目由项目内 `tools/semver.py` 追加，通常在功能组合并到 `main` 后创建。

## Versions

### 示例

```bash
python tools/semver.py next feature-group --root .
python tools/semver.py next patch --root .
python tools/semver.py prepare 0.1.0 "创建项目模板" --root .
```

`0.x.x` 阶段新增功能组只更新 minor；既有功能组内修改、bug 修复或调整只更新 patch。
