import dataset

## NOTE: Creation of the database is no threadsafe

_db = []


def get_db(uri=''):

    if not _db:
        d = dataset.connect(uri)
        _db.append(d)
        return d
    else:
        return _db[0]

