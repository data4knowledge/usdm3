# Dependency version relaxation

## Summary

Three dependencies in `setup.py` need their exact version pins (`==`) relaxed to compatible ranges so that `usdm3` can be installed alongside `cdisc-rules-engine` in the `usdm4` package.

## Background

The `usdm4` package depends on both `usdm3` and `cdisc-rules-engine`. Both packages pin some of the same transitive dependencies at different exact versions, making it impossible for pip to resolve a consistent set of packages.

On Python 3.10, the newest usable `cdisc-rules-engine` is **0.10.0** (versions 0.11.0+ require Python 3.12). Every version of `cdisc-rules-engine` that supports Python 3.10 (0.9.2, 0.9.3, 0.10.0) conflicts with `usdm3==0.12.1` on at least one of the dependencies below.

Attempting to install both packages produces errors like:

```
ERROR: Cannot install cdisc-rules-engine==0.10.0 and usdm3==0.12.1 because
these package versions have conflicting dependencies.

The conflict is caused by:
    usdm3 0.12.1 depends on jsonschema==4.23.0
    cdisc-rules-engine 0.10.0 depends on jsonschema==4.18.5
```

## Conflicts

| Dependency     | usdm3 0.12.1 (current) | cdisc-rules-engine 0.10.0 | cdisc-rules-engine 0.9.2 |
|----------------|------------------------|---------------------------|--------------------------|
| jsonschema     | ==4.23.0               | ==4.18.5                  | (not pinned)             |
| python-dotenv  | ==1.0.1                | ==0.20.0                  | ==0.20.0                 |
| pyyaml         | ==6.0.1                | ==6.0.2                   | (not specified)          |

## Proposed changes to `setup.py`

```python
install_requires=[
    "pydantic==2.7.3",               # unchanged
    "beautifulsoup4==4.12.3",        # unchanged
    "pyyaml>=6.0.1,<7",             # was ==6.0.1
    "simple_error_log>=0.6.0",       # unchanged
    "jsonschema>=4.18.0,<5",        # was ==4.23.0
    "python-dotenv>=0.20.0,<2",     # was ==1.0.1
    "requests==2.32.3",              # unchanged
],
```

The `requirements.txt` file should be updated to match, changing the same three entries.

## Rationale for each change

### jsonschema: `==4.23.0` to `>=4.18.0,<5`

usdm3 uses three imports from jsonschema:

- `validate` (stable API, unchanged across 4.x)
- `RefResolver` (deprecated since 4.18.0 but still present and functional in 4.26+)
- `ValidationError` (stable API, unchanged across 4.x)

Both 4.18.5 and 4.23.0 work identically for this usage. The lower bound of 4.18.0 is the version where `RefResolver` was formally deprecated but retained, so it is the oldest version guaranteed to have the current behaviour.

### python-dotenv: `==1.0.1` to `>=0.20.0,<2`

usdm3 does not import `python-dotenv` anywhere in its library source code. It is listed as a dependency for developer/test tooling convenience (and also appears in `tests_require`). The public API used by callers (`dotenv.load_dotenv()`, `dotenv_values()`) is stable across 0.20.0 through 1.0.1.

### pyyaml: `==6.0.1` to `>=6.0.1,<7`

usdm3 uses `yaml.load(Loader=yaml.FullLoader)`, `yaml.safe_load`, and `yaml.dump`. These APIs have not changed between 6.0.1 and 6.0.2. The difference is a single patch release.

## Verification

A clean virtual environment test confirms the relaxed ranges resolve correctly:

```bash
python3 -m venv test_env
source test_env/bin/activate
pip install \
  "pydantic==2.7.3" \
  "beautifulsoup4==4.12.3" \
  "jsonschema>=4.18.0,<5" \
  "python-dotenv>=0.20.0,<2" \
  "pyyaml>=6.0.1,<7" \
  "requests==2.32.3" \
  "simple_error_log>=0.6.0" \
  "cdisc-rules-engine==0.10.0"
```

Result: pip resolves to jsonschema 4.18.5, python-dotenv 0.20.0, pyyaml 6.0.2. `pip check` reports no broken requirements. All imports work correctly.

## Corresponding changes in usdm4

After this usdm3 release, `usdm4` should update its `setup.py`:

- Change `usdm3==0.12.1` to `usdm3>=0.12.2` (or whatever version number this release gets)
- Change `cdisc-rules-engine` to `cdisc-rules-engine==0.10.0`

## Future considerations

- `RefResolver` will eventually be removed from jsonschema. When that happens, usdm3 should migrate to the `referencing` library. This is not urgent as `RefResolver` remains available in jsonschema 4.26+.
- `cdisc-rules-engine` 0.11.0+ requires Python 3.12. When usdm3/usdm4 move to Python 3.12, the CRE version pin can be updated to access newer rule sets.
