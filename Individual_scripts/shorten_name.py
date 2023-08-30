import os
import re
import shutil

# Path to the directory where the files are located
source_directory = "C:/Users/alexc/Desktop/Blast_completed/Blast_complete_indicator/blast_best_match/count"

# Directory where the new files will be saved
destination_directory = "C:/Users/alexc/Desktop/Blast_completed/Blast_complete_indicator/blast_best_match/count/shortened_name"

# Regular expression pattern to extract the species name
pattern = r".*_([a-z]_[^_]+)\.txt.*"

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# Iterate through all files in the source directory
for file_name in os.listdir(source_directory):
    file_path = os.path.join(source_directory, file_name)
    
    if os.path.isfile(file_path):
        # Get the species name using the regular expression
        match = re.match(pattern, file_name)
        
        if match:
            species = match.group(1)
            new_file_path = os.path.join(destination_directory, f"{species}.txt")
            
            # Copy the file to the destination directory with the new name
            shutil.copy(file_path, new_file_path)
            print(f"File {file_name} renamed and copied as {species}.txt")
        else:
            print(f"Couldn't find a species name in the file {file_name}")
