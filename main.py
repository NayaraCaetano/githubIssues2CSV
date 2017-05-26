# -*- coding: utf-8 -*-

import requests
import json
import csv
import local_settings

from datetime import datetime


BASE_URL = 'https://api.github.com/search/issues'
AUTENTICATED_URL = BASE_URL + '?access_token=' + local_settings.OAUTH_TOKEN


def main():
    params_defautl = '&per_page=100' + local_settings.Q_PARAM

    result = []
    for repo in local_settings.REPOS:
        result += get_issues(AUTENTICATED_URL + params_defautl + '%20repo:' + repo, repo)

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


def dict_to_csv(somedict, csv_file):
    with open(csv_file, 'wb') as f:
        w = csv.writer(f)
        w.writerow(somedict[0].keys())

        for line in somedict:
            w.writerow(line.values())


main()