import json

# Load JSON data from files
with open('file1.json', 'r') as f1, open('file2.json', 'r') as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

# Extract Plugin Names from the first file
plugin_names = {item['Plugin Name'] for item in data1}

# Filter the second file to remove duplicates
filtered_data2 = [item for item in data2 if item['Plugin Name'] not in plugin_names]

# Count the number of duplicates removed
duplicates_removed = len(data2) - len(filtered_data2)

# Save the filtered data to a new file
with open('file2_filtered.json', 'w') as f_out:
    json.dump(filtered_data2, f_out, indent=4)

# Print the number of duplicates removed
print(f"Number of duplicates removed: {duplicates_removed}")

