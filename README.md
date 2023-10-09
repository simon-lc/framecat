## FrameCat
[![build](https://github.com/simon-lc/framecat/actions/workflows/build.yml/badge.svg)](https://github.com/simon-lc/framecat/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/simon-lc/framecat/graph/badge.svg?token=CUWTT7EK5E)](https://codecov.io/gh/simon-lc/framecat)

**Use this tool to automate video and gif generation from (Meshcat-generated) frame sequences.**

### Install package
```
pip install framecat
```
### Install external libraries
**FFmpeg**
```
sudo apt update
sudo apt install ffmpeg
ffmpeg --version
```

**gifsicle**
```
sudo apt update
sudo apt install -y gifsicle
gifsicle --version
```

### Quick start
- Make sure you're not inside a Docker container.
- `cd` to the root folder `~/workspace/framecat`. 
```
user@username~/workspace/framecat$
```

#### `LATEST` mode
- execute the command in the `LATEST` input mode: 
```
python cli/render.py latest --output-names name1 name2
```
- this will pull the latest 2 `.tar` files created in the `--input-folder` (defaults to `~/Downloads`).
- rename the `.tar` files as `name1.tar` and `name2.tar`.
- create a video, a GIF and a lossy GIF for each `.tar` file. 
- store them in the `--output-folder` (defaults to `~/Videos/meshcat`).


#### `BY-NAME` mode
- execute the command in the `BY-NAME` input mode:
```
python cli/render.py ny-name --input-names in_name1 --output-names out_name1`
```
- this will pull the `in_name1.tar` file from the `--input-folder` (defaults to `~/Downloads`).
- rename the `.tar` file as `out_name1.tar`.
- create a video, a GIF and a lossy GIF for each `.tar` file. 
- store these in the `--output-folder` (defaults to `~/Videos/meshcat`).
