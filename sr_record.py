import argparse
import os
import re

from bs4 import BeautifulSoup
import requests


sr_ids = [
   # "818.101.24",  # COVID-19 Verordnung 2
   "170.32",
   "172.010",
   "172.220.1",
   "235.1",
   "510.10",
   "510.518",
   "510.91",
   "943.03",
   "120.423",
   "120.4",
   "152.1",
   "172.010.1",
   "172.010.442",
   "172.010.58",
   "172.010.59",
   "172.214.1",
   "172.220.111.31",
   "172.220.111.3",
   "235.11",
   "510.211.2",
   "510.215",
   "510.411",
   "510.411",
   "510.518.1",
   "510.911",
   "514.20",
   "943.032.1",
   "943.032.1",
   "943.032",
]
search_url = "https://www.admin.ch/opc/search/?text={}"
index_url = r"https://www.admin.ch/opc/de/classified-compilation/{}/index.html"
latest_update_string = r"\(Stand am ([^<]*)\)<"
is_active_string = "Dieser Text ist in Kraft"
download_dir = "downloads"


class SrRecord(object):

    def __init__(self, sr_id):
        self.sr_id = sr_id

    def populate(self):
        url = search_url.format(self.sr_id)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.url = r.url
        self.last_updated = self.get_last_update_date(soup)
        self.title = soup.title.string
        self.is_active = self.get_is_active(soup)
        self.pdf_url = self.get_pdf_url(soup)
        self.pdf = ""

    def get_last_update_date(self, soup):
        m = re.findall(latest_update_string, str(soup))
        if m:
            return m[0]
        else:
            return ""

    def get_is_active(self, soup):
        return is_active_string in str(soup)

    def get_pdf_url(self, soup):
        base_url = self.url[:self.url.rfind('/')]
        pdf_url = soup.find_all("a", string="PDF")[0]['href']
        return base_url + "/" + pdf_url

    def download_pdf(self, download_dir):
        pdf_file = requests.get(self.pdf_url)
        if pdf_file:
            file_name = f"{download_dir}/{self.title}.pdf"
            with open(file_name, "wb") as file:
                file.write(pdf_file.content)

    def __str__(self):
        return (
            f"SR record with ID: {self.sr_id}\n"
            f"Last updated on: {self.last_updated}\n"
            f"Title: {self.title}\n"
            f"Active Status: {self.is_active}\n"
        )


def main(args):
    if not args.print_only:
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
    for sr_id in args.sr_ids:
        record = SrRecord(sr_id)
        record.populate()
        print(record)
        if not args.print_only:
            record.download_pdf(args.output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch legal documents from admin.ch classified collection ("Systematische Rechtssammlung").')
    parser.add_argument('sr_ids', metavar='ID', nargs='+',
                        help='IDs of documents to fetch')
    parser.add_argument('-o', '--output_dir', default=download_dir,
            help='where to place the PDF files')
    parser.add_argument('-p', '--print_only',
            help='do not download anything, just print some info')
    args = parser.parse_args()
    main(args)

