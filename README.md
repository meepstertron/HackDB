![](https://hackatime-badge.hackclub.com/U087PR1B2HX/HackDB) ![Python](https://img.shields.io/badge/Built%20with-python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

# HackDB
HackDB is a simple to use and easy database tool for hackclubbers and more. it bases on postgres and opens it through a webui and sdks plus a cli app

## ! Disclaimer !
AI (Artificial inteligence) has been used in this repo and its code (copilot, gemma3.1). I try to minimze its use and reduce internet slop, for more questions please reach out to me over the contact data provided in the footer :)

## How to get started
> Currently the project is only open to hackclub members </3 but that might change in the future

### WebApp
1. Head to https://hackdb.hexagonical.ch and log in using slack. 
2. Click on the database tab>new and give it a name
3. then you will be taken to a db overview page click on open in editor
4. there will be a simple table already provided for you feel free to delete it or train to get a hang of the ui

### SDKs

---
**Python**
1. Go to your dash and navigate to the tokens page
2. click on new token
3. copy it
4. install the package (if on PiPy yet?) `pip install hackdb`
5. create a simple file like so:
```python
    from python.hackdb import HackDB

    hackdb = HackDB(token="hkdb_tkn_0dff8dfe-****-****-****-3d122da57226")


    print(hackdb)
    print(hackdb.get_tables())
```
6. replace with your token
> Warning: tokens are per database so this will list all tables in that database. global tokens comming in the future <3

### CLI

1. Install using pip: `pip install hackdb-cli`
2. Login `hackdb login`
3. select login method (i recomend slack)
4. `hackdb status` get status of instance and verify if working

Availible commands:
- `hackdb status` - gets the status of the instance
- `hackdb databases` - returns a list of your databases and their ids
- `hackdb drop <database id>` - irreversibely drops a database
- `hackdb table list -d <database name>`
- `hackdb table ` 
