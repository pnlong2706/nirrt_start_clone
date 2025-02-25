import time
import pickle
import argparse
from copy import copy
from os import makedirs
from os.path import join, exists
from importlib import import_module

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path_planner', default='rrt_star', 
        help='rrt_star, irrt_star, nrrt_star, nirrt_star')
    parser.add_argument('-n', '--neural_net', default='none', help='none, pointnet2, unet, pointnet')
    parser.add_argument('-c', '--connect', default='none', help='none, bfs')
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
    parser.add_argument('--path_len_threshold_percentage', type=float, default=0.02, help='block use only.')
    parser.add_argument('--iter_after_initial', type=int, default=5000, help='random_2d use only.')
    parser.add_argument('--num_problems', type=int, help='number of problems to evaluate. None means evaluate all.')
    
    parser.add_argument('--output_path', default='results/evaluation/2d', help='path')
    parser.add_argument('--data_path', default='.', help='path')
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
env_config_list = get_env_configs(args.data_path)
if args.num_problems is None:
    num_problems = len(env_config_list)
else:
    assert args.num_problems <= len(env_config_list)
    num_problems = args.num_problems

result_folderpath = args.output_path
makedirs(result_folderpath, exist_ok=True)

if args.connect != 'none':
    connect_str = '-c-'+args.connect
else:
    connect_str = ''
eval_setting = args.problem+'-'+args.path_planner+connect_str+'-'+args.neural_net+'-'+str(num_problems)
result_filepath = join(result_folderpath, eval_setting+'.pickle')
if not exists(result_filepath):
    env_result_config_list = []
else:
    with open(result_filepath, 'rb') as f:
        env_result_config_list = pickle.load(f)

eval_start_time = time.time()
for env_idx, env_config in enumerate(env_config_list[:num_problems]):
    if env_idx < len(env_result_config_list):
        time_left = (time.time() - eval_start_time) * (num_problems / (env_idx + 1) - 1) / 60
        print("Evaluated {0}/{1} in the loaded file, remaining time: {2} min for {3}".format(env_idx + 1, num_problems, int(time_left), eval_setting))
        continue
    problem = get_problem_input(env_config)
    path_planner = get_path_planner(
        args,
        problem,
        neural_wrapper,
    )
    if args.problem == 'block':
        path_len_threshold = problem['best_path_len']*(1+args.path_len_threshold_percentage)
        path_len_list = path_planner.planning_block_gap(path_len_threshold)
    elif args.problem == 'gap':
        path_len_list = path_planner.planning_block_gap(problem['flank_path_len'])
    elif args.problem == 'random_2d':
        path_len_list = path_planner.planning_random(
            args.iter_after_initial,
        )
    else:
        raise NotImplementedError

    env_result_config = copy(env_config)
    env_result_config['result'] = path_len_list
    env_result_config_list.append(env_result_config)

    with open(result_filepath, 'wb') as f:
        pickle.dump(env_result_config_list, f)
    time_left = (time.time() - eval_start_time) * (num_problems - env_idx - 1) / (env_idx + 1) / 60
    print("Evaluated {0}/{1}, remaining time: {2} min for {3}".format(env_idx + 1, num_problems, int(time_left), eval_setting))