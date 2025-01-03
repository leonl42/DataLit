import os
import re
import json
from tqdm import tqdm
from copy import deepcopy
from statistics import mean, stdev


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
        'greek_letters': r'\\\\(?:alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|omicron|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega)',
        'operations': r'[+\-*/=<>]',
        'special_symbols': r'[{}()\[\]_^]',
        'decorators': r'\\\\(?:boldsymbol|bm)',
    }
    
    # Process LaTeX commands first
    command_matches = re.finditer(r'\\\\[a-zA-Z]+', latex_str)
    for match in command_matches:
        command = match.group()
        if command in (r'\\boldsymbol', r'\\bm'):
            parsed['decorators'].add(command)
        elif re.match(patterns['greek_letters'], command):
            parsed['greek_letters'].add(command)
    
    # Remove the content of special commands to avoid double-counting
    cleaned_str = latex_str
    
    # Extract other elements, being careful not to split LaTeX commands
    command_positions = []
    for match in re.finditer(r'\\\\[a-zA-Z]+', cleaned_str):
        command_positions.append((match.start(), match.end()))
    
    # Process string character by character, skipping over command positions
    current_pos = 0
    while current_pos < len(cleaned_str):
        # Check if current position is part of a command
        is_in_command = False
        for start, end in command_positions:
            if start <= current_pos < end:
                is_in_command = True
                current_pos = end
                break
        
        if not is_in_command:
            char = cleaned_str[current_pos]
            if re.match(patterns['operations'], char):
                parsed['operations'].add(char)
            elif re.match(patterns['special_symbols'], char):
                parsed['special_symbols'].add(char)
            elif re.match(r'[a-zA-Z]', char) and not any(start <= current_pos < end for start, end in command_positions):
                parsed['variables'].add(char)
            current_pos += 1
    
    # Extract subscripts (characters after _)
    subscript_matches = re.finditer(r'_\{([^}]*)\}|_([a-zA-Z0-9])', cleaned_str)
    for match in subscript_matches:
        subscript = match.group(1) or match.group(2)
        if subscript is not None and '\\\\' not in subscript:  # Only add as subscript if it's not a LaTeX command
            parsed['subscripts'].add(subscript)
    
    # Extract superscripts (characters after ^)
    superscript_matches = re.finditer(r'\^\{([^}]*)\}|\^([a-zA-Z0-9])', cleaned_str)
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
    for item in l:
        out = out + item
        out = list(set(out))
    return out

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


def run_parsing_over_papers(data_folder):
    paper_ids = os.listdir(data_folder)
    out = {"num_papers": len(paper_ids)}

    bar = tqdm(total=len(paper_ids))
    for idx, pid in enumerate(paper_ids):

        result = {
            "num_equations": 0,
            "num_overall_unique_symbols": 0,
            "mean_num_unique_symbols": 0.0,
            "std_of_unique_symbols": 0.0,
            "overall_unique_symbols": [],
            "meta_data_per_equation": {}
        }
        path = os.path.join(data_folder, pid, "parsed.math")

        with open(path, "r") as f:
            paper_math = f.readlines()
            result["num_equations"] = len(paper_math)
            paper_math = [item.replace("(","").replace(")","").replace("\n","") for item in paper_math]
            
            equations = [item.split(", ")[1][1:-1] for item in paper_math]
            parsed_equations = [parse_latex_equation(eq) for eq in equations]
            refined_parsed_equations = [refine_parsed_equation(parsed) for parsed in parsed_equations]

            result["meta_data_per_equation"] = {j: refined_parsed_equations[j] for j in range(len(equations))}
            result["overall_unique_symbols"] = prefix_set([item["unique_symbols"] for item in refined_parsed_equations])
            result["num_overall_unique_symbols"] = len(result["overall_unique_symbols"])

            result["mean_num_unique_symbols"] = mean([item["num_uniques"] for item in refined_parsed_equations])
            result["std_of_unique_symbols"] = stdev([item["num_uniques"] for item in refined_parsed_equations])

        out[pid] = result
        bar.update(1)
    
    with open("parsed_papers.json", "w") as f:
        json.dump(out, f, indent=4)
            

if __name__ == "__main__":
    run_parsing_over_papers("extraced_math")


# # Example usage with different types of scripts
# latex_equations = [
#     r'f_{\\boldsymbol{\\theta}}(\\boldsymbol{X})',  # subscript example
#     r'f^{2}_{\\bm{\\theta}}(\\bm{X})',  # both subscript and superscript
#     r'e^{x^2}',  # superscript only
# ]
# latex_equations = [
#     # r"f^{\\phi}_{\\theta + \\alpha}"
#     r'R({\\bm{Z}};\\,\\epsilon):= \\log\\det\\left({\\bm{I}}+ \\frac{d}{n\\epsilon^2} {\\bm{Z}}{\\bm{Z}}^\\top \\right). \\nonumber',
#     r"W(\\sigma_{i},\\sigma_{j})",
#     r"10.39"
# ]

# for eq in latex_equations:
#     print(f"\nParsing equation: {eq}")
#     result = parse_latex_equation(eq)
#     for category, items in result.items():
#         if items:
#             print(f"{category}: {sorted(items)}")
