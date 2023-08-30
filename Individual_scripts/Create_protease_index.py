# Protease database file name
protease_file = "protease.lib"

# File name to save the indicators
indicators_file = "indicators_without_source.txt"

# List to store the indicators
indicators = []

# Open the protease.lib file in read mode
with open(protease_file, "r") as file:
    for line in file:
        if line.startswith(">MER"):
            # Extract the alphanumeric indicator and add it to the indicators list
            indicator = line.strip().split("~")[0]  # Split the line by "~" and take the first part
            indicators.append(indicator)

# Save the indicators in the indicators.txt file
with open(indicators_file, "w") as indicators_file:
    for indicator in indicators:
        indicators_file.write(indicator + "\n")
