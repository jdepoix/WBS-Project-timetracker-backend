import os
import json

import MySQLdb


class LegacyMigrationRunner(object):
    """
    applies a migration to the given database connetion
    """
    def __init__(self, connection, sql):
        """
        :param connection: connection to the database this migration should be applied to
        :param sql: the sql to apply
        """
        self.connection = connection
        self.sql = sql

    def migrate(self):
        """
        runs the migration
        """
        self.connection.cursor().execute(self.sql)


class LegacyMigrationManager(object):
    """
    manages running the legacy migrations
    """
    def __init__(self, legacy_migrations_dir_path, conf_json_path):
        """
        :param legacy_migrations_dir_path: path to the dir containing the legacy migration files
        :param conf_json_path: path to the json conf containing the database information
        """
        self.legacy_migrations_dir_path = legacy_migrations_dir_path
        self.conf = json.load(open(conf_json_path))
        self.connection = None

    def run_legacy_migrations(self):
        """
        runs all mirations
        """
        self.connect_db()

        for migration in self.collect_legacy_migrations():
            LegacyMigrationRunner(self.connection, migration).migrate()

        self.disconnect_db()

    def collect_legacy_migrations(self):
        """
        collects all migrations from the legacy migrations directory

        :return: list with all migrations
        :rtype: list
        """
        migration_files = [
            self.legacy_migrations_dir_path + '/' + migration_file
                for migration_file in os.listdir(self.legacy_migrations_dir_path)
                    if migration_file.endswith('.sql')
        ]

        migration_files.sort()

        migrations = []

        for migration_file in migration_files:
            with open(migration_file) as migration_file_handler:
                migrations.append(migration_file_handler.read())

        return migrations

    def connect_db(self):
        """
        connects to the database specified in the conf.json
        """
        if self.connection:
            self.disconnect_db()

        self.connection = MySQLdb.connect(
            self.conf.get('database').get('host'),
            self.conf.get('database').get('user'),
            self.conf.get('database').get('password'),
        )

    def disconnect_db(self):
        """
        disconnects the database
        """
        if self.connection:
            self.connection.close()
            self.connection = None


if __name__ == '__main__':
    project_base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    LegacyMigrationManager(
        project_base_path + '/setup/legacy_migrations',
        project_base_path + '/conf.json'
    ).run_legacy_migrations()
