def replace_indicators(blast_file, indicators_dict):
    results = []
    with open(blast_file, "r") as blast_file:
        for line in blast_file:
            fields = line.strip().split("\t")
            if len(fields) >= 2:  # Check if there are enough columns
                protein = fields[0]
                indicator = fields[1]
                if indicator in indicators_dict:
                    fields[1] = indicators_dict[indicator][1:]  # Remove ">" sign from the indicator
                results.append("\t".join(fields))
            else:
                print(f"Warning: Line does not have enough columns in the file {blast_file}: {line}")
    return results

import os
import pandas as pd

def load_indicators(indicator_file):
    indicators_dict = {}
    with open(indicator_file, "r") as indicators_file:
        for line in indicators_file:
            if line.startswith(">"):
                indicator = line.strip()[1:].split(" ")[0]  # Extract only the indicator
                indicators_dict[indicator] = line.strip()
    return indicators_dict

def replace_indicators(blast_file, indicators_dict):
    results = []
    with open(blast_file, "r") as blast_file:
        for line in blast_file:
            fields = line.strip().split("\t")
            protein = fields[0]
            indicator = fields[1]
            if indicator in indicators_dict:
                fields[1] = indicators_dict[indicator][1:]  # Remove ">" sign from the indicator
            results.append("\t".join(fields))
    return results

def save_results(results, output_file):
    with open(output_file, "w") as output_file:
        for line in results:
            output_file.write(line + "\n")

if __name__ == "__main__":
    # Folder where BLAST files in .txt format are located
    blast_folder = "C:/Users/alexc/Desktop/Blast_completed"

    # Protease indicators file
    indicator_file = "C:/Users/alexc/Desktop/protease_indicators.txt"

    # Folder to save the results
    output_folder = "Blast_complete_indicator"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load indicators from the indicator file
    indicators_dict = load_indicators(indicator_file)

    # Process each BLAST file and save the results
    blast_files = [f for f in os.listdir(blast_folder) if f.endswith(".txt")]
    for blast_file in blast_files:
        blast_file_path = os.path.join(blast_folder, blast_file)
        results = replace_indicators(blast_file_path, indicators_dict)
        output_file = os.path.join(output_folder, f"{blast_file}")
        save_results(results, output_file)
