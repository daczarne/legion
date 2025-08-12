# Setting up the local environment

This guide explains how to setup the basic local environment that comes with this repository. For more specialized use
cases, update and modify as needed.

## Creating a new environment with Pipenv

The environment includes the following packages:

- [PyYAML][pyyaml-repo]
- [YAMLlint][yamllint-repo]
- [Pytest][pytest-repo]

---
To create a new environment using the `Pipfile.lock` run the following commands:

```shell
pipenv --python 3.10
```

```shell
pipenv shell
```

```shell
pipenv sync
```

```shell
pipenv sync --dev
```

You can verify that the environment was correctly created by running:

```shell
$ python --version
Python 3.13.3
```

```shell
$ pipenv graph
sqlfluff==3.4.0
├── chardet
├── click
├── colorama
├── diff_cover
│   ├── chardet
│   ├── Jinja2
│   │   └── MarkupSafe
│   ├── pluggy
│   └── Pygments
├── Jinja2
│   └── MarkupSafe
├── pathspec
├── platformdirs
├── pytest
│   ├── iniconfig
│   ├── packaging
│   └── pluggy
├── PyYAML
├── regex
├── tblib
└── tqdm
yamllint==1.37.1
├── pathspec
└── PyYAML
```

The output of the `pipenv graph` command might look slightly different in the future, but the main packages should be
there.

## Set the correct interpreter

Once the environment has been setup, make sure to update the path to the correct Python interpreter in
`.vscode/settings.json`.

```json
{
    "python.defaultInterpreterPath": "~/.local/share/virtualenvs/<venv_name>/bin/python",
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

This tool uses two configuration files

- `.markdownlint.yaml` defines the rules that Md files need to follow.
- `.markdownlint-cli2.yaml` controls the behavior of the CLI tool. This configuration already ignors Md files created
  inside some untraced folders like `pycache`.

**Reference documents**:

- [Markdown lint][1]
- [Markdown lint CLI][2]
- [Markdown lint action][3]

## Running CSpell locally

To run CSpell locally use:

```shell
cspell lint --config ".cspell.json" --dot .
```

**Reference documents**:

- [CSpell][4]
- [CSpell CLI][5]

[pyyaml-repo]: https://github.com/yaml/pyyaml
[yamllint-repo]: https://github.com/adrienverge/yamllint
[pytest-repo]: https://github.com/pytest-dev/pytest

[1]: https://github.com/DavidAnson/markdownlint
[2]: https://github.com/DavidAnson/markdownlint-cli2
[3]: https://github.com/DavidAnson/markdownlint-cli2-action
[4]: https://github.com/streetsidesoftware/cspell/tree/main
[5]: https://github.com/streetsidesoftware/cspell/tree/main/packages/cspell
