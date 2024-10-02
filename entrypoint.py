#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import asyncio
import signal
from ruamel.yaml import YAML

yaml = YAML()

async def main():
    processes = []

    # Function to ensure directories exist
    def ensure_directory_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory {path}")

    # Function to write configuration files
    def write_config(env_var, file_path, default_config=None):
        config_str = os.getenv(env_var)
        if config_str:
            try:
                config = json.loads(config_str)
            except json.JSONDecodeError as e:
                print(f"Error parsing {env_var}: {e}")
                sys.exit(1)
        elif default_config is not None:
            config = default_config
        else:
            return  # Skip writing if no config is provided
        # Ensure the directory exists
        ensure_directory_exists(os.path.dirname(file_path))
        # Write the configuration to file in YAML format
        with open(file_path, 'w') as f:
            yaml.dump(config, f)
            print(f"Wrote configuration to {file_path}")

    # Write master configuration
    default_master_config = {
        "auto_accept": True,
        "file_roots": {
            "base": ["/srv/salt"]
        },
        "pillar_roots": {
            "base": ["/srv/pillar"]
        }
    }
    write_config(
        env_var='SALT_MASTER_CONFIG',
        file_path='/etc/salt/master.d/master.conf',
        default_config=default_master_config
    )

    # Write minion configuration
    default_minion_config = {
        "master": "localhost",
        "id": "minion"
    }
    write_config(
        env_var='SALT_MINION_CONFIG',
        file_path='/etc/salt/minion.d/minion.conf',
        default_config=default_minion_config
    )

    # Ensure 'user' is set to 'salt' in master configuration
    with open("/etc/salt/master.d/user.conf", "w") as userfile:
        userfile.write("user: salt\n")

    # Start salt-master
    processes.append(await asyncio.create_subprocess_exec("salt-master", "-l", "info"))

    # Start salt-minion
    processes.append(await asyncio.create_subprocess_exec("salt-minion", "-l", "info"))

    # Wait for all processes to complete
    await asyncio.gather(*[proc.wait() for proc in processes])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for signame in {"SIGINT", "SIGTERM"}:
        loop.add_signal_handler(getattr(signal, signame), loop.stop)

    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
