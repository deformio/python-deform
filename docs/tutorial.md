Initializing client:

```python
from pydeform import Client

deform = Client(
    host='deform.io',
    email='example@email.com',
    password='some-password'
)

deform = Client(
    host='deform.io',
    session_id='some-session-id'
)

deform = Client(
    host='deform.io',
    project='projectid',
    token='some-token'
)
```

Register:

```python
deform = Client(host='deform.io')
deform.register(
    email='example@email.com',
    password='some-password',
)
```

Confirm email:

```python
deform = Client(host='deform.io')
session_id = deform.confirm(
    code='some-confirmation-code',
)
```

Projects (for session authorization):

```python
# getting all projects
deform.projects.find()

# creating a project
deform.project.create('some_project', name='Some project')

# getting a project
deform.project.get('some_project')

# update a project name
deform.project.update('some_project', {'name': 'Project new name'})
```

For token authorization you can use only one project:

```python
# getting a current project
deform.project.get()

# update a project name
deform.project.update({'name': 'Project new name'})
```

Collections:

```python

deform = Client(
    host='deform.io',
    session_id='some-session-id',
    project_id='some_project'
)

# getting all collections (literally all, generator!!!)
deform.collections.find()

# searching for the collections
deform.collections.find({'name': {'$in': ['users', 'venues']}})

# creating a collection
deform.collection.create({'_id': 'users', 'name': 'Users'})  # POST

# saving a collection
deform.collection.save({'_id': 'users', 'name': 'Users'})  # PUT

# saving collection property
deform.collection.save({'type': 'object'}, prop='schema')  # PUT

# update a collection name
deform.collection.update({'name': 'Users'})  # PATCH

# update a collection property
deform.collection.update({'type': 'object'}, prop='schema')  # PATCH

# getting a collection by _id
deform.collection.get('users')

# getting a collection property
deform.collection.get('users', prop='schema')

# removing a collection
project.collection.remove('users')

# removing a collection property
deform.collection.remove('users', prop='schema')
```

Documents create:

```python

deform = Client(
    host='deform.io',
    session_id='some-session-id',
    project_id='some_project'
)

# creating a document
users.document.create(
    {'_id': 'kfc', 'name': 'KFC', 'rating': 10},
    collection='venues'
)  # POST

# saving a document
users.document.save(
    {'_id': 'kfc', 'name': 'KFC', 'rating': 10},
    collection='venues'
)  # PUT
```

Documents retrieve:

```python
# getting all documents
deform.documents.find()

# getting a document by _id
deform.document.get('kfc')

# searching for the documents
deform.documents.find({'rating': 10})

# counting
deform.documents.count()

# or just of those documents that match a specific query:
deform.documents.count({'rating': 10})

# sorting
deform.documents.find({'rating': 10}, sort={'rating': 1})

# limit
deform.documents.find({'rating': 10}, limit=10)

# todo: include/exclude fields
```

Documents update:

```python
# updating a document partial by _id
users.documents('kfc').update({'rating': 1}, partial=True)  # PATCH

# update all documents
users.documents().update({'name': 'KFC', 'rating': 5})  # X-Action: update

# updating documents by query
users.documents({'rating': 10}).update({'name': 'KFC', 'rating': 5})  # X-Action: update

# update all documents partial
users.documents().update({'$set': {'name': 'KFC', 'rating': 5}})  # X-Action: update

# update or insert many documents
users.documents({'rating': 10}).upsert({'name': 'KFC', 'rating': 5})  # X-Action: upsert
```

Documents remove:

```python
# removing a document by _id
users.document.remove('kfc')

# removing all documents
users.documents.remove()  # send {} ?

# removing documents by query
users.documents.remove({'rating': 10})
```
