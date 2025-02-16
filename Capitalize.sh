#!/bin/bash

# Check if the file name is passed as an argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <json-file>"
  exit 1
fi

# Assign the file name to a variable
json_file=$1

# Check if the file exists
if [ ! -f "$json_file" ]; then
  echo "File not found!"
  exit 1
fi

# Use jq to recursively update all Severity fields
updated_json=$(jq 'walk(
  if type == "object" and has("Severity") then
    .Severity |= (.[0:1] | ascii_upcase) + (.[1:] | ascii_downcase)
  else
    .
  end)' "$json_file")

# Check if the updated_json is not empty
if [ -z "$updated_json" ]; then
  echo "An error occurred while updating the JSON."
  exit 1
fi

# Write the updated JSON back to the file
echo "$updated_json" > "$json_file"

echo "Severity field updated successfully."

