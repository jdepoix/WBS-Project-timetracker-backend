import os


PROJECT_BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
VIRTUAL_ENV_PATH = PROJECT_BASE_PATH + '/virtualenv'
REQUIREMENTS_PATH = PROJECT_BASE_PATH + '/requirements'


def execute(command):
    os.system(command)

def sudo(command):
    execute('sudo ' + command)

def setup_virtualenv():
    sudo('pip install virtualenv')
    sudo('virtualenv ' + VIRTUAL_ENV_PATH)

def install_requirements(filename):
    sudo(VIRTUAL_ENV_PATH + '/bin/pip install -r ' + REQUIREMENTS_PATH + '/' + filename)

def run_virtualenv_python(python_file_path):
    sudo(VIRTUAL_ENV_PATH + '/bin/python ' + python_file_path)

def run_manage_command(command):
    run_virtualenv_python(PROJECT_BASE_PATH + 'manage.py ' + command)

def run_migrations():
    run_manage_command('migrate')

def collect_static():
    run_manage_command('collectstatic --noinput')

def run_legacy_migrations():
    run_virtualenv_python(PROJECT_BASE_PATH + '/setup/utils/legacy_migration_manager.py')

def setup(requirements_filename):
    setup_virtualenv()
    install_requirements(requirements_filename)
    collect_static()
    run_legacy_migrations()
    run_migrations()
