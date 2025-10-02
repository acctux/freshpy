import ansible_runner
from pathlib import Path


def run_ansible_playbook(playbook_path: Path, files_to_yaml: dict[str, str]):
    # playbook_path = '/home/nick/Lit/dotfiles/playbook.yml'
    runner = ansible_runner.run(
        playbook=playbook_path,
        extravars={"files_to_copy": files_to_yaml},  # Pass the variable here
    )

    if runner.rc == 0:
        print("Playbook executed successfully!")
    else:
        print(f"Playbook failed with return code {runner.rc}")
