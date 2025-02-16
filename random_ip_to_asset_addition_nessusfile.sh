#!/bin/bash

# Function to generate a random IP address
generate_random_ip() {
    echo "$((RANDOM % 256)).$((RANDOM % 256)).$((RANDOM % 256)).$((RANDOM % 256))"
}

# Source .nessus file
source_nessus="source.nessus"

# Directory to store the generated files
output_dir="output_nessus_files"

# Create the directory if it doesn't exist
mkdir -p "$output_dir"

# Loop to generate 100 files
for i in {1..100}; do
    # Generate a random IP address
    random_ip=$(generate_random_ip)
    
    # Read the source .nessus file and replace the IP address in the specific tag
    new_nessus=$(sed -E "s|(<tag name=\"host-ip\">)[^<]+(</tag>)|\1$random_ip\2|" "$source_nessus")
    
    # Create the file
    file_name="$output_dir/file_$i.nessus"
    echo "$new_nessus" > "$file_name"
    
    echo "Created $file_name with IP $random_ip"
done

echo "100 files created successfully in $output_dir"

