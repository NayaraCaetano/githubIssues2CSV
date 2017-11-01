# -*- coding: utf-8 -*-

import requests
import json
import csv
import local_settings

from datetime import datetime


BASE_URL = 'https://api.github.com/search/issues'


def main():
    params_defautl = '&per_page=100&sort=updated&order=asc' + local_settings.Q_PARAM

    result = []
    for repo in local_settings.REPOS:
        result += get_issues(
            authenticated_url(repo['oauth_token']) + params_defautl + '%20repo:' + repo['repo'],
            repo['repo']
        )

    print(str(len(result)) + ' issues imported')

    dict_to_csv(result, 'issues.csv')


def get_issues(url, projeto):
    print(url)
    content = json.loads(requests.get(url).content)['items']
    list_return = []
    for item in content:
        if item['assignee']:
            result = {
                'projeto': projeto,
                'numero': item['number'],
                'data fechamento': str(datetime.strptime(item['closed_at'], '%Y-%m-%dT%H:%M:%SZ')),
                'responsavel': item['assignee']['login'],
                'url': item['html_url']
            }
            print(result)
            list_return.append(result)

    return list_return


def dict_to_csv(some_dict, csv_file):
    with open(csv_file, 'wb') as f:
        w = csv.writer(f)
        w.writerow(some_dict[0].keys())

        for line in some_dict:
            w.writerow(line.values())


def authenticated_url(token):
    return BASE_URL + '?access_token=' + token

main()
