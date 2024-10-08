"""
Author: Oleg Abramov
Copyright 2023
GitHub Link: https://github.com/olabramov-clgx
Website Link: https://abramov.dev
License: MIT
Version: 0.0.1.1
Email: oleg@abramov.dev
Status: Prototype
Filename: sonarqube_api.py
"""

import requests

class SonarQubeAPI:
    def __init__(self, user_token, sonarqube_url):
        self.user_token = user_token
        self.sonarqube_url = sonarqube_url.rstrip('/')
        self.auth = (user_token, '')
        self.headers = {'Content-Type': 'application/json'}

    def projects_search(self, analyzedBefore=None, projects=None, q=None):
        # Implement pagination
        page = 1
        page_size = 200
        components = []

        while True:
            params = {
                'p': page,
                'ps': page_size
            }
            if analyzedBefore:
                params['analyzedBefore'] = analyzedBefore
            if projects:
                params['projects'] = projects
            if q:
                params['q'] = q

            url = f"{self.sonarqube_url}/api/projects/search"
            response = requests.get(url, auth=self.auth, headers=self.headers, params=params)

            if response.status_code != 200:
                print(f"Error: Failed to search projects. Status code: {response.status_code}")
                break

            data = response.json()
            components.extend(data.get('components', []))

            if data['paging']['pageIndex'] * data['paging']['pageSize'] >= data['paging']['total']:
                break

            page += 1

        return components

    def projects_bulk_delete(self, projects):
        url = f"{self.sonarqube_url}/api/projects/bulk_delete"
        data = {'projects': projects}
        response = requests.post(url, auth=self.auth, headers=self.headers, data=data)
        return response

    def projects_delete(self, project):
        url = f"{self.sonarqube_url}/api/projects/delete"
        params = {'project': project}
        response = requests.post(url, auth=self.auth, headers=self.headers, params=params)
        return response
