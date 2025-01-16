import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from parse import parse,find_main_tex

TEX_PATH = "/home/miri/Documents/university/DataLit/arXiv_src_fetcher/ICLR_2023_first100"
SAVE_PATH  = "/home/miri/Documents/university/DataLit/math_extraction/extraced_math"
MEM_LIMIT = 2500 * 1024 * 1024 #2.5GB
TIMEOUT = 10 # in seconds
NUM_WORKERS = 6
SKIP_EXISTING = False
PRINT_EXPECTED_CONVERSION = True
list_args = []

for folder in os.listdir(TEX_PATH):
    list_args.append([os.path.join(TEX_PATH,folder),os.path.join(SAVE_PATH,folder)])

def _parse(e):
    (tex_path,save_path) = e
    os.makedirs(save_path,exist_ok=True)

    # Skip if was already parsed
    if SKIP_EXISTING and os.path.exists(os.path.join(save_path,"parsed.math")):
        return
    
    # Try to identify the .tex file for parsing
    main_tex = find_main_tex(tex_path)

    if main_tex:
        result = parse(tex_path,save_path,main_tex,MEM_LIMIT,TIMEOUT)

        if PRINT_EXPECTED_CONVERSION:
            expected_conversion_rate = [os.path.exists(os.path.join(SAVE_PATH,folder,"parsed.math")) for folder in os.listdir(SAVE_PATH)]
            expected_conversion_rate = [int(e) for e in expected_conversion_rate]
            expected_conversion_rate = round(100*sum(expected_conversion_rate)/len(expected_conversion_rate), 2)

            print("{0} | Expected Conversion rate: {1}%".format(result, expected_conversion_rate))
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