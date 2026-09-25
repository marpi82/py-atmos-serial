# Contributing to py-atmos-serial

Thanks for helping improve py-atmos-serial.

## How to contribute

1. Open an issue describing the bug or enhancement (optional but appreciated) — use the [issue templates](https://github.com/marpi82/py-atmos-serial/issues/new/choose).
2. Fork the repository and create a feature branch from `main`.
3. Make your changes with tests where practical.
4. Open a pull request against `main` (the [PR template](.github/PULL_REQUEST_TEMPLATE.md) is applied automatically).

Do **not** file security issues publicly — see [SECURITY.md](SECURITY.md).

## Requirements for acceptable contributions

- **Tests**: major new functionality MUST come with tests; bug fixes should add a regression test where practical. Tests must pass without a serial device.
- **Codec**: do not guess framing. A decoder needs a captured fixture and tests.
- **Style**: `ruff format` + `ruff check` clean, `mypy --strict` clean, English only in code and docs, Google-style docstrings. Run `uv run --group dev --group test poe validate` before pushing.
- **DCO**: every commit MUST be signed off (`git commit -s`) to certify the [Developer Certificate of Origin](https://developercertificate.org/).

## Development setup

```bash
uv sync --locked --group dev --group test --group docs --python 3.13
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

## Security reports

Do **not** open a public issue for vulnerabilities. Follow [SECURITY.md](SECURITY.md)
and email `marpi82.dev@google.com`.

## License

By contributing, you agree that your contributions are licensed under the MIT License.

## Branch protection

See [.github/branch-protection-checklist.md](.github/branch-protection-checklist.md).
