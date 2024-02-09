#!/usr/bin/env python
import os
import click
from flask import Flask

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app

app = create_app()

@app.cli.command()
@click.option('--coverage', is_flag=True, help='Run tests under code coverage.')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    else:
        # Ensure this block does not run again if restarted for coverage
        time.sleep(1)
        import unittest
        import xmlrunner
        tests = unittest.TestLoader().discover('tests')
        # run tests with unittest-xml-reporting and output to test-reports locally
        xmlrunner.XMLTestRunner(output=os.environ.get('CIRCLE_TEST_REPORTS', 'test-reports')).run(tests)
        if COV:
            COV.stop()
            COV.save()
            print('Coverage Summary:')
            COV.report()
            basedir = os.path.abspath(os.path.dirname(__file__))
            covdir = os.path.join(basedir, 'tmp/coverage')
            COV.html_report(directory=covdir)
            print('HTML version: file://%s/index.html' % covdir)
            COV.erase()

if __name__ == '__main__':
    app.run()
