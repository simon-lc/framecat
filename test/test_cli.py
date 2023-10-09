import os
import glob
import pytest
import argparse
from unittest import mock
from framecat.cli import (
    execute_command,
    parse_args,
)


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
         "--input-names", "demo",        
         "--output-names", "cli_test_by_name", "--dont-rename-input-file",
         "--gif-framerate", "30", "--start-time", "0.0", 
         "--duration", "1e3", "--width", "-1", "--height", "100", 
         "--hq-colors", "--dont-generate-lossy", "--video-framerate", "60"]

test_cases = [
    (latest_case, "cli_test_latest"),
    (by_name_case, "cli_test_by_name"),
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
    assert(expected + ".mp4" in filenames)
    assert(expected + ".gif" in filenames)



# @mock.patch('argparse.ArgumentParser.parse_args',
#             return_value=parse_args(latest_case))
# def test_main_latest(mock_args):
#     # generate files in LATEST mode
#     execute_command(args)

#     # assert that the mp4 and gif files have been created
#     files = glob.glob(os.path.join(assets_dir, '*'))
#     assert(files)
#     filenames = [os.path.basename(f) for f in files]
#     assert("render_test_latest" + ".mp4" in filenames)
#     assert("render_test_latest" + ".gif" in filenames)


# @mock.patch('argparse.ArgumentParser.parse_args',
#             return_value=parse_args(by_name_case))
# def test_main_by_name(mock_args):
#     # generate files in BY-NAME mode
#     execute_command(args)
#     # assert that the mp4 and gif files have been created
#     files = glob.glob(os.path.join(assets_dir, '*'))
#     assert(files)
#     filenames = [os.path.basename(f) for f in files]
#     assert("render_test_by_name" + ".mp4" in filenames)
#     assert("render_test_by_name" + ".gif" in filenames)

