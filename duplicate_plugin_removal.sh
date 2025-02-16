#!/bin/bash

# File paths
fileA="fileA.csv"
fileB="fileB.csv"
outputFile="fileA_filtered.csv"

# Column name to compare
columnName="Plugin Name"

# Get the column number for "Plugin Name"
columnNum=$(head -1 "$fileA" | awk -F, -v colName="$columnName" '{for(i=1;i<=NF;i++) if($i==colName) print i}')

# Create an associative array to store plugin names from file B
declare -A pluginNamesB

# Read file B and store the plugin names in the array
while IFS=, read -r -a fields; do
  if [[ ${fields[$((columnNum-1))]} != "$columnName" ]]; then
    pluginNamesB["${fields[$((columnNum-1))]}"]=1
  fi
done < <(tail -n +2 "$fileB")

# Process file A, keeping only entries that are not in file B
{
  # Print header
  head -1 "$fileA"
  
  # Print non-duplicate rows
  while IFS=, read -r -a fields; do
    if [[ ${fields[$((columnNum-1))]} != "$columnName" && -z ${pluginNamesB["${fields[$((columnNum-1))]}"]} ]]; then
      echo "${fields[*]}"
    fi
  done < <(tail -n +2 "$fileA")
} > "$outputFile"

echo "Filtered file has been saved to $outputFile"

