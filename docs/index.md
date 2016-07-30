<h1>Deform.io python client Documentation</h1>

[Deform.io](https://deform.io/) is a simple database as a service.
This documentation contains all the information you need
to get started using Deform with Python. You can find Deform's
general documentation [here](http://deformio.github.io/docs/).

[Source repository on Github](https://github.com/deformio/python-deform).

Start by installing python client from pip:

```
$ pip install python-deform
```

Let's use the client:

```python
from pydeform import Client

client = Client().auth('token', '<token>', '<project_id>')

# get collections
client.collections.find()

# get documents in collection
client.documents.find(collection='venues')
```
