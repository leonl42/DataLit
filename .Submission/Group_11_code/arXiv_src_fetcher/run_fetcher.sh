#!/bin/bash

# Exit on error
set -e

# Function to run analysis and ensure completion
run_analysis() {
    local json_file=$1
    echo -e "\n=== Starting analysis for $json_file ==="
    
    # Run the analysis and capture the exit status
    python arXiv_fetcher.py --json_file "$json_file"
    local status=$?
    
    # Check if the analysis completed successfully
    if [ $status -eq 0 ]; then
        echo -e "\n=== Successfully completed analysis for $json_file ==="
        
        # Check if stats files were created
        local base_name=${json_file%.*}  # Remove .json extension
        if [ -f "$base_name/analysis_stats.txt" ]; then
            echo "Statistics file generated successfully"
            
            # Print a brief summary from the stats file
            echo -e "\nSummary for $json_file:"
            grep "Total papers" "$base_name/analysis_stats.txt"
        else
            echo "Warning: Statistics file not found"
        fi
    else
        echo "Error: Analysis failed for $json_file"
        exit 1
    fi
}

# Create log directory if it doesn't exist
mkdir -p logs

# Get current timestamp for log files
timestamp=$(date +"%Y%m%d_%H%M%S")

# Process ICLR 2023
(
    run_analysis "ICLR_2023.json"
    echo -e "\nICLR 2023 analysis complete. Proceeding with NeurIPS 2023...\n"
    sleep 5  
    
    run_analysis "NeurIPS_2023.json"
) 2>&1 | tee "logs/arxiv_analysis_${timestamp}.log"

echo -e "\nAnalysis complete. Full log available at: logs/arxiv_analysis_${timestamp}.log"

# Display summary of created folders and their contents
echo -e "\nCreated folders:"
for dir in ICLR_2023 NeurIPS_2023; do
    if [ -d "$dir" ]; then
        echo "- $dir/"
        echo "  $(find "$dir" -type f | wc -l) files downloaded"
    else
        echo "Warning: $dir directory was not created"
    fi
done