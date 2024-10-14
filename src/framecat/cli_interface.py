# %%

import argparse
import os
from framecat.rendering import (
    get_latest_files,
    render_file,
    InputType,
    RenderingParameters,
)


class InputMode:
    """
    Class to represent the different modes for input selection.

    Attributes:
        LATEST (str): Represents the mode to select the latest input.
        BY_NAME (str): Represents the mode to select input by name.
    """

    LATEST = "latest"
    BY_NAME = "by-name"


def parse_args(args):
    """
    Parses command-line arguments for video and GIF generation.

    This function sets up the argument parser with various options for input modes,
    input types, file paths, and parameters for GIF and video generation.

    Args:
        args (list): A list of command-line arguments to parse.

    Returns:
        Namespace: A Namespace object containing the parsed arguments.
    """
    home_directory = os.path.expanduser("~")
    default_input_folder = os.path.join(home_directory, "Downloads")
    default_output_folder = os.path.join(home_directory, "Videos", "framecat")

    parser = argparse.ArgumentParser(
        description="Generate videos and GIF and low-memory footprint GIF from frame sequences, video and GIF sources."
    )

    parser.add_argument(
        "input_mode",
        type=str,
        choices=[InputMode.LATEST, InputMode.BY_NAME],
        help="Data input mode: can be either 'latest' or 'by-name'.\
                            See README.md for more info. ",
    )

    parser.add_argument(
        "--input-type",
        type=str,
        default=InputType.TAR,
        choices=[InputType.TAR, InputType.MP4, InputType.GIF],
        help="Data input type: can be either 'tar', 'mp4' or 'gif'.\
                            See README.md for more info. ",
    )

    parser.add_argument(
        "--input-folder",
        type=str,
        default=default_input_folder,
        help="Input TAR files folder.",
    )
    parser.add_argument(
        "--output-folder",
        type=str,
        default=default_output_folder,
        help="Output folder for generated .mp4 and .gif files.",
    )
    parser.add_argument(
        "--input-names",
        nargs="+",
        type=str,
        help="List of input file names as a list of strings e.g. 'frames_1234'.",
    )
    parser.add_argument(
        "--output-names",
        nargs="+",
        type=str,
        help="List of output file names as a list of strings e.g. 'name1'.",
    )

    parser.add_argument(
        "--dont-overwrite",
        action="store_true",
        help="Prevent overwriting the .tar, .mp4 and .gif files.",
    )
    parser.add_argument(
        "--dont-rename-input-file",
        action="store_true",
        help="Do not rename input file according to the output file name.",
    )
    parser.add_argument(
        "--gif-framerate",
        type=int,
        default=30,
        help="Framerate (fps) of the output GIF.",
    )
    parser.add_argument(
        "--start-time",
        type=float,
        default=0.0,
        help="Start time of the GIF extracted from video.",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=1e3,
        help="Duration of the GIF extracted from video.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=-1,
        help="GIF width in pixel, -1 preserves the aspect ratio.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=-1,
        help="GIF height in pixel, -1 preserves the aspect ratio.",
    )
    parser.add_argument(
        "--hq-colors",
        action="store_true",
        help="Generate high quality colors for the GIF, \
                            increase the GIF size.",
    )
    parser.add_argument(
        "--dont-generate-lossy",
        action="store_true",
        help="Do not generate a GIF with reduced memory footprint \
                            in addition to a high quality GIF.",
    )
    parser.add_argument(
        "--video-framerate",
        type=int,
        default=60,
        help="Video framerate (fps) used to parse the TAR \
                            file frames, e.g. Meshcat uses 60 fps.",
    )
    return parser.parse_args(args)


def execute_command(args):
    """
    Executes the rendering process based on the parsed command-line arguments.

    This function configures the rendering parameters and determines the input files
    to process based on the specified input mode (latest or by name). It then calls
    the `render_file` function for each input file.

    Args:
        args (Namespace): A Namespace object containing the parsed command-line arguments.
    """
    params = RenderingParameters(
        overwrite=not args.dont_overwrite,
        rename_input_file=not args.dont_rename_input_file,
        gif_framerate=args.gif_framerate,
        start_time=args.start_time,
        duration=args.duration,
        width=args.width,
        height=args.height,
        hq_colors=args.hq_colors,
        generate_lossy=not args.dont_generate_lossy,
        video_framerate=args.video_framerate,
    )

    extension = args.input_type.lower()

    if args.input_mode == InputMode.LATEST:
        if args.output_names:
            num_files = len(args.output_names)
            files = get_latest_files(args.input_folder, num_files, extension=extension)

    elif args.input_mode == InputMode.BY_NAME:
        if args.input_names is None:
            args.input_names = []
        ni = len(args.input_names)
        if args.output_names is None:
            args.output_names = []
        no = len(args.output_names)
        assert ni >= no
        if args.input_names:
            files = []
            for i, input_name in enumerate(args.input_names):
                files.append(
                    os.path.join(args.input_folder, input_name + "." + extension)
                )
                if i >= no:
                    args.output_names.append(input_name)

    num_files = len(files)
    for i in range(num_files):
        render_file(
            files[i],
            args.output_names[i],
            output_folder=args.output_folder,
            params=params,
        )
