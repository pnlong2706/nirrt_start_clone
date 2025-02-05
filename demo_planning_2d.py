import argparse
from importlib import import_module
from a_start_path_cost import a_star_cost

import numpy as np


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path_planner', default='rrt_star', 
        help='rrt_star, irrt_star, nrrt_star, nirrt_star')
    parser.add_argument('-n', '--neural_net', default='none', help='none, pointnet2, unet, pointnet')
    parser.add_argument('-c', '--connect', default='none', help='none, bfs, astar')
    parser.add_argument('--device', default='cuda', help='cuda, cpu')

    parser.add_argument('--step_len', type=float, default=10)
    parser.add_argument('--iter_max', type=int, default=50000)
    parser.add_argument('--clearance', type=float, default=0, help='0 for block and gap, 3 for random_2d.')
    parser.add_argument('--pc_n_points', type=int, default=2048)
    parser.add_argument('--pc_over_sample_scale', type=int, default=5)
    parser.add_argument('--pc_sample_rate', type=float, default=0.5)
    parser.add_argument('--pc_update_cost_ratio', type=float, default=0.9)
    parser.add_argument('--connect_max_trial_attempts', type=int, default=5)

    parser.add_argument('--problem', default='random_2d', help='block, gap, random_2d')
    parser.add_argument('--result_folderpath', default='results')
    parser.add_argument('--path_len_threshold_percentage', type=float, default=0.02, help='block use only.')
    parser.add_argument('--iter_after_initial', type=int, default=1000, help='random_2d use only.')
  
    return parser.parse_args()



args = arg_parse()
# * sanity check
if args.path_planner == 'rrt_star' or args.path_planner == 'irrt_star':
    assert args.neural_net == 'none'
else:
    assert args.neural_net != 'none'
#  * set get_path_planner
if args.neural_net == 'none':
    path_planner_name = args.path_planner
elif args.neural_net == 'pointnet2' or args.neural_net == 'pointnet':
    path_planner_name = args.path_planner+'_png'
elif args.neural_net == 'unet':
    path_planner_name = args.path_planner+'_gng'
else:
    raise NotImplementedError
if args.connect != 'none':
    path_planner_name = path_planner_name+'_c'
path_planner_name = path_planner_name+'_2d'
get_path_planner = getattr(import_module('path_planning_classes.'+path_planner_name), 'get_path_planner')
#  * set NeuralWrapper
if args.neural_net == 'none':
    NeuralWrapper = None
elif args.neural_net == 'pointnet2' or args.neural_net == 'pointnet':
    neural_wrapper_name = args.neural_net+'_wrapper'
    if args.connect != 'none':
        neural_wrapper_name = neural_wrapper_name+'_connect_'+args.connect
    NeuralWrapper = getattr(import_module('wrapper.pointnet_pointnet2.'+neural_wrapper_name), 'PNGWrapper')
elif args.neural_net == 'unet':
    neural_wrapper_name = args.neural_net+'_wrapper'
    if args.connect != 'none':
        raise NotImplementedError
    NeuralWrapper = getattr(import_module('wrapper.unet.'+neural_wrapper_name), 'GNGWrapper')
else:
    raise NotImplementedError
#  * set planning problem
get_env_configs = getattr(import_module('datasets.planning_problem_utils_2d'), 'get_'+args.problem+'_env_configs')
get_problem_input = getattr(import_module('datasets.planning_problem_utils_2d'), 'get_'+args.problem+'_problem_input')

# * main
if NeuralWrapper is None:
    neural_wrapper = None
else:
    neural_wrapper = NeuralWrapper(
        device=args.device,
    )
if args.problem == 'random_2d':
    args.clearance = 3
print(args)
env_config_list = get_env_configs(mode = "train")


import time

first_iter_list = []
c_best_list = []
time_list = []
astar_cost_list = []
no_sol_cnt = 0

first_iter_avg = 0
c_best_avg = 0

num = 0

print("Total sample:", len(env_config_list))
print(path_planner_name)

env_config_index = 19*4 + 0
id_env = env_config_index // 4
id_env_cfg = env_config_index % 4

astar_cost = a_star_cost("data/random_2d/train/astar_paths/"+ str(id_env) + "_" + str(id_env_cfg) +".txt")

print("\n***** Env_config_index: ", env_config_index)
print("Astar cost:", astar_cost)

problem = get_problem_input(env_config_list[env_config_index], mode = "train")
path_planner = get_path_planner(
    args,
    problem,
    neural_wrapper,
)

second = time.time()
first_iter, c_best = path_planner.planning(visualize=True) # * we can only run planning once, or we need reset.
total_time = time.time() - second
print("Total time:", total_time)

# for env_config_index in range(len(env_config_list)):
    
#     id_env = env_config_index // 4
#     id_env_cfg = env_config_index % 4
    
#     astar_cost = a_star_cost("data/random_2d/train/astar_paths/"+ str(id_env) + "_" + str(id_env_cfg) +".txt")
#     astar_cost_list.append(astar_cost)
    
#     print("\n***** Env_config_index: ", env_config_index)
#     print("Astar cost:", astar_cost)
    
#     problem = get_problem_input(env_config_list[env_config_index], mode = "train")
#     path_planner = get_path_planner(
#         args,
#         problem,
#         neural_wrapper,
#     )

#     second = time.time()
#     first_iter, c_best = path_planner.planning(visualize=False) # * we can only run planning once, or we need reset.
#     total_time = time.time() - second
    
#     if(first_iter < 50000):
#         # print("First path:", first_iter)
#         # print("Path cost: ", c_best)
        
#         first_iter_list.append(first_iter)
#         c_best_list.append(c_best)
        
#         first_iter_avg += first_iter
#         c_best_avg += c_best
#     else:
#         # print("No solution!")    
#         first_iter_list.append(-1)
#         c_best_list.append(-1)
        
#         no_sol_cnt += 1
    
#     print("Total time:", total_time)
#     time_list.append(total_time)
#     num += 1
    
#     # if(env_config_index > 0):
#     #     break

# first_iter_avg = first_iter_avg / (num - no_sol_cnt)
# c_best_avg = c_best_avg / (num - no_sol_cnt)

# print("\n\n*********** FINISH ***********")
# print("No solution count:", no_sol_cnt)
# print("Avg first iter:", first_iter_avg)
# print("Avg time:", np.average(np.array(time_list)))
# print("Avg cost:", c_best_avg)

# with open('stat/first_iter_list_'+ path_planner_name + '.txt', 'w') as f:
#     for line in first_iter_list:
#         f.write(f"{line}\n")
        
# with open('stat/c_best_list_'+ path_planner_name + '.txt', 'w') as f:
#     for line in c_best_list:
#         f.write(f"{line}\n")
        
# with open('stat/time_list_'+ path_planner_name + '.txt', 'w') as f:
#     for line in time_list:
#         f.write(f"{line}\n")
        
# with open('stat/astar_cost_list_'+ path_planner_name + '.txt', 'w') as f:
#     for line in astar_cost_list:
#         f.write(f"{line}\n")

