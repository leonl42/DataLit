import os
import re
import math
import json
from tqdm import tqdm
from copy import deepcopy
import argparse
import pandas as pd

GREEK_LETTERS_REGEX_PATTERN = r'\\\\(?:alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|omicron|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega)'
OPERATIONS_REGEX_PATTERN = r'[+\-*/=<>]'
SPECIAL_SYMBOLS_REGEX_PATTERN = r'[{}()\[\]_^]'
DECORATORS_REGEX_PATTERN = r'\\\\(?:boldsymbol|bm)'


def parse_latex_equation(latex_str):
    """
    Claude 3.5 Sonnet did this primarily, all the other functions are mine.
    """
    # Initialize categories
    parsed = {
        'variables': set(),
        'subscripts': set(),
        'superscripts': set(),  # Added superscripts category
        'greek_letters': set(),
        'operations': set(),
        'special_symbols': set(),
        'decorators': set()  # For boldsymbol, bm and similar commands
    }
    
    # Define regex patterns for double-escaped commands
    patterns = {
        'greek_letters': GREEK_LETTERS_REGEX_PATTERN,
        'operations': OPERATIONS_REGEX_PATTERN,
        'special_symbols': SPECIAL_SYMBOLS_REGEX_PATTERN,
        'decorators': DECORATORS_REGEX_PATTERN,
    }
    
    # Process LaTeX commands first
    command_matches = re.finditer(r'\\\\[a-zA-Z]+', latex_str)
    for match in command_matches:
        command = match.group()
        if command in (r'\\boldsymbol', r'\\bm'):
            parsed['decorators'].add(command)
        elif re.match(patterns['greek_letters'], command):
            parsed['greek_letters'].add(command)
    
    # Extract other elements, being careful not to split LaTeX commands
    command_positions = []
    for match in re.finditer(r'\\\\[a-zA-Z]+', latex_str):
        command_positions.append((match.start(), match.end()))
    
    # Process string character by character, skipping over command positions
    current_pos = 0
    while current_pos < len(latex_str):
        # Check if current position is part of a command
        is_in_command = False
        for start, end in command_positions:
            if start <= current_pos < end:
                is_in_command = True
                current_pos = end
                break
        
        if not is_in_command:
            char = latex_str[current_pos]
            if re.match(patterns['operations'], char):
                parsed['operations'].add(char)
            elif re.match(patterns['special_symbols'], char):
                parsed['special_symbols'].add(char)
            elif re.match(r'[a-zA-Z]', char) and not any(start <= current_pos < end for start, end in command_positions):
                parsed['variables'].add(char)
            current_pos += 1
    
    # Extract subscripts (characters after _)
    subscript_matches = re.finditer(r'_\{([^}]*)\}|_([a-zA-Z0-9])', latex_str)
    for match in subscript_matches:
        subscript = match.group(1) or match.group(2)
        if subscript is not None and '\\\\' not in subscript:  # Only add as subscript if it's not a LaTeX command
            parsed['subscripts'].add(subscript)
    
    # Extract superscripts (characters after ^)
    superscript_matches = re.finditer(r'\^\{([^}]*)\}|\^([a-zA-Z0-9])', latex_str)
    for match in superscript_matches:
        superscript = match.group(1) or match.group(2)
        if superscript is not None and '\\\\' not in superscript:  # Only add as superscript if it's not a LaTeX command
            parsed['superscripts'].add(superscript)
    
    return parsed

def is_float(s):
    if "." not in s:
        return False
    s = s.split(".")
    return all(c.isdigit() for c in s)

def prefix_set(l):
    out = []
    lendiff = 0
    for item in l:
        sout = set(out)
        sitem = set(item)

        diff = sitem - sitem.intersection(sout)
        lendiff += len(list(diff))
        
        del diff
        del sitem
        del sout
        
        out = out + item
        out = list(set(out))

    if len(l) == 0:
        raise Exception("ATTENTION ATTENTION THIS IS AN EXCEPTION. l HAS LENGTH 0 IN LINE 116")
    
    return out, lendiff / len(l)
    

def one_pass_mean_std(data):
    n = 0
    mean = 0.0
    M2 = 0.0  # Second moment about the mean
    
    # First pass computes mean and sum of squared differences from the current mean
    for x in data:
        n += 1
        delta = x - mean
        mean += delta / n
        delta2 = x - mean
        M2 += delta * delta2
    
    if n < 1:
        raise ValueError("Cannot compute statistics on empty sequence")
    
    # Compute standard deviation
    if n < 2:
        std = 0.0
    else:
        std = math.sqrt(M2 / (n - 1))  # Use n-1 for sample standard deviation
        
    return mean, std    


