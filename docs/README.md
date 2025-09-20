# Setting up the local environment

This guide explains how to setup the local environment.

## Creating a new environment with `uv`

The environment includes the following libraries:

- [`PyYAML`][pyyaml-repo]
- [`rich`][rich-repo]

And the following dev libraries:

- [`isort`][isort-repo]
- [`YAMLlint`][yamllint-repo]
- [`pytest`][pytest-repo]

To create a new environment using the `uv.lock` run the following commands:

```shell
uv sync --locked --all-extras --dev
```

## Set the correct interpreter

Once the environment has been setup, make sure to update the path to the correct Python interpreter in
`.vscode/settings.json`.

```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
}
```

This will ensure that when VS Code is launched the correct environment will be automatically loaded.

## Running YAMLlint locally

To run YAMLlint locally use:

```shell
yamllint -c .yamllint.yaml .
```

## Running Markdown lint locally

To run Markdownlint locally use:

```shell
markdownlint-cli2 --config ".markdownlint.yaml" .
```

Beware of local, untracked files that may cause this to fail. If they are inside py-cached folders, these can usually
be removed safely.

This tool uses two configuration files:

- `.markdownlint.yaml` defines the rules that Md files need to follow.
- `.markdownlint-cli2.yaml` controls the behavior of the CLI tool. This configuration already ignors Md files created
  inside some untracked folders like `pycache`.

**Reference documents**:

- [Markdown lint][markdown-lint-repo]
- [Markdown lint CLI][markdown-lint-cli-repo]
- [Markdown lint action][markdown-lint-action-repo]

## Running CSpell locally

To run CSpell locally use:

```shell
cspell lint --config ".cspell.json" --dot .
```

**Reference documents**:

- [CSpell][cspell-repo]
- [CSpell CLI][cspell-cli-repo]

## Running isort locally

To run isort locally use:

```shell
uv run isort --check-only --verbose --color --sp pyproject.toml .
```

[cspell-cli-repo]: https://github.com/streetsidesoftware/cspell/tree/main/packages/cspell
[cspell-repo]: https://github.com/streetsidesoftware/cspell/tree/main
[markdown-lint-action-repo]: https://github.com/DavidAnson/markdownlint-cli2-action
[markdown-lint-cli-repo]: https://github.com/DavidAnson/markdownlint-cli2
[markdown-lint-repo]: https://github.com/DavidAnson/markdownlint
[pytest-repo]: https://github.com/pytest-dev/pytest
[pyyaml-repo]: https://github.com/yaml/pyyaml
[yamllint-repo]: https://github.com/adrienverge/yamllint
[rich-repo]: https://github.com/Textualize/rich
[isort-repo]: https://github.com/PyCQA/isort
