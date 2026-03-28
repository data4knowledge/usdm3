# USDM3

A Python library for the CDISC TransCelerate Unified Study Data Model (USDM) Version 3.

## Project overview

USDM3 provides base infrastructure for working with USDM data: API model classes (Pydantic-based), controlled terminology libraries (CDISC CT, ISO 3166/639), biomedical concept support, validation rules, and utilities such as ID management and file caching. It is also a dependency of the `usdm4` package.

## Structure

- `src/usdm3/` — package source
  - `api/` — Pydantic domain model classes
  - `bc/cdisc/` — biomedical concept library and cache
  - `ct/cdisc/` — CDISC controlled terminology library, config, and missing CT handling
  - `rules/` — validation rule implementations and schema validation
  - `base/` — shared utilities (ID manager, singleton, API instance factory)
  - `file_cache/` — YAML-based file caching
- `tests/` — pytest test suite (mirrors `src/` structure)
- `docs/` — project documentation
- `setup.py` — package metadata and dependencies
- `requirements.txt` — development dependencies (includes test and build tools)

## Key dependencies

The package depends on:
- `pydantic` — API model validation and serialisation
- `beautifulsoup4` — HTML parsing
- `jsonschema` — JSON Schema validation (uses `validate`, `RefResolver`, `ValidationError`)
- `pyyaml` — YAML loading for CT config, missing CT data, and file cache
- `requests` — HTTP client for CDISC Library API access
- `simple_error_log` — error collection and reporting
- `python-dotenv` — environment variable loading (used in test/dev tooling only, not imported by library code)

### Dependency version policy

Some dependencies use exact pins (`==`), others use compatible ranges (`>=`). When changing dependency versions, be aware that `usdm3` is consumed by `usdm4`, which also depends on `cdisc-rules-engine`. Pins that are too strict can cause irreconcilable conflicts between the two dependency trees. Prefer compatible ranges (`>=x.y,<z`) over exact pins unless there is a known incompatibility with a specific version. See `docs/DEPENDENCY_RELAXATION.md` for the full rationale and history.

## Development

- Format: `ruff format`
- Lint: `ruff check`
- Test: `pytest` (requires 100% coverage)
- Build: `python3 -m build --sdist --wheel`
- Publish: `twine upload dist/*`

## Notes

- Version is defined in `src/usdm3/__info__.py` (`__package_version__` and `__model_version__`)
- The `RefResolver` import from `jsonschema` is deprecated since v4.18.0 but still functional through v4.26+. A future migration to the `referencing` library will be needed eventually but is not urgent.
