import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

tex_path = "/home/miri/Documents/DataLit/arXiv_src_fetcher/ICLR_2023_first100"
save_path  = "/home/miri/Documents/DataLit/math_extraction/extraced_math"
list_args = []

for folder in os.listdir(tex_path):
    list_args.append([os.path.join(save_path,folder),os.path.join(tex_path,folder)])

def parse(args):
    subprocess.run(["python","parse.py",args[0],args[1]])

with ThreadPoolExecutor(max_workers=12) as executor:
    executor.map(parse,list_args)
