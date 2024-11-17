import subprocess 
import argparse
import os
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser()
parser.add_argument("path_to_tex_folder", type=str)
args = parser.parse_args()

to_map = []

for id in os.listdir(args.path_to_tex_folder):
    if os.path.isfile(args.path_to_tex_folder + "/" + id):
        continue
    path = args.path_to_tex_folder + "/" + id
    
    log = {"tex" : None, "json" : None, "error" : None}

    files = os.listdir(path)

    if "parsed.json" in files or "parsed.xml" in files:
        continue

    tex_files = [f for f in files if ".tex" in f]
    tex_files_with_bbl = [f for f in tex_files if f.split(".tex")[0]+".bbl" in files]
    
    if len(tex_files_with_bbl) == 0:
        if len(tex_files) == 1:
            main_tex = tex_files[0]
        else:
            continue
    else:
        main_tex = tex_files_with_bbl[0]

    to_map.append((path,main_tex))

def convert(e):
    path,main_tex = e
    try:
        subprocess.run(["pandoc","{0}".format(main_tex),"-o {0}".format("parsed.json")],timeout=360,check=True,cwd=path)
        return "Passed"
    except Exception as e1:
        try:
            subprocess.run(["latexml","{0}".format(main_tex),"--output={0}".format("parsed.xml"),"--log={0}".format("parsed.log"),"--quiet"],timeout=360,check=True,cwd=path)
            return "Passed"
        except Exception as e2:
            return (e1,e2)


with ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(convert, to_map))


print(sum([int(e=="Passed") for e in results]))
print(len(results))