from django.db import connections


class DbLoader(object):
    """
    this class handles dynamically adding databases during runtime
    """
    def __init__(self, *db_configs):
        """
        takes a list of db config dicts you want to add to the runtime environment

        :param db_configs: list of db config
        :type db_configs: list<dict>
        """
        self.db_configs = db_configs

    def _load_db(self, db_config):
        """
        adds a single database to the runtime enviroment

        :param db_config: the config for the database
        :type db_config: dict
        """
        connections.databases.update(db_config)

    def load_dbs(self):
        """
        adds the databases to the runtime enviroment
        """
        [self._load_db(db_config) for db_config in self.db_configs]
