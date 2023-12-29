## FrameCat
[![build](https://github.com/simon-lc/framecat/actions/workflows/build.yml/badge.svg)](https://github.com/simon-lc/framecat/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/simon-lc/framecat/graph/badge.svg?token=CUWTT7EK5E)](https://codecov.io/gh/simon-lc/framecat)

**Generate videos and GIF and low-memory footprint GIF from frame sequences, video and GIF sources.**

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
- Create a virtual environment if needed
```
pip install framecat
```

#### `LATEST` mode
- execute the command in the `LATEST` input mode: 
```
framecat latest --output-names name1 name2
```
- this will pull the latest 2 `.tar` files created in the `--input-folder` (defaults to `~/Downloads`).
- rename the `.tar` files as `name1.tar` and `name2.tar`.
- create a video, a GIF and a lossy GIF for each `.tar` file. 
- store them in the `--output-folder` (defaults to `~/Videos/framecat`).


#### `BY-NAME` mode
- execute the command in the `BY-NAME` input mode:
```
framecat by-name --input-names in_name1 --output-names out_name1`
```
- this will pull the `in_name1.tar` file from the `--input-folder` (defaults to `~/Downloads`).
- rename the `.tar` file as `out_name1.tar`.
- create a video, a GIF and a lossy GIF for each `.tar` file. 
- store these in the `--output-folder` (defaults to `~/Videos/framecat`).


#### Input type
We can choose to run the `framecat` command on different file types:
- on 'tar' files, this command will create a video, a GIF and a lossy GIF. This is the default mode. 
```
framecat latest --input-type tar --output-names out_name1`
```
or equivalently:
```
framecat latest --output-names out_name1`
```
- on 'mp4' files, this command will create a GIF and a lossy GIF. 
```
framecat latest --input-type mp4 --output-names out_name1`
```
- on 'gif' files, this command will create a lossy GIF.
```
framecat latest --input-type gif --output-names out_name1`
```