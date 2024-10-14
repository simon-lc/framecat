import os
import glob
import logging
import tarfile
import tempfile
import subprocess
import shutil
import colorlog
from PIL import Image
from pathlib import Path

# Set up logging configuration with colorlog
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s[%(levelname)s] - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "light_yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
)

logger = colorlog.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class InputType:
    """
    Class to represent the different input file types supported.

    Attributes:
        TAR (str): Represents a TAR file type.
        MP4 (str): Represents an MP4 file type.
        GIF (str): Represents a GIF file type.
    """

    TAR = "tar"
    MP4 = "mp4"
    GIF = "gif"


def rename_file(
    file_path: str,
    new_file_name: str,
) -> str:
    """
    Renames a file to a new specified name.

    Args:
        file_path (str): Path to the file to be renamed.
        new_file_name (str): New name for the file (including extension).

    Returns:
        str: The path to the renamed file.
    """

    folder_path = os.path.dirname(file_path)
    new_file_path = os.path.join(folder_path, new_file_name)

    # Rename the file
    os.rename(file_path, new_file_path)
    logging.info(f"Renamed file from {file_path} to {new_file_path}")
    return new_file_path


def get_latest_files(
    folder_path: str,
    num_files: int = 1,
    extension: str = "tar",
) -> list:
    """
    Retrieves the latest modified files with a specified extension from a given folder.

    Args:
        folder_path (str): Path to the folder to search for files.
        num_files (int, optional): Number of most recent files to return.
                                   Defaults to 1.
        extension (str, optional): File extension to filter by.
                                   Defaults to "tar".

    Returns:
        list: A list of paths to the latest modified files with the specified extension.

    Raises:
        ValueError: If the provided folder path does not exist.
    """
    # Use glob to list all ".tar" files in the folder
    # and sort them by modification time (most recent first)
    ext_files = glob.glob(os.path.join(folder_path, f"*.{extension}"))
    ext_files.sort(key=os.path.getmtime, reverse=True)

    # Check if there are any ".tar" files in the folder
    if ext_files:
        # Print the most recent ".tar" file
        if num_files > len(ext_files):
            logging.warning(
                f"There are only {len(ext_files)} .{extension} files in {folder_path}."
            )
            num_files = len(ext_files)
        file_paths = ext_files[0:num_files]
        logging.info(f"Found {len(file_paths)} .{extension} files in {folder_path}")
        return file_paths
    else:
        logging.warning(f"No .{extension} files found in {folder_path}.")
        return []


def convert_frames_to_video(
    tar_file_path: str,
    output_path: str = "output.mp4",
    framerate: int = 60,
    overwrite: bool = False,
    conversion_args: tuple = (),
) -> str:
    """
    Converts frames extracted from a TAR file into a video.

    You can pass arguments for the video conversion, for example,
    `conversion_args=("-pix_fmt", "yuv420p")` to create videos playable in Windows.

    Args:
        tar_file_path (str): Path to the input TAR file containing frames.
        output_path (str, optional): Path to save the output video.
                                      Defaults to "output.mp4".
        framerate (int, optional): Frame rate for the output video. Defaults to 60.
        overwrite (bool, optional): Whether to overwrite the output file if it exists.
                                    Defaults to False.
        conversion_args (tuple, optional): Additional arguments for video conversion.
                                            Defaults to an empty tuple.

    Returns:
        str: The path to the saved video.

    Raises:
        FileNotFoundError: If the input TAR file does not exist.
        subprocess.CalledProcessError: If the FFMPEG command fails.
    """
    output_path = os.path.abspath(output_path)

    if not os.path.isfile(tar_file_path):
        logging.warning(f"Could not find the input file {tar_file_path}")
    if os.path.isfile(output_path) and not overwrite:
        logging.warning(f"The output path {output_path} already exists. \
            To overwrite that file, you can pass `overwrite=true` to this function")

    # Open the tar file for reading
    with tarfile.open(tar_file_path, "r") as tar:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Extract all the contents to the specified directory
        tar.extractall(path=temp_dir)
        # get the file extension
        images = glob.glob(os.path.join(temp_dir, "*"))
        if images:
            # Get the first file in the list
            first_image = images[0]
            # Extract the file extension
            image_extension = os.path.splitext(first_image)[-1]
            # Extract the image size
            width, height = Image.open(first_image).size
            # get the resizing dimensions if the original size were odd.
            # odd sizes prevent the video and GIF conversions.
            width -= width % 2
            height -= height % 2

            cmd = [
                "ffmpeg",
                "-r",
                str(framerate),
                "-i",
                "%07d" + image_extension,
                "-vf",
                "scale=" + str(width) + ":" + str(height),
                "-vcodec",
                "libx264",
                "-preset",
                "slow",
                "-crf",
                "18",
                *conversion_args,
            ]
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
                logging.error("Error:", e)

    # Remove the directory and its contents
    shutil.rmtree(temp_dir)

    logging.info(f"Saved output as {output_path}")
    return output_path


