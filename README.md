# Intended Use

Fetch information about legal documents from [https://www.admin.ch/gov/de/start/bundesrecht/systematische-sammlung.html](Swiss classified collection). A legal document may be a federal law, directive or other regulation.

Provides some sort of "API for the poor". Works by parsing HTML pages.

Naming: SR is short for "Systemematische Rechtssammlung".

Partly inspired by <https://github.com/syzer/sbb-blog-legal-hack-2017>.


# Installation

Prerequisite: Have git, Python 3 installed locally.

```
git clone https://github.com/ultinate/classified_collection_fetcher
cd classified_collection_fetcher
```

```
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python sr_record.py -h
```

These instructions apply for Linux.For other OSes, adjust to taste (e.g. `./env/Script/activate` on Windows instead of `source env/bin/activate`).

# Usage examples

Retrieve a document (e.g. "COVID-19 Verordnung 2"):

```
python sr_record.py 818.101.24
```

Retrieve multiple documents, but don't download the PDFs:

```
python sr_record.py -p 818.101.24 101
```

Retrieve info about a list of documents and specify download folder.
```
cat ids.txt | xargs python sr_record.py --output_dir my_pdfs
```

Retrieve CSV list of documents:

  Have a look at `output.csv` after running above commands.


# License
MIT License, see `LICENSE`.


# Keywords

Keywords (DE): Gesetz, Verordnung, Systematische Rechtssammlung (SR), admin.ch

Keywords (FR): loi, ordonnance, recueil systématique du droit fédéral (RS), admin.ch

Keywords (IT): legge, ordinanza, raccolta sistematica del diritto federale (RS), admin.ch


# TODO

  * Choose language for downloads (currently: PDFs are downloaded in German).
  * Make available as pip package on Pypi.org. Prerequisite: Have a catchy name.
  * Provide history for a record.
  * Provide change list for a record.
  * Monitor changelog (e.g. RSS) for relevant changes.

