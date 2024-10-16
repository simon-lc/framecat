# Building documentation

## Github pages deplyoment setting
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
pip install -e .[docs]
```

Build the documentation
```
sphinx-build docs docs/_build  --keep-going
```

To fail when there is a warning, you can add the `-W` flag
```
sphinx-build docs docs/_build -W --keep-going
```

Serve the documentation locally
```
python -m http.server --directory docs/_build 8000
```

Clean up built documentation
```
rm -rf docs/_build
```
