import os
import contextlib

from invoke import run, task, util


@task
def deploy_docs():
    """
    Based on https://gist.github.com/domenic/ec8b0fc8ab45f39403dd
    """
    run('rm -rf ./site/')
    run('mkdocs build')
    with util.cd('./site/'):
        run('git init')
        run('echo ".*pyc" > .gitignore')
        run('git config user.name "Travis CI"')
        run('git config user.email "%s"' % os.environ['EMAIL'])
        run('git add .')
        run('git commit -m "Deploy to GitHub Pages"')
        run(
            'git push --force --quiet "https://{GH_TOKEN}@{GH_REF}" master:gh-pages > /dev/null 2>&1'.format(
                GH_TOKEN=os.environ['GH_TOKEN'],
                GH_REF=os.environ['GH_REF'],
            )
        )
