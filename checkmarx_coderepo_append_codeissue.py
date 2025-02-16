python3 <<EOF
          import os
          import json
          def get_code_snippet(lines, start_line, start_column, end_column):
              start_line = max(start_line - 3, 0)  # Start from 3 lines before or 0
              end_line = min(start_line + 5, len(lines))  # End 2 lines after the snippet
              snippet_lines = lines[start_line:end_line]
              highlighted_snippet = []
              for i, line in enumerate(snippet_lines):
                  line_number = start_line + i + 1  # Correct line number offset
                  if line_number == start_line:  # Highlight the start line
                      highlighted_snippet.append(
                          line[:start_column - 1] +
                          "<<<HIGHLIGHT>>>" +
                          line[start_column - 1:end_column] +
                          "<<<END_HIGHLIGHT>>>" +
                          line[end_column:]
                      )
                  else:
                      highlighted_snippet.append(line)
              snippet_with_comments = "// Start of snippet\n"
              snippet_with_comments += "".join(highlighted_snippet)
              snippet_with_comments += "// End of snippet\n"
              return snippet_with_comments
          def process_sarif_file(sarif_path):
              with open(sarif_path, "r") as sarif_file:
                  sarif_data = json.load(sarif_file)
              for run in sarif_data.get("runs", []):
                  for result in run.get("results", []):
                      for location in result.get("locations", []):
                          physical_location = location.get("physicalLocation", {})
                          artifact_location = physical_location.get("artifactLocation", {})
                          region = physical_location.get("region", {})
                          uri = artifact_location.get("uri")
                          start_line = region.get("startLine")
                          start_column = region.get("startColumn")
                          end_column = region.get("endColumn")
                          if uri and start_line and start_column and end_column:
                              file_path = os.path.join(".", uri.lstrip("./"))
                              try:
                                  with open(file_path, "r") as source_file:
                                      lines = source_file.readlines()
                                      snippet_with_comments = get_code_snippet(
                                          lines, start_line, start_column, end_column
                                      )
                                      region["snippet"] = {
                                          "text": snippet_with_comments
                                      }
                              except FileNotFoundError:
                                  print(f"Failed to process file {file_path}: File not found.")
                              except Exception as e:
                                  print(f"Failed to process file {file_path}: {e}")
              with open("tmp_sarif_with_snippets.sarif", "w") as output_file:
                  json.dump(sarif_data, output_file, indent=2)
          process_sarif_file("cx_result.sarif")
          EOF
