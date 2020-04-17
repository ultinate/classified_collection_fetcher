# Goal

Fetch information about legal documents from [https://www.admin.ch/gov/de/start/bundesrecht/systematische-sammlung.html](admin.ch classified collection).

Provides some sort of "API for the poor". Works by parsing HTML pages.

Partly inspired by <https://github.com/syzer/sbb-blog-legal-hack-2017>.


# Installation

You need Python 3 installed locally. The following instructions apply for Linux.For other OSes, adjust to taste (e.g. `./env/Script/activate` on Windows instead of `source env/bin/activate`).

```
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python sr_record.py -h
```


# Usage examples

Retrieve a document (e.g. "COVID-19 Verordnung 2"):

```
python sr_record.py 818.101.24
```

Retrieve info about a list of documents, but don't download the PDFs.
```
cat ids.txt | xargs python sr_record.py --print_only
```


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

