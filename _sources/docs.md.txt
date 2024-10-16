# Building documentation

## Github pages deployment setting
Use the following settings for the Github pages deployment:

![framecat logo](_static/images/gh-pages-settings.png)

## Building locally
Go to package root
```
cd ~/framecat
```

Create a virtual environment `.docs_venv`
```
python -m venv .docs_venv
source .docs_venv/bin/activate
```

Install documentation dependencies
```
pip install uv
uv pip install --system -e ".[dev]"
uv pip install --system -r docs/requirements.txt
```

Build the documentation
```
sphinx-build docs/source docs/build -b dirhtml
```

To fail when there is a warning, you can add the `-W` flag
```
sphinx-build docs/source docs/build -W -b dirhtml
```

Serve the documentation locally
```
python -m http.server --directory docs/build 8000
```

Clean up built documentation
```
rm -rf docs/build
```




# Documentation related packages
    "pytest>=7.1.2",
    "pytest-cov>=3.0.0",
    "torch>=1.10.0",
    "pyright>=1.1.349,!=1.1.379",
    "ruff>=0.1.13",
    "mypy>=1.4.1",
    # As of 7/27/2023, flax install fails for Python 3.7 without pinning to an
    # old version. But doing so breaks other Python versions.
    "flax>=0.6.9;python_version>='3.8'",
    "pydantic>=2.5.2",
    "coverage[toml]>=6.5.0",
dev = [
    "PyYAML>=6.0",
    "frozendict>=2.3.4",
    "omegaconf>=2.2.2",
    "attrs>=21.4.0",
    "numpy>=1.20.0",
    "eval_type_backport>=0.1.3",
]


# "git+https://github.com/brentyi/ansi.git",
# "git+https://github.com/brentyi/sphinxcontrib-programoutput.git",
