# SaltMaster Docker Container

This project provides a Dockerized SaltMaster that can be dynamically configured using environment variables. The container is based on Python and Alpine Linux, with SaltStack and GitFS support enabled. You can provide configuration via JSON through environment variables, allowing for dynamic and flexible setups.

## Features

- SaltStack 3007.0 installed with pygit2 for GitFS support.
- Automatically configures SaltMaster and SaltMinion using environment variables.
- Uses `ruamel.yaml` for YAML configuration file generation.
- Built on Alpine Linux for a small footprint.

## Prerequisites

- Docker installed on your system.

## Build the Docker Image

Clone this repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/saltmaster-docker.git
cd saltmaster-docker
```

Build the Docker image:

```bash
docker build -t saltmaster:latest .
```

## Running the Container with Minimal Configuration

You can run the SaltMaster container with minimal configuration by passing a few basic environment variables.

### Example 

```bash
docker run -d --name saltmaster -p 4505:4505 -p 4506:4506 \
-e "SALT_MASTER_CONFIG={\"auto_accept\": true}" \
-e "SALT_MINION_CONFIG={\"master\": \"saltmaster.local\", \"id\": \"minion\"}" \
saltmaster:latest
```

## Explanation:

- **SALT_MASTER_CONFIG**: Provides basic SaltMaster settings (e.g., `auto_accept` is set to `true`).
- **SALT_MINION_CONFIG**: Configures SaltMinion to connect to the master (in this case, `saltmaster.local` with an ID of `minion`).

The container will expose the required SaltStack ports:

- `4505` for the event publisher (used by Salt Minions to listen for commands).
- `4506` for Salt Master request and worker communication.

## Advanced Configuration with GitFS and Pillars

For more advanced setups, you can use `pygit2` to enable GitFS for the SaltMaster. This allows the SaltMaster to pull its state files from a remote Git repository.

```bash
docker run -d --name saltmaster -p 4505:4505 -p 4506:4506 \
-e "SALT_MASTER_CONFIG={\"auto_accept\": true, \"log_level\": \"info\", \"file_roots\": {\"base\": [\"/srv/salt\"]}, \"fileserver_backend\": [\"gitfs\"], \"gitfs_remotes\": [\"http://gituser:gitpassword@your-git-server.com/repo.git\"], \"gitfs_provider\": \"pygit2\", \"top_file_merging_strategy\": \"same\", \"gitfs_base\": \"main\", \"gitfs_root\": \"states\"}" \
-e "SALT_MINION_CONFIG={\"master\": \"saltmaster.local\", \"id\": \"saltmaster.local\"}" \
saltmaster:latest
```

### Explanation:

- **GitFS Configuration**: The `gitfs_remotes` parameter points to a Git repository from which Salt states will be fetched. The `gitfs_provider` is set to `pygit2` to use this library for Git operations.
- **SALT_MINION_CONFIG**: This remains the same as in the minimal configuration but can be adjusted according to your needs.

## Environment Variables

- **SALT_MASTER_CONFIG**: A JSON object that configures the SaltMaster. This can include settings like `auto_accept`, `log_level`, `file_roots`, `pillar_roots`, and more. For advanced setups, GitFS support can be enabled with `fileserver_backend`, `gitfs_remotes`, `gitfs_provider`, and other Git-related settings.
- **SALT_MINION_CONFIG**: A JSON object that configures the SaltMinion. It must contain the `master` to which the minion connects and the minion `id`.

## Example Configurations

### Minimal Configuration Example:

```json
{
  "auto_accept": true
}
```

### Advanced GitFS Configuration Example:

```json
{
  "auto_accept": true,
  "log_level": "info",
  "file_roots": {
    "base": ["/srv/salt"]
  },
  "fileserver_backend": ["gitfs"],
  "gitfs_remotes": ["http://gituser:gitpassword@your-git-server.com/repo.git"],
  "gitfs_provider": "pygit2",
  "top_file_merging_strategy": "same",
  "gitfs_base": "main",
  "gitfs_root": "states"
}
```

### Minion Configuration Example:

```json
{
  "master": "saltmaster.local",
  "id": "minion"
}
```

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## How to Use:

1. **Basic setup**:
   - The example shows how to run the container with minimal configuration (`auto_accept` and basic minion setup).
   
2. **Advanced GitFS setup**:
   - To use advanced features like GitFS, modify the JSON object passed in the `SALT_MASTER_CONFIG` environment variable to include the necessary GitFS settings.
