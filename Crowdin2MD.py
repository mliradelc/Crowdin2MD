# Copyright (c) 2019 Maximiliano Lira Del Canto
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# Crowdin Top members list to Markdown script.
# This script calls Markdown API to generate a list of top translators
# then, converts the list to markdown and save it on a desired file
#
#Aknowlegments:
# Lev Zakharov (https://github.com/lzakharov) for the csv2md code
# Crowdin for the Translation platform
#
# Usage: $ Crowdin2MD.py Pidentifier Pkey -o [file]

import argparse
import csv
import io
import json
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Retrieve the translators list from a Crowdin project and create a Markdown file')
parser.add_argument('Pidentifier', type=str,
                        help='The project identifier name from Crowdin')
parser.add_argument('Pkey', type=str,
                        help='The API project key to get the data from the project')
parser.add_argument('-o', '--output', metavar='OUTPUTFILE', type=str, default='translators.md',
                        help='Set output file, by default \'translators.md\' ')
args = parser.parse_args()

class Table:
    def __init__(self, cells):
        self.cells = cells
        self.widths = list(map(max, zip(*[list(map(len, row)) for row in cells])))

    def markdown(self, center_aligned_columns=None, right_aligned_columns=None):
        def format_row(row):
            return '| ' + ' | '.join(row) + ' |'

        rows = [format_row([cell.ljust(width) for cell, width in zip(row, self.widths)]) for row in self.cells]
        separators = ['-' * width for width in self.widths]

        if right_aligned_columns is not None:
            for column in right_aligned_columns:
                separators[column] = ('-' * (self.widths[column] - 1)) + ':'
        if center_aligned_columns is not None:
            for column in center_aligned_columns:
                separators[column] = ':' + ('-' * (self.widths[column] - 2)) + ':'

        rows.insert(1, format_row(separators))

        return '\n'.join(rows)

    @staticmethod
    def parse_csv(file, delimiter=',', quotechar='"'):
        return Table(list(csv.reader(file, delimiter=delimiter, quotechar=quotechar)))


url = "https://api.crowdin.com/api/project/" + args.Pidentifier + "/reports/top-members/export"

querystring = {"key": args.Pkey}

payload = {
    "unit" : (None, "words"),
    "format" : (None, "csv")
}

headers = {
    'content-disposition': "form-data",
    'cache-control': "no-cache",
    'Connection':'close'
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

soup = BeautifulSoup(response.text, 'html.parser')

responseHash = soup.hash.text

import requests

url = "https://api.crowdin.com/api/project/"+ args.Pidentifier +"/reports/top-members/download"

querystring = {"key":args.Pkey,"hash":responseHash}

headers = {
    'cache-control': "no-cache",
    'Connection':'close'
    }

csvReport = requests.request("GET", url, headers=headers, params=querystring)
table = Table.parse_csv(io.StringIO(csvReport.content.decode('UTF-8')))

outputSTR = "# Translators\n\nOn this page, we want to say thanks to all the people and organizations who made contributions to the localization of the different languages that Opencast support today.\n\n"
outputSTR = outputSTR + table.markdown()


with open(args.output,'w') as f:
    f.write(outputSTR)
