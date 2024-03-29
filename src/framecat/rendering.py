import os
import glob
import tarfile
import tempfile
import subprocess
import shutil
from PIL import Image
from pathlib import Path
from typing import Optional

class InputType:
    TAR = "tar"
    MP4 = "mp4"
    GIF = "gif"


def rename_file(
    file_path: str, 
    new_file_name: str, 
    ):

    folder_path = os.path.dirname(file_path)
    new_file_path = os.path.join(folder_path, new_file_name)

    # Rename the file
    os.rename(file_path, new_file_path)
    return new_file_path


def get_latest_files(
    folder_path: str, 
    num_files: int = 1, 
    extension: str = "tar",
    ):

    # Use glob to list all ".tar" files in the folder 
    # and sort them by modification time (most recent first)
    ext_files = glob.glob(os.path.join(folder_path, f"*.{extension}"))
    ext_files.sort(key=os.path.getmtime, reverse=True)

    # Check if there are any ".tar" files in the folder
    if ext_files:
        # Print the most recent ".tar" file
        if num_files > len(ext_files):
            print(f"There are only {len(ext_files)} .{extension} files in {folder_path}.")
            num_files = len(ext_files)
        file_paths = ext_files[0:num_files]
        return file_paths
    else:
        print(f"No .{extension} files found in {folder_path}.")


