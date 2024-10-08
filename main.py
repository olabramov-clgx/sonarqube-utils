"""
Author: Oleg Abramov
Copyright 2023
GitHub Link: https://github.com/olabramov-clgx
Website Link: https://abramov.dev
License: MIT
Version: 0.0.1.2
Email: oleg@abramov.dev
Status: Prototype
Filename: main.py
"""

import os
import sys
import argparse
import configparser
import json
from modules.sonarqube_api import SonarQubeAPI

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='SonarQube Utilities')
    parser.add_argument('--user_token', help='SonarQube user token')
    parser.add_argument('--sonarqube_url', help='SonarQube URL')
    parser.add_argument('--action', help='Action(s) to perform, comma-separated', required=True)
    parser.add_argument('--project', help='Project key')
    parser.add_argument('--projects', help='Project keys, comma-separated')
    parser.add_argument('--analyzedBefore', help='Filter projects not analyzed since a given date (YYYY-MM-DD)')
    parser.add_argument('--q', help='Search query')
    parser.add_argument('--dryRun', help='If true, do not perform delete operations', action='store_true')

    args = parser.parse_args()

    # Load configurations
    config = configparser.ConfigParser()
    secrets_file = os.path.join(os.path.dirname(__file__), 'conf', 'secrets.ini')
    config.read(secrets_file)

    # Get parameters
    user_token = args.user_token or os.getenv('SQ_USER_TOKEN') or config.get('SONARQUBE', 'user_token', fallback=None)
    sonarqube_url = args.sonarqube_url or os.getenv('SQ_URL') or config.get('SONARQUBE', 'sonarqube_url', fallback=None)
    action_list = args.action.split(',')

    if not user_token or not sonarqube_url:
        print("Error: user_token and sonarqube_url are required parameters.")
        sys.exit(1)

    # Initialize API
    sq_api = SonarQubeAPI(user_token=user_token, sonarqube_url=sonarqube_url)RUN

    # Process actions
    for action in action_list:
        if action == 'bulk_delete':
            projects = args.projects
            analyzedBefore = args.analyzedBefore
            q = args.q
            dryRun = args.dryRun

            if not projects and not analyzedBefore and not q:
                print("Error: For bulk_delete, at least one of projects, analyzedBefore, or q must be provided.")
                continue

            if dryRun:
                # Use api/projects/search
                components = sq_api.projects_search(analyzedBefore=analyzedBefore, projects=projects, q=q)
                # Save results to output.json
                with open('output.json', 'w') as f:
                    json.dump(components, f, indent=4)
                # Output to cmd
                for component in components:
                    print(f"{component['name']}:{component['key']}")
            else:
                # Use api/projects/bulk_delete
                if projects:
                    projects_list = projects
                else:
                    # Get list of projects to delete
                    components = sq_api.projects_search(analyzedBefore=analyzedBefore, projects=projects, q=q)
                    projects_list = ','.join([component['key'] for component in components])

                response = sq_api.projects_bulk_delete(projects_list)
                if response.status_code == 204:
                    print("Projects deleted successfully.")
                else:
                    print(f"Failed to delete projects. Status code: {response.status_code}, Response: {response.text}")

        elif action == 'delete':
            project = args.project
            dryRun = args.dryRun

            if not project:
                print("Error: For delete action, 'project' parameter is required.")
                continue

            if dryRun:
                # Use api/projects/search and make project = projects
                components = sq_api.projects_search(projects=project)
                # Save results to output.json
                with open('output.json', 'w') as f:
                    json.dump(components, f, indent=4)
                # Output to cmd
                for component in components:
                    print(f"{component['name']}:{component['key']}")
            else:
                # Use api/projects/delete
                response = sq_api.projects_delete(project)
                if response.status_code == 204:
                    print(f"Project '{project}' deleted successfully.")
                else:
                    print(f"Failed to delete project '{project}'. Status code: {response.status_code}, Response: {response.text}")

        elif action == 'search':
            analyzedBefore = args.analyzedBefore
            projects = args.projects
            q = args.q

            components = sq_api.projects_search(analyzedBefore=analyzedBefore, projects=projects, q=q)
            # Save results to output.json
            with open('output.json', 'w') as f:
                json.dump(components, f, indent=4)
            # Output to cmd
            for component in components:
                print(f"{component['name']}:{component['key']}")
        else:
            print(f"Unknown action: {action}")

if __name__ == '__main__':
    main()
