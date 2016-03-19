import os

from invoke import run, task, util


API_REFERENCE_CONFIG = {
    'client': ['auth'],
    'session_client': [
        'user',
        'projects',
        'project',
        'use_project'
    ],
    'project_client': [
        'info',
        'collections',
        'collection',
        'documents',
        'document',
    ]
}


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
            'git push --force --quiet "https://{GH_TOKEN}@{GH_REF}" '
            'master:gh-pages > /dev/null 2>&1'.format(
                GH_TOKEN=os.environ['GH_TOKEN'],
                GH_REF=os.environ['GH_REF'],
            )
        )


@task(name='generate-api-reference')
def generate_api_reference():
    pass
    # config = {
    #     'host': os.environ['DEFORM_HOST'],
    #     'secure': os.environ['DEFORM_SECURE']
    # }
    #
    # from pydeform import Client
    # client = Client(
    #     host=config['host'],
    #     secure=config['secure']
    # )
    # session_client = client.auth('session', 'noop')
    # project_client = session_client.use_project('noop')
    # print session_client.user.get.__doc__


@task(name='serve-docs')
def serve_docs():
    run('mkdocs serve')
