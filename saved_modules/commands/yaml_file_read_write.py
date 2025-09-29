import yaml
from pathlib import Path
from main import COPY_LIST_YAML


def generate_yaml(etc_files: list[Path], dot_files: list[Path]):
    """
    Generate a YAML file with 'dest' and 'src' based on the provided lists of files.

    Parameters:
        etc_files (list): List of destination paths (in /etc).
        dot_files (list): List of source paths (dot files).
        diff_files (list): List of diff files (optional for now).
        yaml_output_path (str): Path to save the generated YAML file.
    """
    # Prepare the list of dictionaries with 'dest' and 'src'
    files_to_copy = []

    for etc_file, dot_file in zip(etc_files, dot_files):
        files_to_copy.append({"dest": str(etc_file), "src": str(dot_file)})

    # Prepare the YAML structure
    yaml_data = {"files_to_copy": files_to_copy}

    # Write the YAML to a file
    try:
        with open(COPY_LIST_YAML, "w") as yaml_file:
            yaml.dump(yaml_data, yaml_file, default_flow_style=False, indent=2)
        print(f"✅ YAML file successfully written to {COPY_LIST_YAML}")
    except Exception as e:
        print(f"❌ Error writing YAML file: {e}")
