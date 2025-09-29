import yaml
from pathlib import Path


def update_playbook(playbook_path: Path, files_to_yaml: list[dict[str, str]]) -> None:
    try:
        # Read the existing playbook
        with open(playbook_path, "r") as playbook_file:
            playbook_data = yaml.safe_load(playbook_file)

        # Ensure the playbook_data is a list (Ansible playbooks are a list of plays)
        if not isinstance(playbook_data, list):
            raise ValueError("The playbook must be a list of plays.")

        # Check that there is at least one play
        if not playbook_data:
            raise ValueError("The playbook contains no plays.")

        # Get the first play (assuming single play for simplicity)
        play = playbook_data[0]

        # Ensure the play has a 'vars' key
        if "vars" not in play:
            play["vars"] = {}

        # Update the 'files_to_copy' in 'vars' as a list of dictionaries
        play["vars"]["files_to_copy"] = files_to_copy

        # Write the updated playbook back to the file
        with open(playbook_path, "w") as playbook_file:
            yaml.safe_dump(
                playbook_data, playbook_file, default_flow_style=False, indent=2
            )

        print(f"✅ Playbook updated successfully at {playbook_path}")

    except FileNotFoundError:
        print(f"❌ Playbook file not found: {playbook_path}")
    except yaml.YAMLError as e:
        print(f"❌ YAML error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
