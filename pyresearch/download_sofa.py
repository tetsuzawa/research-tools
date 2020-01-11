#!/usr/bin/env python
# encoding: utf-8

import argparse
import pathlib
import requests
import bs4
import urllib.parse

"""
Note that the modules (numpy, maplotlib, wave, scipy) are properly installed on your environment.

Plot wave, spectrum, save them as pdf and png at same directory.

Example:
   python calc_wave_analysis.py IR_test.wav

"""


def main():
    parser = argparse.ArgumentParser(description="This script downloads *.sofa files from designated path.")

    parser.add_argument('url',
                        action='store',
                        nargs=None,
                        const=None,
                        default=None,
                        type=str,
                        help='The URL where the sofa file is located.',
                        metavar=None)

    parser.add_argument('-d', '--dst_path',
                        action='store',
                        nargs='?',
                        # const="/Users/tetsu/personal_files/Research/filters/test/img",
                        default=".",
                        # default=None,
                        type=str,
                        help='Directory path where you want to locate sofa files. (default: current directory)',
                        metavar=None)

    args = parser.parse_args()
    url = args.url
    out_dir = pathlib.Path(args.dst_path)

    is_success = scrape(url, out_dir)

    if is_success:
        print("\ndownloaded files have saved at: ", out_dir, "\n")
        print("Success!")
    else:
        print("Failed!")


def scrape(url, out_dir):
    # obtain page contents from url
    try:
        res_get = requests.get(url)
        res_get.raise_for_status()
        soup = bs4.BeautifulSoup(res_get.content, "lxml")
    except Exception as e:
        print(e)
        return False

    # download sofa files
    try:
        sofa_list = []
        links = soup.find_all("a")
        for link in links:
            if link.get("href").endswith(".sofa"):
                sofa_list.append(link.get("href"))

        for target in sofa_list:
            print(target)
            req = requests.get(urllib.parse.urljoin(url, target))
            out_path = pathlib.Path.joinpath(out_dir, target.split('/')[-1])
            with open(str(out_path), 'wb') as f:
                f.write(req.content)
    except Exception as e:
        print(e)
        return False

    return True


# %%
if __name__ == '__main__':
    main()