def refine_parsed_equation(parsed):
    mutable_parsed = deepcopy(parsed)
    for k, v in mutable_parsed.items():
        mutable_parsed[k] = list(v)

    unique_symbols = mutable_parsed["variables"] + mutable_parsed["greek_letters"]
    
    for k in ["subscripts", "superscripts"]:
        for symbol in mutable_parsed[k]:
            if symbol.isdigit() or is_float(symbol):
                mutable_parsed[k].remove(symbol)
    
    unique_symbols = unique_symbols + mutable_parsed["superscripts"] + mutable_parsed["subscripts"]
    return {"unique_symbols": unique_symbols, "num_uniques": len(unique_symbols)}


def transform_math(paper_math):
    # Transform math from format:
    # """
    # (Chapter, Equation)
    # .
    # .
    # .
    # (Chapter, Equation)
    # """
    # To a format that is better for processing

    paper_math = [item.replace("(","").replace(")","").replace("\n","") for item in paper_math]
        
    equations = [item.split(", ")[1][1:-1] for item in paper_math]
    parsed_equations = [parse_latex_equation(eq) for eq in equations]
    refined_parsed_equations = [refine_parsed_equation(parsed) for parsed in parsed_equations]

    return refined_parsed_equations


def num_equations(paper_math, equations):
    # Returns the number of equations
    return len(equations)

def overall_unique_symbols(paper_math, equations):
    return prefix_set([item["unique_symbols"] for item in equations])[0]

def mean_num_new_symbols_introduced(paper_math, equations):
    return prefix_set([item["unique_symbols"] for item in equations])[1]

def num_overall_unique_symbols(paper_math, equations):
    return len(prefix_set([item["unique_symbols"] for item in equations])[0])

def mean_num_unique_symbols(paper_math, equations):
    return one_pass_mean_std([item["num_uniques"] for item in equations])[0]

def std_of_unique_symbols(paper_math, equations):
    return one_pass_mean_std([item["num_uniques"] for item in equations])[1]

def max_representational_complexity(paper_math, equations):
    meta_data_per_equation = {j: equations[j] for j in range(len(equations))}
    return max(meta_data_per_equation[x]["num_uniques"] for x in meta_data_per_equation)

def get_recommendation_avg(metadata_json, paper_id):
    for metadata_paper in metadata_json:
        if metadata_paper["id"] == paper_id:
            return metadata_paper["recommendation_avg"]
        
    raise Exception("Could not find metadata for: {0}".format(id))

def get_status(metadata_json, paper_id):
    for metadata_paper in metadata_json:
        if metadata_paper["id"] == paper_id:
            return metadata_paper["status"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and analyze LaTeX files.")

    parser.add_argument(
        '--math-path', type=str, help="Path to the folder with the folder containing the extracted math."
    )
    parser.add_argument(
        '--metadata-json', type=str, help=""
    )

    parser.add_argument(
        '--conference', type=str, help="Either iclr or neurips", default="iclr"
    )

    parser.add_argument(
        '--out', type=str, help="Path to the output csv."
    )

    args = parser.parse_args()

    with open(args.metadata_json,"r") as f:
        metadata_json = json.load(f)

    # Get paper id of all parsed paper
    paper_ids = [paper_id for paper_id in os.listdir(args.math_path) if os.path.exists(os.path.join(args.math_path,paper_id,"parsed.math"))]

    out_df = pd.DataFrame({"paper_id" : [],
                           "num_equations" : [],
                           "mean_num_new_symbols_introduced":[],
                           "num_overall_unique_symbols":[],
                           "mean_num_unique_symbols": [],
                           "std_of_unique_symbols": [],
                           "max_representational_complexity": [],
                           "recommendation_avg" : [],
                           "status" : []})
    out_df.set_index("paper_id", inplace=True)

    for paper_id in tqdm(paper_ids):
        
        # Read parsed.math file and simplify format
        with open(os.path.join(args.math_path, paper_id, "parsed.math"), "r") as f:
            paper_math = f.readlines()
        equations = transform_math(paper_math)

     
        try:
            # Extract all features and save them in the Dataframe
            result = {"paper_id" : paper_id}
            result["num_equations"] = num_equations(paper_math, equations)
            result["mean_num_new_symbols_introduced"] = mean_num_new_symbols_introduced(paper_math, equations)
            result["num_overall_unique_symbols"] = num_overall_unique_symbols(paper_math, equations)
            result["mean_num_unique_symbols"] = mean_num_unique_symbols(paper_math, equations)
            result["std_of_unique_symbols"] = std_of_unique_symbols(paper_math, equations)
            result["max_representational_complexity"] = max_representational_complexity(paper_math, equations)
            result["recommendation_avg"] = get_recommendation_avg(metadata_json,paper_id)
            result["status"] = get_status(metadata_json,paper_id)

            result = pd.DataFrame([result])
            result.set_index("paper_id", inplace=True)

            out_df = pd.concat([out_df,result])

        except Exception as e:
            print("Skipping: {0} due to Exception: {1}".format(os.path.join(args.math_path,paper_id),e))

    with open(args.out, "w") as f:
        out_df.to_csv(f)
