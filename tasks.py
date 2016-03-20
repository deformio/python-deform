import os
from multiprocessing import Process

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


@task(name='serve-docs')
def autobuild_docs():
    generate_api_reference()

    target_cmd = (
        'watchmedo shell-command -R -c '
        '"invoke generate-api-reference" pydeform docs'
    )
    p = Process(target=run, args=(target_cmd,))
    p.daemon = True
    p.start()

    run('mkdocs serve')


@task(name='generate-api-reference')
def generate_api_reference():
    from docs.generator import generate_api_reference
    print 'Generating API reference'
    generate_api_reference()


# @task(name='serve-docs')
# def serve_docs():
#     run('mkdocs serve')