def convert_frames_to_video(
    tar_file_path: str, 
    output_path: str = "output.mp4", 
    framerate: int = 60, 
    overwrite: bool = False, 
    conversion_args = ()):

    """You can pass arguments for the video conversion, for 
    example, `conversion_args=("-pix_fmt", "yuv420p")` to create videos playable in 
    Windows.
    """

    output_path = os.path.abspath(output_path)

    if not os.path.isfile(tar_file_path):
        print(f"Could not find the input file {tar_file_path}")
    if os.path.isfile(output_path) and not overwrite:
        print(f"The output path {output_path} already exists. \
            To overwrite that file, you can pass `overwrite=true` to this function")

    # Open the tar file for reading
    with tarfile.open(tar_file_path, "r") as tar:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Extract all the contents to the specified directory
        tar.extractall(path=temp_dir)
        # get the file extension
        images = glob.glob(os.path.join(temp_dir, '*'))
        if images:
            # Get the first file in the list
            first_image = images[0]
            # Extract the file extension
            image_extension = os.path.splitext(first_image)[-1]
            # Extract the image size
            width, height = Image.open(first_image).size
            # get the resizing dimensions if the original size were odd.
            # odd sizes prevent the video and GIF conversions. 
            width -= width%2 
            height -= height%2 

            cmd = ["ffmpeg", "-r", str(framerate), "-i", "%07d" + image_extension, 
                "-vf", "scale=" + str(width) + ":" + str(height), "-vcodec", "libx264", 
                "-preset", "slow", "-crf", "18", *conversion_args]
            if overwrite:
                cmd.append("-y")
            cmd.append(output_path)

            # Change the working directory to the specified folder
            os.chdir(temp_dir)

            # Specify the FFMPEG command you want to execute
            ffmpeg_command = " ".join(cmd)

            # Execute the FFMPEG command using subprocess
            try:
                subprocess.run(ffmpeg_command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print("Error:", e)

    # Remove the directory and its contents
    shutil.rmtree(temp_dir)

    print(f"Saved output as {output_path}")
    return output_path


def convert_video_to_gif(
    video_file_path: str, 
    output_path: str = "output.gif",
    framerate: int = 30, 
    start_time: float = 0.0, 
    duration: float = 1e3, 
    overwrite: bool = False, 
    width: int = -1, 
    height: int = 1080, 
    hq_colors: bool = False,
    ):
    
    output_path = os.path.abspath(output_path)

    if not os.path.isfile(video_file_path):
        print("Could not find the input file $video_file_path")
    if os.path.isfile(output_path) and not overwrite:
        print("The output path $output_path already exists. \
              To overwrite that file, you can pass `overwrite=true` to this function")

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    if overwrite:
        if hq_colors:
            color_map = f"\"[0:v] fps={framerate}, scale={width}:{height}, \
                split [a][b];[a] palettegen=stats_mode=single [p];[b][p] paletteuse=new=1\""
        else:
            color_map = f"\"[0:v] fps={framerate}, scale={width}:{height}, \
                split [a][b];[a] palettegen [p];[b][p] paletteuse\""
        cmd = ["ffmpeg", "-ss", str(start_time), "-t", str(duration), "-i", 
                video_file_path, "-filter_complex", color_map]
        if overwrite:
            cmd.append("-y")
        cmd.append(output_path)

        # Change the working directory to the specified folder
        os.chdir(temp_dir)

        # Specify the FFMPEG command you want to execute
        ffmpeg_command = " ".join(cmd)

        # Execute the FFMPEG command using subprocess
        try:
            subprocess.run(ffmpeg_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print("Error:", e)

    # Remove the directory and its contents
    shutil.rmtree(temp_dir)

    print(f"Saved GIF as {output_path}")
    return output_path


def compress_gif(
    file_path: str, 
    output_path: Optional[str] = None,
    overwrite: bool = False, 
    ):
    
    if not os.path.isfile(file_path):
        print("Could not find the input file $file_path")
    
    if output_path is None:
        output_path = file_path[:-4] + "_lossy.gif"
    output_path = os.path.abspath(output_path)

    if os.path.isfile(output_path) and not overwrite:
        print("The output path $output_path already exists. \
              To overwrite that file, you can pass `overwrite=true` to this function")

    if overwrite:
        gifsicle_command = f"gifsicle -O3 -k128 --lossy=100 --verbose {file_path} -o {output_path}"
        # Execute the gifsicle command using subprocess
        try:
            print("Executing the gifsicle command.")
            subprocess.run(gifsicle_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print("Error:", e)

    print(f"Saved lossy GIF as {output_path}")
    return output_path


class RenderingParameters:
    def __init__(
        self,
        overwrite: bool = True,
        rename_input_file: bool = True,
        gif_framerate: int = 30, 
        start_time: float = 0.0, 
        duration: float = 1e3, 
        width: int = -1, 
        height: int = 1080, 
        hq_colors: bool = False,
        generate_lossy: bool = False,
        video_framerate: int = 60, 
        video_conversion_args = (),
    ):
        self.overwrite = overwrite
        self.rename_input_file = rename_input_file
        self.gif_framerate = gif_framerate
        self.start_time = start_time
        self.duration = duration
        self.width = width
        self.height = height
        self.hq_colors = hq_colors
        self.generate_lossy = generate_lossy
        self.video_framerate = video_framerate
        self.video_conversion_args = video_conversion_args


def get_input_type(file_path: str):
    path = Path(file_path)
    extension = path.suffix.lower()[1:]
    for input_type in [InputType.TAR, InputType.MP4, InputType.GIF]:
        if input_type.lower() == extension:
            return input_type
    # If no matching input type is found, we raise a specific exception.
    raise ValueError(f"Unknown extension: {extension}")


def render_file(
    file_path: str, 
    output_name: str,
    output_folder: str = None,
    params: RenderingParameters = RenderingParameters(),
    ):
        
    if output_folder is None:
        # Get the user's home directory
        home_directory = os.path.expanduser("~")
        output_folder = os.path.join(home_directory, "Videos", "framecat")

    # Check if output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_type = get_input_type(file_path)

    # Frames to video
    if input_type == InputType.TAR:
        tar_file_path = file_path
        video_output_file_path = os.path.join(output_folder, output_name + ".mp4")

        if params.rename_input_file:
            tar_file_path = rename_file(
                tar_file_path, 
                output_name + ".tar", 
                )

        convert_frames_to_video(
            tar_file_path, 
            output_path = video_output_file_path, 
            framerate = params.video_framerate, 
            overwrite = params.overwrite, 
            conversion_args = params.video_conversion_args,
            )
        video_input_file_path = video_output_file_path
    
    # Video to GIF
    if input_type in [InputType.TAR, InputType.MP4]:
        if input_type == InputType.MP4:
            video_input_file_path = file_path
        gif_output_file_path = os.path.join(output_folder, output_name + ".gif")
        
        convert_video_to_gif(
            video_input_file_path, 
            output_path = gif_output_file_path,
            framerate = params.gif_framerate, 
            start_time = params.start_time, 
            duration = params.duration, 
            overwrite = params.overwrite, 
            width = params.width, 
            height = params.height, 
            hq_colors = params.hq_colors,
            )
    
        gif_input_file_path = gif_output_file_path

    # GIF to small memory footprint GIF
    if params.generate_lossy:
        if input_type == InputType.GIF:
            gif_input_file_path = file_path
        compress_gif(
            gif_input_file_path, 
            output_path = None,
            overwrite = params.overwrite, 
            )