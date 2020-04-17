import argparse
import logging
import os
import re

from bs4 import BeautifulSoup
import requests
import yaml

search_url = "https://www.admin.ch/opc/search/?text={}"
latest_update_string = r"\(Stand am ([^<]*)\)<"
is_active_string = "Dieser Text ist in Kraft"
download_dir = "downloads"
logger = logging.getLogger("root")
csv_logger = logging.getLogger("csv_logger")


def setup_logging():
    import logging.config
    with open('log_conf.yaml') as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
        logging.config.dictConfig(conf)


class SrRecord(object):
    """A legal document from admin.ch classified collection.

    May be a federal law, directive or other regulation.
    SR is short for "Systemematische Rechtssammlung".
    """

    def __init__(self, sr_id):
        self.sr_id = sr_id

    def populate(self):
        url = search_url.format(self.sr_id)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.url = r.url
        self.last_update = self.get_last_update_date(soup)
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

    @staticmethod
    def get_csv_header():
        return (
            "ID; "
            "Title (German); "
            "Last update; "
            "Active status; "
            "URL"
            )

    def to_csv(self):
        return (
            f"{self.sr_id}; "
            f"{self.title}; "
            f"{self.last_update}; "
            f"{self.is_active}; "
            f"{self.url}"
            )

    def __str__(self):
        return (
            f"SR record with ID: {self.sr_id}\n"
            f"Last updated on: {self.last_update}\n"
            f"Title: {self.title}\n"
            f"Active Status: {self.is_active}\n"
        )


def keep_unique_only(id_list):
    return list(set(id_list))


def main(args):

    setup_logging()

    if not args.print_only:
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)

    records = []
    sr_ids = keep_unique_only(args.sr_ids)
    for sr_id in sr_ids:
        record = SrRecord(sr_id)
        record.populate()
        records.append(record)
        logger.info(record)

    csv_logger.info(SrRecord.get_csv_header())
    for record in records:
        csv_logger.info(record.to_csv())

    if args.print_only:
        logger.info("Skipping downloads.")
    else:
        logger.info(f"Downloading PDFs into {args.output_dir} ...")
        for record in records:
            record.download_pdf(args.output_dir)
        logger.info("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch legal documents from admin.ch classified collection ("Systematische Rechtssammlung").')
    parser.add_argument('sr_ids', metavar='ID', nargs='+',
                        help='IDs of documents to fetch')
    parser.add_argument('-o', '--output_dir', default=download_dir,
            help='where to place the PDF files')
    parser.add_argument('-p', '--print_only', action='store_true',
            help='do not download anything, just print some info')
    args = parser.parse_args()
    main(args)

