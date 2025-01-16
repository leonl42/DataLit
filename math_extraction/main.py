import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from parse import parse,find_main_tex

tex_path = "/home/miri/Documents/university/DataLit/arXiv_src_fetcher/ICLR_2023_first100"
save_path  = "/home/miri/Documents/university/DataLit/math_extraction/extraced_math"
list_args = []

for folder in os.listdir(tex_path):
    list_args.append([os.path.join(tex_path,folder),os.path.join(save_path,folder)])

def _parse(e):
    (tex_path,save_path) = e
    os.makedirs(save_path,exist_ok=True)
    main_tex = find_main_tex(tex_path)
    print(tex_path)
    parse(tex_path,save_path,main_tex)

with multiprocessing.Pool(processes=2) as pool:
    pool.map(_parse,list_args)

"""
if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_save_folder", type=str)
    parser.add_argument("path_to_tex_folder", type=str)
    args = parser.parse_args()

    tex_path = args.path_to_tex_folder
    save_path = args.path_to_save_folder
    os.makedirs(save_path,exist_ok=True)
    main_tex = find_main_tex(tex_path)
    parse(tex_path,save_path,main_tex)
"""