def convert_video_to_gif(
    video_file_path: str,
    output_path: str = "output.gif",
    framerate: int = 30,
    start_time: float = 0.0,
    duration: float = 1e3,
    overwrite: bool = False,
    width: int = -1,
    height: int = -1,
    hq_colors: bool = False,
) -> str:
    """
    Converts a video file to a GIF.

    Args:
        video_file_path (str): Path to the input video file.
        output_path (str, optional): Path to save the output GIF.
                                      Defaults to "output.gif".
        framerate (int, optional): Frame rate for the GIF. Defaults to 30.
        start_time (float, optional): Start time for the conversion in seconds. Defaults to 0.0.
        duration (float, optional): Duration of the output GIF in seconds. Defaults to 1000.0.
        overwrite (bool, optional): Whether to overwrite the output file if it exists.
                                    Defaults to False.
        width (int, optional): Width of the output GIF. Defaults to -1 (no resizing).
        height (int, optional): Height of the output GIF. Defaults to -1 (no resizing).
        hq_colors (bool, optional): Whether to use high-quality colors for the GIF. Defaults to False.

    Returns:
        str: The path to the saved GIF.

    Raises:
        FileNotFoundError: If the input video file does not exist.
        subprocess.CalledProcessError: If the FFMPEG command fails.
    """
    output_path = os.path.abspath(output_path)

    if not os.path.isfile(video_file_path):
        logging.warning("Could not find the input file $video_file_path")
    if os.path.isfile(output_path) and not overwrite:
        logging.warning(
            "The output path $output_path already exists. \
              To overwrite that file, you can pass `overwrite=true` to this function"
        )

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    if overwrite:
        if hq_colors:
            color_map = f'"[0:v] fps={framerate}, scale={width}:{height}, \
                split [a][b];[a] palettegen=stats_mode=single [p];[b][p] paletteuse=new=1"'
        else:
            color_map = f'"[0:v] fps={framerate}, scale={width}:{height}, \
                split [a][b];[a] palettegen [p];[b][p] paletteuse"'
        cmd = [
            "ffmpeg",
            "-ss",
            str(start_time),
            "-t",
            str(duration),
            "-i",
            video_file_path,
            "-filter_complex",
            color_map,
        ]
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
            logging.error("Error:", e)

    # Remove the directory and its contents
    shutil.rmtree(temp_dir)

    logging.info(f"Saved GIF as {output_path}")
    return output_path


