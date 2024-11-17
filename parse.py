import subprocess 
import argparse
import os
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser()
parser.add_argument("path_to_tex_folder", type=str)
args = parser.parse_args()

to_map = []

# Iterate over all subfolders in the directory
for id in os.listdir(args.path_to_tex_folder):
    if os.path.isfile(args.path_to_tex_folder + "/" + id):
        continue
    path = args.path_to_tex_folder + "/" + id
    
    log = {"tex" : None, "json" : None, "error" : None}

    files = os.listdir(path)

    # Skip this folder if there is already a parsed file
    if "parsed.json" in files or "parsed.xml" in files:
        continue

    # Try to find the main tex file 
    tex_files = [f for f in files if f.endswith(".tex")]
    tex_files_with_bbl = [f for f in tex_files if f.split(".tex")[0]+".bbl" in files]
    
    # First choice for the main tex file is a .tex file with a matching .bbl file. If there is more than one .tex with matching .bbl we skip that folder
    # Second choice for the main tex file is a .tex from the directory. If there is more than one .tex we skip that folder
    if len(tex_files_with_bbl) == 0:
        if len(tex_files) == 1:
            main_tex = tex_files[0]
        else:
            continue
    elif len(tex_files_with_bbl) == 1:
        main_tex = tex_files_with_bbl[0]
    else:
        continue

    to_map.append((path,main_tex))

def parse(e):
    # Takes as input the path to the folder with the .tex and the name of the .tex as a tuple.
    # The .tex file is then parsed using a bash command.
    # Path and file have to be specified separately because the bash command is executed in the directory with the .tex file.
    path,main_tex = e

    
    try:
        subprocess.run(["pandoc","{0}".format(main_tex),"-o {0}".format("parsed.json")],timeout=180,check=True,cwd=path)
        return "Passed"
    except Exception as e1:
        try:
            subprocess.run(["latexml","{0}".format(main_tex),"--output={0}".format("parsed.xml"),"--log={0}".format("parsed.log"),"--quiet"],timeout=180,check=True,cwd=path)
            return "Passed"
        except Exception as e2:
            return (e1,e2)

# Parse all collected files
with ThreadPoolExecutor(max_workers=12) as executor:
    results = list(executor.map(parse, to_map))

# Print how many were successfully parsed and how many files in total we tried to parse
print(sum([int(e=="Passed") for e in results]))
print(len(results))