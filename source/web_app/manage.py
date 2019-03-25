#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import subprocess

from MediaKraken.app import create_app
from MediaKraken.database import db
from MediaKraken.settings import ProdConfig
from MediaKraken.user.models import User
from flask_script import Manager, Shell, Server
from flask_script.commands import Clean, ShowUrls

app = create_app(ProdConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())

if __name__ == '__main__':
    wait_pid = subprocess.Popen(['/poe/wait-for-it-ash.sh', '-h',
                                 'poerabbitmq', '-p', ' 5672', '-t', '30'],
                                shell=False)
    wait_pid.wait()
    manager.run()
