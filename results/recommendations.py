# -*- coding: utf-8 -*-

import os
from glob import glob
import urllib
import re
from frequency_response import FrequencyResponse

RESULTS_DIR = os.path.abspath(os.path.join(__file__, os.pardir))


def form_url(rel_path):
    url = '/'.join(FrequencyResponse._split_path(rel_path))
    url = 'https://github.com/jaakkopasanen/AutoEq/tree/master/results/{}'.format(url)
    url = urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
    return url


def get_urls(files):
    urls = dict()
    skipped = dict()
    for path in files:
        rel_path = os.path.relpath(path, RESULTS_DIR)
        model = os.path.split(rel_path)[-1]
        if re.search(' sample [a-zA-Z0-9]$', model) or re.search(' sn[a-zA-Z0-9]+$', model):
            # Skip measurements with sample or serial number, those have averaged results
            model = re.sub(' sample [a-zA-Z0-9]$', '', model)
            model = re.sub(' sn[a-zA-Z0-9]+$', '', model)
            try:
                skipped[model].append(rel_path)
            except KeyError as err:
                skipped[model] = [rel_path]
            continue
        urls[model.lower()] = '- [{model}]({url})'.format(model=model, url=form_url(rel_path))

    for model, rel_paths in skipped.items():
        # Add skipped models with only one item, these have no averaged results
        if len(rel_paths) == 1:
            urls[model.lower()] = '- [{model}]({url})'.format(model=model, url=form_url(rel_paths[0]))
    return urls


def main():
    urls = dict()
    # Get links to Headphone.com results
    urls.update(get_urls(glob(os.path.abspath(os.path.join('headphonecom', 'sbaf-serious', '*')))))
    # Get links to Innerfidelity results and override Headphone.com results with the same name
    urls.update(get_urls(glob(os.path.abspath(os.path.join('innerfidelity', 'sbaf-serious', '*')))))
    # Get links to custom results
    urls.update(get_urls(glob(os.path.abspath(os.path.join('custom', '*')))))
    with open('README.md', 'w') as f:
        keys = sorted(urls.keys())
        s = '# Recommended Results\n'
        s += '\n'.join([urls[key] for key in keys])
        f.write(s)


if __name__ == '__main__':
    main()
