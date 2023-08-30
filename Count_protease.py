import os
import pandas as pd
import re
import shutil

def load_indicators(indicator_file):
    indicators_dict = {}
    with open(indicator_file, "r") as indicators_file:
        for line in indicators_file:
            if line.startswith(">"):
                indicator = line.strip()[1:].split(" ")[0]  
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
                fields[1] = indicators_dict[indicator][1:]  
            results.append("\t".join(fields))
    return results

def save_results(results, output_file):
    with open(output_file, "w") as output_file:
        for line in results:
            output_file.write(line + "\n")

def select_best_match(blast_file):
    best_matches = {}
    with open(blast_file, "r") as blast_file:
        for line in blast_file:
            fields = line.strip().split("\t")
            if len(fields) >= 12:
                protein = fields[0]
                protease = fields[1]
                score = float(fields[11])

                if protein not in best_matches:
                    best_matches[protein] = (protease, score)
                else:
                    _, best_score = best_matches[protein]
                    if score > best_score:
                        best_matches[protein] = (protease, score)

    return best_matches

def save_best_matches(best_matches, output_folder, file_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, file_name)

    with open(output_file, "w") as output_file:
        for protein, (protease, score) in best_matches.items():
            output_file.write(f"{protein}\t{protease}\t{score}\n")

def count_proteases_in_blast(blast_file):
    protease_count = {}
    with open(blast_file, "r") as blast_file:
        for line in blast_file:
            fields = line.strip().split("\t")
            if len(fields) >= 2:
                protease = fields[1]
                protease_count[protease] = protease_count.get(protease, 0) + 1
    return protease_count

def save_protease_count(protease_count, output_folder, file_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, file_name)

    with open(output_file, "w") as output_file:
        for protease, count in protease_count.items():
            output_file.write(f"{protease}\t{count}\n")

def main():
    blast_folder = "Blast_terminados"
    indicator_file = "indicators_without_source.txt"
    blast_output_folder = "Blast_complete_indicator"
    best_match_output_folder = "blast_best_match"
    protease_count_output_folder = "protease_count"
    renamed_output_folder = "blast_best_match/count/shortened_name"
    summary_output_file = "summary_table.csv"
    
    if not os.path.exists(blast_output_folder):
        os.makedirs(blast_output_folder)

    if not os.path.exists(best_match_output_folder):
        os.makedirs(best_match_output_folder)

    if not os.path.exists(protease_count_output_folder):
        os.makedirs(protease_count_output_folder)

    if not os.path.exists(renamed_output_folder):
        os.makedirs(renamed_output_folder)

    indicators_dict = load_indicators(indicator_file)

    blast_files = [f for f in os.listdir(blast_folder) if f.endswith(".txt")]
    for blast_file in blast_files:
        blast_file_path = os.path.join(blast_folder, blast_file)
        
        results = replace_indicators(blast_file_path, indicators_dict)
        blast_output_file = os.path.join(blast_output_folder, f"{blast_file}")
        save_results(results, blast_output_file)
        
        best_matches = select_best_match(blast_output_file)
        best_match_file_name = f"result_{os.path.splitext(blast_file)[0]}.txt"
        best_match_output_file = os.path.join(best_match_output_folder, best_match_file_name)  
        save_best_matches(best_matches, best_match_output_folder, best_match_file_name)
        
        protease_count = count_proteases_in_blast(best_match_output_file)
        protease_count_file_name = f"count_{os.path.splitext(blast_file)[0]}.txt"
        save_protease_count(protease_count, protease_count_output_folder, protease_count_file_name)
        
        source_directory = protease_count_output_folder
        destination_directory = renamed_output_folder
        pattern = r".*_([a-z]_[^_]+)\.txt.*"
        
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        
        for file_name in os.listdir(source_directory):
            file_path = os.path.join(source_directory, file_name)
            
            if os.path.isfile(file_path):
                match = re.match(pattern, file_name)
                
                if match:
                    species = match.group(1)
                    new_file_path = os.path.join(destination_directory, f"{species}.txt")
                    
                    shutil.copy(file_path, new_file_path)
                    print(f"File {file_name} renamed and copied as {species}.txt")
                else:
                    print(f"Couldn't find a species name in the file {file_name}")
    
    directory = renamed_output_folder
    protease_types = ["S", "C", "A", "M", "I", "T", "G"]
    protease_data = {protease_type: {} for protease_type in protease_types}

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            species_name = filename.split(".")[0]
            protease_counts = {protease_type: 0 for protease_type in protease_types}

            with open(os.path.join(directory, filename), "r") as file:
                for line in file:
                    parts = line.split("\t")
                    if len(parts) >= 2:
                        text = parts[0]
                        quantity = int(parts[1])
                        protease_type = extract_protease_type(text, protease_types)
                        if protease_type:
                            protease_counts[protease_type] += quantity

            for protease_type, count in protease_counts.items():
                protease_data[protease_type][species_name] = count

    table = [["Protease Type"] + list(protease_data[protease_types[0]].keys())]

    for protease_type in protease_types:
        row = [protease_type]
        row.extend(protease_data[protease_type].values())
        table.append(row)

    df = pd.DataFrame(table)
    df.to_csv(summary_output_file, index=False, header=None)

def extract_protease_type(text, protease_types):
    keywords = ["family", "subfamily"]
    for keyword in keywords:
        index = text.find(keyword)
        if index != -1:
            protease_letter_index = index + len(keyword) + 1
            if protease_letter_index < len(text):
                protease_letter = text[protease_letter_index]
                if protease_letter in protease_types:
                    return protease_letter
    return None

if __name__ == "__main__":
    main()
