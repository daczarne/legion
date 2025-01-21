# Legion gold

This project is a CLI that allows to compare different production scenarios for a given city in Legion Gold.

## Creating a new environment with Pipenv

To create a new environment using the `Pipfile.lock` run the following commands:

```zsh
pipenv --python 3.10
```

```zsh
pipenv shell
```

```zsh
pipenv sync
```

```zsh
pipenv sync --dev
```

You can verify that the environment was correctly created by running:

```zsh
pipenv shell
```

```zsh
$ python --version
Python 3.10.1
```

```zsh
$ pipenv graph
pytest==8.3.3
├── exceptiongroup [required: >=1.0.0rc8, installed: 1.2.2]
├── iniconfig [required: Any, installed: 2.0.0]
├── packaging [required: Any, installed: 24.1]
├── pluggy [required: >=1.5,<2, installed: 1.5.0]
└── tomli [required: >=1, installed: 2.0.1]
yamllint==1.32.0
├── pathspec [required: >=0.5.3, installed: 0.12.1]
└── PyYAML [required: Any, installed: 6.0.2]
```

## Running YAMLlint locally

You can run YAMLling locally with:

```zsh
yamllint -c .yamllint.yaml .
```

## Running Markdown lint locally

To run Md lint locally, first make sure that the CLI is installed. To install globally use:

```zsh
brew install markdownlint-cli2
```

Once installed, it can be run locally via:

```zsh
markdownlint-cli2 --config ".markdownlint.yaml" "**/*.md"
```

**Reference documents**:

- [Markdown lint][1]
- [Markdown lint CLI][2]
- [Markdown lint action][3]

## Running SQLFluff locally

If the project uses also SQL files, these can be linted with:

```zsh
sqlfluff lint --config .sqlfluff .
```

## Running CSpell locally

To run CSpell locally use:

```zsh
cspell lint --config ".cspell.json" "**/*.md"
```

**Reference documents**:

- [CSpell][4]
- [CSpell CLI][5]

[1]: https://github.com/DavidAnson/markdownlint
[2]: https://github.com/DavidAnson/markdownlint-cli2
[3]: https://github.com/DavidAnson/markdownlint-cli2-action
[4]: https://github.com/streetsidesoftware/cspell/tree/main
[5]: https://github.com/streetsidesoftware/cspell/tree/main/packages/cspell
