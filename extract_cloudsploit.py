import os
import json
import glob
import subprocess
import re

def clone_repo(repo_url, clone_dir):
    if os.path.exists(clone_dir):
        print(f"Repository already exists at {clone_dir}, pulling latest changes...")
        subprocess.run(["git", "-C", clone_dir, "pull"], check=True)
    else:
        print(f"Cloning repository from {repo_url}...")
        subprocess.run(["git", "clone", repo_url, clone_dir], check=True)

def find_plugin_dirs(base_dir):
    plugin_dirs = {}
    for cloud in ["aws", "google", "azure"]:
        potential_dir = os.path.join(base_dir, "plugins", cloud)
        if os.path.exists(potential_dir):
            plugin_dirs[cloud] = potential_dir
    return plugin_dirs

def extract_plugins(plugin_dir, output_file):
    plugins = []
    for file_path in glob.glob(os.path.join(plugin_dir, '**', '*.js'), recursive=True):
        if file_path.endswith(".spec.js"):  # Skip spec files
            continue
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            try:
                title_match = re.search(r"title:\s*'([^']+)'", content)
                severity_match = re.search(r"severity:\s*'([^']+)'", content)
                more_info_match = re.search(r"more_info:\s*'([^']+)'", content)
                domain_match = re.search(r"domain:\s*'([^']+)'", content)
                
                if title_match:
                    plugins.append({
                        'plugin_name': title_match.group(1),
                        'severity': severity_match.group(1) if severity_match else '',
                        'more_info': more_info_match.group(1) if more_info_match else '',
                        'domain': domain_match.group(1) if domain_match else ''
                    })
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    if plugins:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(plugins, f, indent=4)
        print(f"Extracted {len(plugins)} plugins to {output_file}")
    else:
        print(f"No valid plugin data extracted from {plugin_dir}.")

def main():
    repo_url = "https://github.com/aquasecurity/cloudsploit.git"
    clone_dir = "cloudsploit"
    
    clone_repo(repo_url, clone_dir)
    plugin_dirs = find_plugin_dirs(clone_dir)
    output_files = {cloud: f"{cloud}_plugins.json" for cloud in plugin_dirs.keys()}
    
    for cloud, plugin_dir in plugin_dirs.items():
        if os.path.exists(plugin_dir):
            extract_plugins(plugin_dir, output_files[cloud])
        else:
            print(f"Plugin directory {plugin_dir} does not exist.")

if __name__ == "__main__":
    main()
