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
video_file_path = os.path.join(assets_dir, "graph_expansion.mp4")
print(video_file_path)

#%%
output_name = "output"
# video_file_path = os.path.join(assets_dir, output_name + ".mp4")
gif_file_path = os.path.join(assets_dir, output_name + ".gif")


#%%
# convert_frames_to_video(
#     tar_file_path, 
#     output_path = video_file_path, 
#     framerate = 60, 
#     overwrite = True, 
#     conversion_args = (),
#     )

#%%
convert_video_to_gif(
    video_file_path, 
    gif_file_path,
    framerate = 30, 
    start_time = 3.15, 
    duration = 10, 
    overwrite = True, 
    width = -1, 
    height = 600, 
    hq_colors = False,
    # generate_lossy = True,
    )
    
#%%
