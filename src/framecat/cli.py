import argparse
import os
from framecat.utils import (
    get_latest_files, 
    generate_meshcat_rendering, 
    RenderingParameters,
)

class InputMode:
    LATEST = "latest"
    BY_NAME = "by-name"

def parse_args(args):
    home_directory = os.path.expanduser("~")
    default_input_folder = os.path.join(home_directory, "Downloads")
    default_output_folder = os.path.join(home_directory, "Videos", "meshcat")
    
    parser = argparse.ArgumentParser(
        description="Video and GIF processing tool for (Meshcat-generated) video frames.")
    
    parser.add_argument("input_mode", type=str, 
                        choices=[InputMode.LATEST, InputMode.BY_NAME], 
                        help="Data input mode: can be either 'latest' or 'by-name'.\
                            See README.md for more info. ")

    parser.add_argument("--input-folder", type=str, default=default_input_folder,
                        help="Input TAR files folder.")
    parser.add_argument("--output-folder", type=str, default=default_output_folder,
                        help="Output folder for generated .mp4 and .gif files.")
    parser.add_argument("--input-names", nargs="+", type=str, 
                        help="List of input file names as a list of strings e.g. 'meshcat_1234'.")
    parser.add_argument("--output-names", nargs="+", type=str, 
                        help="List of output file names as a list of strings e.g. 'name1'.")


    parser.add_argument("--dont-overwrite", action="store_true",
                        help="Prevent overwriting the .tar, .mp4 and .gif files.")
    parser.add_argument("--dont-rename-input-file", action="store_true", 
                        help="Do not rename input file according to the output file name.")
    parser.add_argument("--gif-framerate", type=int, default=30, 
                        help="Framerate (fps) of the output GIF.")
    parser.add_argument("--start-time", type=float, default=0.0, 
                        help="Start time of the GIF extracted from video.")
    parser.add_argument("--duration", type=float, default=1e3, 
                        help="Duration of the GIF extracted from video.")
    parser.add_argument("--width", type=int, default=-1, 
                        help="GIF width in pixel, -1 preserves the aspect ratio.")
    parser.add_argument("--height", type=int, default=1080, 
                        help="GIF height in pixel, -1 preserves the aspect ratio.")
    parser.add_argument("--hq-colors", action="store_true", 
                        help="Generate high quality colors for the GIF, \
                            increase the GIF size.")
    parser.add_argument("--dont-generate-lossy", action="store_true", 
                        help="Do not generate a GIF with reduced memory footprint \
                            in addition to a high quality GIF.")
    parser.add_argument("--video-framerate", type=int, default=60, 
                        help="Video framerate (fps) used to parse the TAR \
                            file frames, Meshcat uses 60 fps.")
    return parser.parse_args(args)


def execute_command(args):

    params = RenderingParameters(
        overwrite = not args.dont_overwrite,
        rename_input_file = not args.dont_rename_input_file,
        gif_framerate = args.gif_framerate,
        start_time = args.start_time,
        duration = args.duration,
        width = args.width,
        height = args.height,
        hq_colors = args.hq_colors,
        generate_lossy = not args.dont_generate_lossy,
        video_framerate = args.video_framerate,
        )
    
    if args.input_mode == InputMode.LATEST:
        if args.output_names:    
            num_files = len(args.output_names)
            tar_files = get_latest_files(args.input_folder, num_files) 

            for (i, tar_file) in enumerate(tar_files):
                generate_meshcat_rendering(
                    tar_file,
                    args.output_names[i],
                    output_folder=args.output_folder,
                    params=params,
                    )

    elif args.input_mode == InputMode.BY_NAME:
        if args.input_names and args.output_names:
            tar_files = []
            for input_name in args.input_names:
                tar_files.append(os.path.join(args.input_folder, input_name + ".tar"))
        
            num_files = min(len(args.input_names), len(args.output_names))

            for i in range(num_files):
                generate_meshcat_rendering(
                    tar_files[i],
                    args.output_names[i],
                    output_folder=args.output_folder,
                    params=params,
                    )