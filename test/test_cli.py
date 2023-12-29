import os
import glob
import pytest
import argparse
from framecat.command import (
    execute_command,
    parse_args,
)
from framecat.rendering import InputType


# directories
test_dir = os.path.dirname(os.path.abspath(__file__))
package_dir = os.path.dirname(test_dir)
assets_dir = os.path.join(package_dir, "assets")

# Define test cases as tuples with input arguments and expected output
latest_case = ["latest", "--input-folder", assets_dir, "--output-folder", assets_dir, 
         "--output-names", "cli_test_latest", "--dont-rename-input-file",
         "--gif-framerate", "30", "--start-time", "0.0", 
         "--duration", "1e3", "--width", "-1", "--height", "100", 
         "--hq-colors", "--dont-generate-lossy", "--video-framerate", "60"]

by_name_case = ["by-name", "--input-folder", assets_dir, "--output-folder", assets_dir, 
         "--input-names", "demo", "demo_odd",        
         "--output-names", "cli_test_by_name", "cli_test_odd_by_name", 
         "--dont-rename-input-file",
         "--gif-framerate", "30", "--start-time", "0.0", 
         "--duration", "1e3", "--width", "-1", "--height", "100", 
         "--hq-colors", "--dont-generate-lossy", "--video-framerate", "60"]

from_tar_case = ["latest", "--input-type", "tar", "--input-folder", assets_dir, 
         "--output-folder", assets_dir, "--output-names", "cli_test_from_tar", 
         "--dont-rename-input-file", "--gif-framerate", "30", "--start-time", "0.0", 
         "--duration", "1e3", "--width", "-1", "--height", "100", 
         "--hq-colors", "--dont-generate-lossy", "--video-framerate", "60"]

from_mp4_case = ["latest", "--input-type", "mp4", "--input-folder", assets_dir, 
         "--output-folder", assets_dir, "--output-names", "cli_test_from_mp4", 
         "--dont-rename-input-file", "--gif-framerate", "30", "--start-time", "0.0", 
         "--duration", "1e3", "--width", "-1", "--height", "100", 
         "--hq-colors", "--dont-generate-lossy", "--video-framerate", "60"]

from_gif_case = ["latest", "--input-type", "gif", "--input-folder", assets_dir, 
         "--output-folder", assets_dir, "--output-names", "cli_test_from_gif", 
         "--dont-rename-input-file", "--gif-framerate", "30", "--start-time", "0.0", 
         "--duration", "1e3", "--width", "-1", "--height", "100", 
         "--hq-colors", "--dont-generate-lossy", "--video-framerate", "60"]

test_cases = [
    (latest_case, "cli_test_latest"),
    (by_name_case, "cli_test_by_name"),
    (from_tar_case, "cli_test_from_tar"),
    (from_mp4_case, "cli_test_from_mp4"),
    (from_gif_case, "cli_test_from_gif"),
]

@pytest.mark.parametrize("test_input,expected", test_cases)
def test_parser(test_input, expected):
    # test that the input arguments are parsed correctly.
    args = parse_args(test_input)
    assert(type(args) == argparse.Namespace)

    # generate files in LATEST mode
    execute_command(args)

    # assert that the mp4 and gif files have been created
    files = glob.glob(os.path.join(assets_dir, '*'))
    assert(files)
    filenames = [os.path.basename(f) for f in files]
    if args.input_type == InputType.TAR:
        assert(expected + ".mp4" in filenames)
        assert(expected + ".gif" in filenames)
    elif args.input_type == InputType.MP4:
        assert(expected + ".gif" in filenames)
    