import pandas as pd
import os

def main():
    directory = "C:/Users/alexc/Desktop/Blast_completed/Blast_complete_indicator/blast_best_match/count/shortened_name"
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
    df.to_csv("summary_table.csv", index=False, header=None)

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
