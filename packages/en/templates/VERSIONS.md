# VERSIONS.md

This file records releases after a feature group is complete. Version entries are appended by the project-local `tools/semver.py`, usually after the feature group is merged into `main`.

## Versions

### Example

```bash
python tools/semver.py next feature-group --root .
python tools/semver.py next patch --root .
python tools/semver.py prepare 0.1.0 "Create project template" --root .
```

When the user only asks to bump the version, default to patch. During `0.x.x`, new feature groups bump minor only; changes, bug fixes, or adjustments inside an existing feature group bump patch only.
