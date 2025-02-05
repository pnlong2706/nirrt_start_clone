#  Source
https://github.com/tedhuang96/nirrt_star

# Add
-  ```a_star_path_cost.py```: return cost from astar txt file.
-  ```eval_sample.py```: trash (for plotting, comparing between IRRT* & NIRRT* from output txt file from demo_planning.py).
-  ```generate_self_defined_map.py```: this file is a clone of ```generate_random_world_env_2d.py```, but instead of random, I manually add obstacles.
-  ```run.bat```: for running ```demo_planning.py```.

# Modify
-  ```datasets/planning_problem_utils_2d.py```: add ```mode``` parameter to ```get_random_2d_env_configs```, ```get_random_2d_problem_input```, enable getting config from train or test folder.
-  ```demo_planning_2d.py```: add more statistics and save to txt files.
-  ```env_configs/random_2d.yml```: increase ```num_rectangles_range``` and ```num_circles_range```.
-  ```path_planning_classes/irrt_star_2d.py```, ```path_planning_classes/nirrt_star_png_2d.py```: modify ```planning``` method, now it will print the number of iter for the initial solution and final path cost. Modify ```generate_random_node``` (important) - in case the path is zigzag and the path cost is large, ```c_max < np.inf``` will perform poorly. Also, change some bugs in the name for the figure or output image, the origin uses `*` in their name.
-  ```visualize_data_samples_2d.py```: add ```mode``` variable, enable visualizing from both train or test folder.
-  ```wrapper/pointnet_pointnet2/pointnet2_wrapper_connect_bfs.py```: change `device` to `cpu` since I don't have GPU. The commented line is for manually adding more guidance points in the Neural connect step.

# Note
-  This repo is a bit messy, mostly for testing, so cloning from the origin repo is another option.
