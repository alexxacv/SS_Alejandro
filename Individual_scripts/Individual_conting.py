import os

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

if __name__ == "__main__":
    blast_folder = "C:/Users/alexc/Desktop/Blast_completed/Full_indicator_blast/best_match_blast"
    output_folder = "C:/Users/alexc/Desktop/Blast_completed/Full_indicator_blast/count"  # Full path of the output folder

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for blast_file in os.listdir(blast_folder):
        input_file = os.path.join(blast_folder, blast_file)
        output_file_name = f"count_{os.path.splitext(blast_file)[0]}.txt"

        # Count proteases in the current BLAST file
        protease_count = count
