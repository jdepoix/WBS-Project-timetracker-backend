import os


VIRTUAL_ENV_PATH = '../virtualenv'
REQUIREMENTS_PATH = '../requirements'

def execute(command):
    os.system(command)

def sudo(command):
    execute('sudo ' + command)

def setup_virtualenv():
    sudo('virtualenv ' + VIRTUAL_ENV_PATH)

def install_requirements(filename):
    sudo(VIRTUAL_ENV_PATH + '/bin/pip install -r ' + REQUIREMENTS_PATH + '/' + filename)


setup_virtualenv()
