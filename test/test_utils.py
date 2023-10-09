import os
import glob
from framecat.utils import (
    generate_meshcat_rendering, 
    get_latest_files,
    RenderingParameters, 
)


def test_rendering_tool() -> None:    
    
    # directories
    test_dir = os.path.dirname(os.path.abspath(__file__))
    package_dir = os.path.dirname(test_dir)
    assets_dir = os.path.join(package_dir, "assets")
    
    # files
    tar_file_path = os.path.join(assets_dir, "demo.tar")
    output_name = "rendering_output"

    # rendering parameters
    params = RenderingParameters(
        height=100, 
        generate_lossy=False,
        rename_input_file=False,
        )

    # generate video and gif from frames
    generate_meshcat_rendering(
        tar_file_path, 
        output_name,
        output_folder = assets_dir,
        params = params,
        )

    # assert that the mp4 and gif files have been created
    files = glob.glob(os.path.join(assets_dir, '*'))
    assert(files)
    filenames = [os.path.basename(f) for f in files]
    assert(output_name + ".mp4" in filenames)
    assert(output_name + ".gif" in filenames)

    # assert file size of video is lower than the frame sequence
    video_path = os.path.join(assets_dir, output_name + ".mp4")
    tar_size = os.path.getsize(tar_file_path)
    video_size = os.path.getsize(video_path)
    assert(video_size <= tar_size)

    # assert that last created gif file is the gif we just wrote
    gif_path = os.path.join(assets_dir, output_name + ".gif")
    latest_path = get_latest_files(assets_dir, num_files=1, extension="gif")[0]
    assert(os.path.abspath(latest_path) == os.path.abspath(gif_path))


