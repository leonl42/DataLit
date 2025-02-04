import json
import requests
import time
from typing import Dict, List, Tuple, Optional
import urllib.parse
import argparse
from collections import Counter
import os
import gzip
import shutil
import tarfile
import xml.etree.ElementTree as ET

def get_status_distribution(papers: List[Dict]) -> Dict[str, int]:
    """
    Count the number of papers for each status in the dataset.
    """
    return Counter(paper['status'] for paper in papers)

def get_arxiv_id_and_title_from_response(response_text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract arXiv ID and title from API response XML.
    Returns a tuple of (arxiv_id, title) or (None, None) if not found.
    """
    try:
        root = ET.fromstring(response_text)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        entry = root.find('.//atom:entry', namespace)
        if entry is not None:
            id_elem = entry.find('atom:id', namespace)
            title_elem = entry.find('atom:title', namespace)
            if id_elem is not None and title_elem is not None:
                arxiv_id = id_elem.text.split('/')[-1]
                return arxiv_id, title_elem.text.strip()
    except Exception as e:
        print(f"Error parsing arXiv response: {e}")
    return None, None

def titles_match(title1: str, title2: str, threshold: float = 0.9) -> bool:
    """
    Check if titles in the arXiv API response and actual title match, as API search is a bit buggy.
    """
    
    t1 = ' '.join(title1.lower().split())
    t2 = ' '.join(title2.lower().split())
    
    # If exact match, return True
    if t1 == t2:
        return True
    
    return False

def download_source(arxiv_id: str, save_path: str) -> bool:
    """
    Download and extract LaTeX source files for a given arXiv ID.
    """
    try:
        url = f'https://arxiv.org/src/{arxiv_id}'
        print(f"Downloading source files for arXiv:{arxiv_id}")
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error downloading source: Status code {response.status_code}")
            return False
        
        # Get the filename from Content-Disposition header, or fall back to URL parsing
        content_disp = response.headers.get('Content-Disposition', '')
        if 'filename=' in content_disp:
            filename = content_disp.split('filename=')[-1].strip('"')
        else:
            filename = url.split('/')[-1]
        
        print(f"Downloaded filename: {filename}")
        
        # Create the save directory
        os.makedirs(save_path, exist_ok=True)
        
        # Save the downloaded file with 
        temp_file = os.path.join(os.path.dirname(save_path), f'temp_{arxiv_id}_{filename}')
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        
        # Try to extract based on file type
        if filename.endswith('.tar.gz'):
            with tarfile.open(temp_file) as tar:
                # Use filter to suppress the deprecation warning
                tar.extractall(path=save_path, filter='data')
        elif filename.endswith('.gz'):
            # Handle pure gz files
            output_file = os.path.join(save_path, filename[:-3] + ".tex")  # Remove .gz extension
            with gzip.open(temp_file, 'rb') as gz_in:
                with open(output_file, 'wb') as f_out:
                    shutil.copyfileobj(gz_in, f_out)
        else:
            print(f"Unrecognized file format: {filename}")
            os.remove(temp_file)
            return False
        
        # Clean up temporary file
        os.remove(temp_file)
        print(f"Successfully extracted files to {save_path}")
        return True
    
    except Exception as e:
        print(f"Error downloading/extracting source: {e}")
        return False

def search_arxiv(title: str, paper_id: str, sources_dir: str) -> bool:
    """
    Search arxiv for a paper title and download its source if found.
    """
    encoded_title = urllib.parse.quote(title)
    url = f'http://export.arxiv.org/api/query?search_query={encoded_title}&max_results=1&searchtype=title'
    
    print(f"\nSearching arXiv for paper: {title}")
    print(f"Using URL: {url}")
    
    time.sleep(3) # arXiv requests that API only be queried every 3 seconds at most
    
    try:
        response = requests.get(url)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            has_entry = '<entry>' in response.text
            print(f"Paper found on arXiv: {has_entry}")
            
            if has_entry:
                arxiv_id, arxiv_title = get_arxiv_id_and_title_from_response(response.text)
                if arxiv_id and arxiv_title:
                    if titles_match(title, arxiv_title):
                        print(f"Title match confirmed. ArXiv title: {arxiv_title}")
                        paper_dir = os.path.join(sources_dir, str(paper_id))  # Create directory for this paper's source
                        return download_source(arxiv_id, paper_dir)
                    else:
                        print(f"Title mismatch. ArXiv title: {arxiv_title}")
                        return False
            return False
        else:
            print(f"Error response from arXiv API")
            return False
    except Exception as e:
        print(f"Error searching for title: {title}")
        print(f"Error: {e}")
        return False

def analyze_papers(json_file: str, limit: int = None) -> Tuple[Dict[str, int], Dict[str, float]]:
    """
    Analyze papers from a JSON file and return statistics about arxiv availability.
    """
    try:
        # Create directory for sources based on JSON filename
        json_basename = os.path.splitext(os.path.basename(json_file))[0]
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sources_dir = os.path.join(base_dir, json_basename)
        os.makedirs(sources_dir, exist_ok=True)
        
        print(f"Reading JSON file: {json_file}")
        with open(json_file, 'r') as f:
            papers = json.load(f)
        
        # Display initial distribution
        print("\nInitial paper distribution:")
        status_dist = get_status_distribution(papers)
        total_papers = len(papers)
        print(f"Total papers in dataset: {total_papers}")
        for status, count in sorted(status_dist.items()):
            percentage = (count / total_papers) * 100
            print(f"{status}: {count} papers ({percentage:.2f}%)")
        
        if limit is not None:
            papers = papers[:limit]
            print(f"\nProcessing first {limit} papers...")
        else:
            print(f"\nProcessing all {len(papers)} papers...")
        
        stats = {
            'total': len(papers),
            'accepted': 0,
            'rejected': 0,
            'accepted_on_arxiv': 0,
            'rejected_on_arxiv': 0
        }
        
        for paper in papers:
            print(f"\n--- Processing paper {paper['id']} ---")
            print(f"Title: {paper['title']}")
            print(f"Status: {paper['status']}")
            
            is_rejected = 'reject' or 'desk reject' in paper['status'].lower()
            
            if is_rejected:
                stats['rejected'] += 1
                print("Paper status: Rejected")
            else:
                stats['accepted'] += 1
                print("Paper status: Accepted")
            
            # Search on arxiv and download source if found
            if search_arxiv(paper['title'], paper['id'], sources_dir):
                if is_rejected:
                    stats['rejected_on_arxiv'] += 1
                else:
                    stats['accepted_on_arxiv'] += 1
        
        percentages = {
            'total_on_arxiv': ((stats['accepted_on_arxiv'] + stats['rejected_on_arxiv']) / 
                              stats['total'] * 100 if stats['total'] > 0 else 0),
            'accepted_on_arxiv': (stats['accepted_on_arxiv'] / 
                                stats['accepted'] * 100 if stats['accepted'] > 0 else 0),
            'rejected_on_arxiv': (stats['rejected_on_arxiv'] / 
                                 stats['rejected'] * 100 if stats['rejected'] > 0 else 0)
        }
        
        return stats, percentages
    
    except Exception as e:
        print(f"Error in analyze_papers: {e}")
        raise

def main():
    try:
        parser = argparse.ArgumentParser(description='Analyze papers for arXiv availability and download sources')
        parser.add_argument('--json_file', type=str, default='papers.json',
                          help='Path to the JSON file containing paper data')
        parser.add_argument('--limit', type=int, default=None,
                          help='Maximum number of papers to process. If not specified, process all papers')
        
        args = parser.parse_args()
        
        print(f"\nStarting analysis with the following settings:")
        print(f"JSON file: {args.json_file}")
        print(f"Paper limit: {'All' if args.limit is None else args.limit}")
        
        if not os.path.exists(args.json_file):
            print(f"\nError: JSON file '{args.json_file}' not found!")
            return
        
        # Get base directory from json file location
        json_basename = os.path.splitext(os.path.basename(args.json_file))[0]
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sources_dir = os.path.join(base_dir, json_basename)
        
        stats, percentages = analyze_papers(args.json_file, args.limit)
        
        print("\nRaw Statistics:")
        print(f"Total papers analyzed: {stats['total']}")
        print(f"Accepted papers: {stats['accepted']}")
        print(f"Rejected papers: {stats['rejected']}")
        print(f"Accepted papers on arxiv: {stats['accepted_on_arxiv']}")
        print(f"Rejected papers on arxiv: {stats['rejected_on_arxiv']}")
        
        print("\nPercentages:")
        print(f"Total papers on arxiv: {percentages['total_on_arxiv']:.2f}%")
        if stats['accepted'] > 0:
            print(f"Accepted papers on arxiv: {percentages['accepted_on_arxiv']:.2f}%")
        if stats['rejected'] > 0:
            print(f"Rejected papers on arxiv: {percentages['rejected_on_arxiv']:.2f}%")
        
        # Create stats output
        output_stats = {
            'run_settings': {
                'json_file': args.json_file,
                'paper_limit': args.limit,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'raw_statistics': stats,
            'percentages': percentages
        }
        
        # Write to both JSON and human-readable formats
        stats_base_path = os.path.join(sources_dir, 'analysis_stats')
        
        # JSON output
        json_path = f"{stats_base_path}.json"
        with open(json_path, 'w') as f:
            json.dump(output_stats, f, indent=2)
        print(f"\nDetailed statistics saved to: {json_path}")
        
        # Human-readable output
        txt_path = f"{stats_base_path}.txt"
        with open(txt_path, 'w') as f:
            f.write("ArXiv Analysis Statistics\n")
            f.write("=======================\n\n")
            
            f.write("Run Settings:\n")
            f.write(f"- Input file: {args.json_file}\n")
            f.write(f"- Paper limit: {args.limit if args.limit is not None else 'All'}\n")
            f.write(f"- Run timestamp: {output_stats['run_settings']['timestamp']}\n\n")
            
            f.write("Raw Statistics:\n")
            f.write(f"- Total papers analyzed: {stats['total']}\n")
            f.write(f"- Accepted papers: {stats['accepted']}\n")
            f.write(f"- Rejected papers: {stats['rejected']}\n")
            f.write(f"- Accepted papers on arxiv: {stats['accepted_on_arxiv']}\n")
            f.write(f"- Rejected papers on arxiv: {stats['rejected_on_arxiv']}\n\n")
            
            f.write("Percentages:\n")
            f.write(f"- Total papers on arxiv: {percentages['total_on_arxiv']:.2f}%\n")
            if stats['accepted'] > 0:
                f.write(f"- Accepted papers on arxiv: {percentages['accepted_on_arxiv']:.2f}%\n")
            if stats['rejected'] > 0:
                f.write(f"- Rejected papers on arxiv: {percentages['rejected_on_arxiv']:.2f}%\n")
        
        print(f"Summary saved to: {txt_path}")
    
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
