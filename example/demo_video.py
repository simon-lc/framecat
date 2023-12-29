#%%
import os
from framecat.rendering import convert_video_to_gif

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
gif_file_path = os.path.join(assets_dir, output_name + ".gif")

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
    )
    
#%%
