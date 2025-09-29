import os
from pathlib import Path
import ansible_runner
from ansible import context
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.parsing.dataloader import DataLoader
from ansible.inventory import Inventory
from ansible.vars.manager import VariableManager
from ansible.plugins.loader import module_loader, action_loader
from ansible.playbook.play import Play
from ansible.playbook.playbook import Playbook


def execute_ansible_task(files_to_copy, marker_file):
    """
    Executes a simple ansible task using Ansible's Python API to copy files
    """
    # Setup Ansible environment
    context.CLIARGS = {
        "connection": "local",
        "inventory": "localhost,",  # No inventory, just localhost
        "module_path": None,
        "forks": 1,
        "become": None,
        "become_method": None,
        "become_user": None,
        "check": False,
        "diff": False,
    }

    # Initialize Ansible components
    loader = DataLoader()
    inventory = Inventory(loader=loader, sources=["localhost,"])
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # Playbook task queue manager
    tqm = None

    try:
        # Define a simple play
        play_source = {
            "name": "Copy Files with Backup",
            "hosts": "localhost",
            "tasks": [
                {
                    "name": "Check if marker file exists",
                    "action": {"module": "stat", "args": {"path": marker_file}},
                },
                {
                    "name": "Copy files if not already done",
                    "block": [
                        {
                            "name": "Ensure destination directories exist",
                            "action": {
                                "module": "file",
                                "args": {
                                    "path": "{{ item.dest | dirname }}",
                                    "state": "directory",
                                    "mode": "0755",
                                    "owner": "root",
                                    "group": "root",
                                },
                            },
                            "loop": files_to_copy,
                        },
                        {
                            "name": "Copy configuration files to destination",
                            "action": {
                                "module": "copy",
                                "args": {
                                    "src": "{{ item.src }}",
                                    "dest": "{{ item.dest }}",
                                    "mode": "0644",
                                    "owner": "root",
                                    "group": "root",
                                    "backup": True,
                                },
                            },
                            "loop": files_to_copy,
                        },
                        {
                            "name": "Create marker file to prevent re-running",
                            "action": {
                                "module": "file",
                                "args": {
                                    "path": marker_file,
                                    "state": "touch",
                                    "mode": "0644",
                                    "owner": "root",
                                    "group": "root",
                                },
                            },
                        },
                    ],
                },
            ],
        }

        # Create a play from the above source
        play = Play().load(
            play_source, variable_manager=variable_manager, loader=loader
        )

        # Execute the play
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=context.CLIARGS,
            passwords={},
        )
        tqm.run(play)

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        if tqm:
            tqm.cleanup()


# Example usage
files_to_copy = [
    {"src": "/path/to/source/file1", "dest": "/path/to/destination/file1"},
    {"src": "/path/to/source/file2", "dest": "/path/to/destination/file2"},
]

marker_file = "/path/to/marker_file"

execute_ansible_task(files_to_copy, marker_file)