def compress_gif(
    file_path: str,
    output_path: str | None = None,
    overwrite: bool = False,
) -> str:
    """
    Compresses a GIF file to reduce its size with lossy optimization.

    Args:
        file_path (str): Path to the input GIF file.
        output_path (str, optional): Path to save the compressed GIF.
                                      If None, defaults to `<input_file>_lossy.gif`.
        overwrite (bool, optional): Whether to overwrite the output file if it exists.
                                    Defaults to False.

    Returns:
        str: The path to the saved compressed GIF.

    Raises:
        FileNotFoundError: If the input file does not exist.
    """
    if not os.path.isfile(file_path):
        logging.warning("Could not find the input file $file_path")

    if output_path is None:
        output_path = file_path[:-4] + "_lossy.gif"
    output_path = os.path.abspath(output_path)

    if os.path.isfile(output_path) and not overwrite:
        logging.warning(
            "The output path $output_path already exists. \
              To overwrite that file, you can pass `overwrite=true` to this function"
        )

    if overwrite:
        gifsicle_command = (
            f"gifsicle -O3 -k128 --lossy=100 --verbose {file_path} -o {output_path}"
        )
        # Execute the gifsicle command using subprocess
        try:
            logging.info("Executing the gifsicle command.")
            subprocess.run(gifsicle_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logging.error("Error:", e)

    logging.info(f"Saved lossy GIF as {output_path}")
    return output_path


class RenderingParameters:
    """
    Class to hold parameters for rendering operations.

    Attributes:
        overwrite (bool): Whether to overwrite existing files. Defaults to True.
        rename_input_file (bool): Whether to rename the input file. Defaults to True.
        gif_framerate (int): Frame rate for the GIF output. Defaults to 30.
        start_time (float): Start time for video conversion in seconds. Defaults to 0.0.
        duration (float): Duration for video conversion in milliseconds. Defaults to 1000.0.
        width (int): Width of the output GIF. Defaults to -1 (no resizing).
        height (int): Height of the output GIF. Defaults to -1 (no resizing).
        hq_colors (bool): Whether to use high-quality colors for GIF. Defaults to False.
        generate_lossy (bool): Whether to generate a lossy GIF. Defaults to False.
        video_framerate (int): Frame rate for the video output. Defaults to 60.
        video_conversion_args (tuple): Additional arguments for video conversion. Defaults to an empty tuple.
    """

    def __init__(
        self,
        overwrite: bool = True,
        rename_input_file: bool = True,
        gif_framerate: int = 30,
        start_time: float = 0.0,
        duration: float = 1e3,
        width: int = -1,
        height: int = -1,
        hq_colors: bool = False,
        generate_lossy: bool = False,
        video_framerate: int = 60,
        video_conversion_args: tuple = (),
    ) -> None:
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


def get_input_type(file_path: str) -> InputType:
    """
    Determines the input type based on the file extension.

    Args:
        file_path (str): Path to the input file.

    Returns:
        InputType: The identified input type (TAR, MP4, or GIF).

    Raises:
        ValueError: If the file extension is not recognized.
    """
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
    output_folder: str | None = None,
    params: RenderingParameters = RenderingParameters(),
) -> None:
    """
    Renders a video or GIF from the specified file.

    Args:
        file_path (str): Path to the input file (TAR or MP4).
        output_name (str): Name for the output files (without extension).
        output_folder (str, optional): Directory for saving output files.
                                       Defaults to ~/Videos/framecat.
        params (RenderingParameters, optional): Parameters for rendering options.

    Returns:
        None: This function does not return a value.
    """
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
            output_path=video_output_file_path,
            framerate=params.video_framerate,
            overwrite=params.overwrite,
            conversion_args=params.video_conversion_args,
        )
        video_input_file_path = video_output_file_path

    # Video to GIF
    if input_type in [InputType.TAR, InputType.MP4]:
        if input_type == InputType.MP4:
            video_input_file_path = file_path
        gif_output_file_path = os.path.join(output_folder, output_name + ".gif")

        convert_video_to_gif(
            video_input_file_path,
            output_path=gif_output_file_path,
            framerate=params.gif_framerate,
            start_time=params.start_time,
            duration=params.duration,
            overwrite=params.overwrite,
            width=params.width,
            height=params.height,
            hq_colors=params.hq_colors,
        )

        gif_input_file_path = gif_output_file_path

    # GIF to small memory footprint GIF
    if params.generate_lossy:
        if input_type == InputType.GIF:
            gif_input_file_path = file_path
        compress_gif(
            gif_input_file_path,
            output_path=None,
            overwrite=params.overwrite,
        )
