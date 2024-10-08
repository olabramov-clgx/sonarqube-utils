# MX SonarQube Utils

SonarQube Utilities.

## Features

- Search for projects
- Delete projects
- Bulk delete projects
- Supports dry run mode
- Configurable via environment variables, command-line arguments, or configuration files

## Requirements

- Python 3.x
- `requests` library (install via `pip install requests`)

## Installation

Clone the repository and install the required packages:
	
	git clone https://github.com/olabramov-clgx/sonarqube-utils.git
	cd sonarqube-utils
	pip install -r requirements.txt

##Configuration

Configuration can be provided via:

* Environment variables `SQ_USER_TOKEN` and `SQ_URL`
* Command-line arguments
* Configuration file `conf/secrets.ini`

Sample `secrets.ini` file:

	[SONARQUBE]
	user_token = your_user_token_here
	sonarqube_url = https://your-sonarqube-instance.com

##Usage
Run the script with the desired action(s):

	python mx_sonarqube_utils/main.py --action search --q "My Project"

Available actions:

* `search` - Search projects
* `delete` - Delete a project
* `bulk_delete` - Bulk delete projects

Parameters:

* `--user_token` - SonarQube user token (required if not set via environment or config)
* `--sonarqube_url` - SonarQube URL (required if not set via environment or config)
* `--action` - Action(s) to perform, comma-separated (required)
* `--project` - Project key (required for delete action)
* `--projects` - Project keys, comma-separated
* `--analyzedBefore` - Filter projects not analyzed since a given date (YYYY-MM-DD)
* `--q` - Search query
* `--dryRun` - If true, do not perform delete operations

Examples:

Search projects:
	`python mx_sonarqube_utils/main.py --action search --q "My Project"`
	
Delete a project:
	`python mx_sonarqube_utils/main.py --action delete --project my_project_key`

Bulk delete projects analyzed before a specific date (dry run):
	`python mx_sonarqube_utils/main.py --action bulk_delete --analyzedBefore 2023-01-01 --dryRun`

Bulk delete projects:
	`python mx_sonarqube_utils/main.py --action bulk_delete --projects project_key1,project_key2`

##License
MIT License

##Author
Oleg Abramov

* GitHub: [https://github.com/olabramov-clgx](https://github.com/olabramov-clgx)
* Website: [https://abramov.dev](https://abramov.dev)


## Notes

- The utility supports multiple actions, accepts parameters via command-line arguments, environment variables, or configuration files, and handles actions sequentially if multiple are specified.
- The `dryRun` parameter allows you to preview the actions without making changes to the SonarQube server.
- The `projects_search` function handles pagination to ensure all results are retrieved.

---

Please make sure to update the `user_token` and `sonarqube_url` in your `secrets.ini` file or set them via environment variables or command-line arguments before running the utility.
