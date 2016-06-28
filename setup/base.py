import os


PROJECT_BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../'
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

def run_migrations():
    sudo(PROJECT_BASE_PATH + 'manage.py migrate')


setup_virtualenv()
