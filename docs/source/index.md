
```{image} _static/images/logo-light.svg
:width: 400
:align: center
:alt: framecat
:class: only-light
```

```{image} _static/images/logo-dark.svg
:width: 400
:align: center
:alt: framecat
:class: only-dark
```

# framecat

|build| |nbsp| |docs| |nbsp| |coverage|

:code:`framecat` provides simple tools to automate video and gif generation from frame sequences via a command-line interface.


Framecat provides simple tools to automate video and gif generation from frame sequences.

Try it quickly by following this [**tutorial**](quickstart).



Our core API, :func:`tyro.cli()`,

- **Generates CLI interfaces** from a comprehensive set of Python type
  constructs.
- **Populates helptext automatically** from defaults, annotations, and
  docstrings.
- **Understands nesting** of `dataclasses`, `pydantic`, and `attrs` structures.
- **Prioritizes static analysis** for type checking and autocompletion with
  tools like
  [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance),
  [Pyright](https://github.com/microsoft/pyright), and
  [mypy](https://github.com/python/mypy).

For advanced users, it also supports:

- **Subcommands**, as well as choosing between and overriding values in
  configuration objects.
- **Completion script generation** for `bash`, `zsh`, and `tcsh`.
- **Fine-grained configuration** via [PEP
  593](https://peps.python.org/pep-0593/) annotations (`tyro.conf.*`).

To get started, we recommend browsing the examples to the left.

### Why `tyro`?

1. **Strong typing.**

   Unlike tools dependent on dictionaries, YAML, or dynamic namespaces,
   arguments populated by `tyro` benefit from IDE and language server-supported
   operations — think tab completion, rename, jump-to-def, docstrings on hover —
   as well as static checking tools like `pyright` and `mypy`.

2. **Minimal overhead.**

   Standard Python type annotations, docstrings, and default values are parsed
   to automatically generate command-line interfaces with informative helptext.

   `tyro` works seamlessly with tools you already use: examples are included for
   [dataclasses](https://docs.python.org/3/library/dataclasses.html),
   [attrs](https://www.attrs.org/),
   [pydantic](https://pydantic-docs.helpmanual.io/),
   [flax.linen](https://flax.readthedocs.io/en/latest/api_reference/flax.linen.html),
   and more.

3. **Modularity.**

   `tyro` supports hierarchical configuration structures, which make it easy to
   distribute definitions, defaults, and documentation of configurable fields
   across modules or source files.

4. **Tab completion.**

   By extending [shtab](https://github.com/iterative/shtab), `tyro`
   automatically generates tab completion scripts for bash, zsh, and tcsh.

<!-- prettier-ignore-start -->

.. toctree::
   :caption: Getting started
   :hidden:
   :maxdepth: 1
   :titlesonly:

   quickstart

.. toctree::
   :caption: Getting started old
   :hidden:
   :maxdepth: 1
   :titlesonly:

   installation
   your_first_cli

.. toctree::
   :caption: Basics
   :hidden:
   :maxdepth: 1
   :titlesonly:
   :glob:

   examples/01_basics/*


.. toctree::
   :caption: Hierarchies
   :hidden:
   :maxdepth: 1
   :titlesonly:
   :glob:

   examples/02_nesting/*


.. toctree::
   :caption: Config Management
   :hidden:
   :maxdepth: 1
   :titlesonly:
   :glob:

   examples/03_config_systems/*


.. toctree::
   :caption: Additional Features
   :hidden:
   :maxdepth: 1
   :titlesonly:
   :glob:

   examples/04_additional/*


.. toctree::
   :caption: Notes
   :hidden:
   :maxdepth: 5
   :glob:

   goals_and_alternatives
   helptext_generation
   tab_completion






.. |build| image:: https://github.com/simon-lc/framecat/actions/workflows/build.yml/badge.svg
   :alt: Build status icon
   :target: https://github.com/simon-lc/framecat
.. |docs| image:: https://github.com/simon-lc/framecat/actions/workflows/docs.yml/badge.svg
   :alt: Docs status icon
   :target: https://github.com/simon-lc/framecat
.. |coverage| image:: https://codecov.io/gh/simon-lc/framecat/graph/badge.svg?token=CUWTT7EK5E
   :alt: Test coverage status icon
   :target: https://github.com/simon-lc/framecat
.. |nbsp| unicode:: 0xA0
   :trim:

<!-- prettier-ignore-end -->
