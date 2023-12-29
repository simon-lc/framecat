#%%
import os
from framecat.rendering import (
    get_latest_files, 
    convert_frames_to_video, 
    render_file, 
    convert_video_to_gif,
    RenderingParameters,
)

#%%
# directories
test_dir = os.path.dirname(os.path.abspath(__file__))
package_dir = os.path.dirname(test_dir)
assets_dir = os.path.join(package_dir, "assets")

# files
tar_file_path = get_latest_files(assets_dir)[0]
output_name = "output"
video_file_path = os.path.join(assets_dir, output_name + ".mp4")
gif_file_path = os.path.join(assets_dir, output_name + ".gif")


#%%
convert_frames_to_video(
    tar_file_path, 
    output_path = video_file_path, 
    framerate = 60, 
    overwrite = True, 
    conversion_args = (),
    )

#%%
convert_video_to_gif(
    video_file_path, 
    gif_file_path,
    framerate = 30, 
    start_time = 0.0, 
    duration = 1e3, 
    overwrite = True, 
    width = -1, 
    height = 100, 
    hq_colors = True,
    )
    
#%%
params = RenderingParameters(
    height=100, 
    generate_lossy=False,
    rename_input_file=False,
    )
    
render_file(
    tar_file_path, 
    output_name,
    assets_dir,
    params = params,
    )
# %%
