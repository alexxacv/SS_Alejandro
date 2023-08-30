import os

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

if __name__ == "__main__":
    input_folder = "C:/Users/alexc/Desktop/Blast_completed/Blast_complete_indicator"
    output_folder = "blast_best_match"

    for blast_file in os.listdir(input_folder):
        if blast_file.endswith(".txt"):
            input_file = os.path.join(input_folder, blast_file)
            file_name = f"result_{os.path.splitext(blast_file)[0]}.txt"

            # Select the best match for each protein in the BLAST file
            best_matches = select_best_match(input_file)

            # Save the results to a text file in the output folder
            save_best_matches(best_matches, output_folder, file_name)
