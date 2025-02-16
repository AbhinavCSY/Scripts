#!/bin/bash

# Check if the input JSON file is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <input_json_file>"
  exit 1
fi

input_file="$1"
output_file="output.json"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
  echo "jq is not installed. Please install it and try again."
  exit 1
fi

# Start the JSON array
echo "[" > "$output_file"

# Read the input file and process each entry
jq -c '.[]' "$input_file" | while read -r entry; do
  title=$(echo "$entry" | jq -r '.title')
  severity=$(echo "$entry" | jq -r '.severity')

  # Construct the new entry
  new_entry=$(jq -n \
    --arg program_name "APRA 234 STANDARD" \
    --arg control_name "$title" \
    --arg control_description "Maintain an information security capability commensurate with the size and extent of threats to the organization's information assets." \
    --arg plugin_name "Storage Accounts Encryption" \
    --arg description "Ensures encryption is enabled for Storage Accounts" \
    --arg severity "$severity" \
    --arg recommended_action "Ensure all Storage Accounts are configured with a BYOK key." \
    --arg link "https://learn.microsoft.com/en-us/azure/storage/common/storage-service-encryption-customer-managed-keys" \
    '{
      "Program Name": $program_name,
      "Control Name": $control_name,
      "Control Description": $control_description,
      "Plugin Name": $plugin_name,
      "Description": $description,
      "Severity": $severity,
      "Recommended Action": $recommended_action,
      "Link": $link
    }')

  # Append the new entry to the output file
  echo "$new_entry," >> "$output_file"
done

# Remove the trailing comma and close the JSON array
sed -i '$ s/,$//' "$output_file"
echo "]" >> "$output_file"

echo "Output has been written to $output_file"

