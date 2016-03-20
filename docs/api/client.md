
## Client

Deform.io python client class.

Parameters:

* `host` - HTTP server host. E.g. `deform.io`.
* `port` - HTTP server port. Default is `None`.
* `secure` - if `True` client will make secure request via `https`.
   Default is `True`.
* `requests_session` - python requests' [Session][requests-session]
   instance. Default is `None`.
* `request_defaults` - python requests' [request][requests-request]
   defaults. Default is `None`.
* `api_base_path` - HTTP server's api uri base path. Default is `/api/`.

Example:

```python
client = Client(host='deform.io')
```

[requests-session]: http://docs.python-requests.org/en/master/user/advanced/#session-objects
[requests-request]: http://docs.python-requests.org/en/master/api/#requests.request


### Client.**auth**()

Creates authenticated client.

Parameters:

* `auth_type` - Authentication type. Use `session` for auth
  by session key. Use `token` for auth by token.
* `auth_key` - Authentication `session key` or `token`.
* `project_id` - Project identifier. Must be provided for
  `token` authentication. Default is `None`.

Returns:

* Instance of [SessionAuthClient](#sessionauthclient) if
  `auth_type` is `session`.
* Instance of [ProjectClient](#projectclient) if
  `auth_type` is `token`

Raises:

* ValueError: if `project_id` parameter was not provided

Examples:

For auth with `session` you should obtain session key by
[Client.user.login](#clientuserlogin) providing
your account's email and password:

```python
client = Client(host='deform.io')
session_client = client.auth(
    'session',
    client.user.login('email@example.com', 'password'),
)
print session_client
<pydeform.client.SessionAuthClient object at 0x10c585650>
```

Authentication with `token` example:

```python
client = Client(host='deform.io')
session_client = client.auth(
  'token',
  auth_key='token-value',
  project_id='some-project',
)
print session_client
<pydeform.client.ProjectClient object at 0x11c585650>
```


### Client.**user**

Non-auth user manipulation object.


### Client.user.**create**()

Creates user.


Parameters:


* `password` - User password (required).
* `email` - User email (required).

### Client.user.**login**()

Login with email and password.

Returns:
    Session id


Parameters:


* `password` - User password (required).
* `email` - User email (required).

### Client.user.**confirm**()

Email confirmation method.

Returns:
    Session id


Parameters:


* `code` - Email confirmation code (required).



## SessionAuthClient

Session auth client.

You should not initalize this client manually.
Use [Client.auth](#clientauth) method with ``session`` authentication.


### SessionAuthClient.**use_project**()

Creates an instance of [ProjectClient](#projectclient),
providing session authentication.

Parameters:

* `project_id` - project identifier.

Returns:

Instance of [ProjectClient](#projectclient) with
session authentication.

Example:

```python
client = Client('deform.io')
session_client = client.auth(
    'session',
    client.user.login('email@example.com', 'password')
)
session_client.use_project('some-project-id')
```


### SessionAuthClient.**project**

One project manipulation object


### SessionAuthClient.project.**create**()




Parameters:


* `data` - Data (required).
* `property` - Work with specified property.

### SessionAuthClient.project.**save**()




Parameters:


* `data` - Data (required).
* `property` - Work with specified property.
* `identity` - Identity.

### SessionAuthClient.project.**get**()




Parameters:


* `identity` - Identity (required).
* `property` - Work with specified property.

### SessionAuthClient.**projects**

Many projects manipulation object


### SessionAuthClient.projects.**count**()




Parameters:


* `filter` - Filter query.
* `text` - Full text search value.

### SessionAuthClient.projects.**find**()




Parameters:


* `filter` - Filter query.
* `text` - Full text search value.
* `per_page` - None.
* `page` - None.
* `sort` - None.

### SessionAuthClient.**user**

Authenticated by session user manipulation object


### SessionAuthClient.user.**logout**()




### SessionAuthClient.user.**update**()




Parameters:


* `data` - Data (required).

### SessionAuthClient.user.**get**()






## ProjectClient

Project client.

You should not initalize this client manually.
Use [Client.auth](#clientauth) method with ``token`` authentication or
[SessionAuthClient.use_project](#sessionauthclientuse_project) method.




### ProjectClient.**collection**

One collection manupulation object


### ProjectClient.collection.**create**()




Parameters:


* `data` - Data (required).
* `property` - Work with specified property.

### ProjectClient.collection.**save**()




Parameters:


* `data` - Data (required).
* `property` - Work with specified property.
* `identity` - Identity.

### ProjectClient.collection.**update**()




Parameters:


* `data` - Data (required).
* `identity` - Identity (required).
* `property` - Work with specified property.

### ProjectClient.collection.**remove**()




Parameters:


* `identity` - Identity (required).
* `property` - Work with specified property.

### ProjectClient.collection.**get**()




Parameters:


* `identity` - Identity (required).
* `property` - Work with specified property.

### ProjectClient.**collections**

Many collections manupulation object


### ProjectClient.collections.**count**()




Parameters:


* `filter` - Filter query.
* `text` - Full text search value.

### ProjectClient.collections.**find**()




Parameters:


* `filter` - Filter query.
* `text` - Full text search value.
* `per_page` - None.
* `page` - None.
* `sort` - None.

### ProjectClient.**document**

One document manupulation object


### ProjectClient.document.**get**()




Parameters:


* `collection` - Collection (required).
* `identity` - Identity (required).
* `fields` - Return specified fields only.
* `property` - Work with specified property.
* `fields_exclude` - Return all but the excluded field.

### ProjectClient.document.**create**()




Parameters:


* `data` - Data (required).
* `collection` - Collection (required).
* `fields` - Return specified fields only.
* `property` - Work with specified property.
* `fields_exclude` - Return all but the excluded field.

### ProjectClient.document.**update**()




Parameters:


* `collection` - Collection (required).
* `data` - Data (required).
* `identity` - Identity (required).
* `fields` - Return specified fields only.
* `fields_exclude` - Return all but the excluded field.
* `property` - Work with specified property.

### ProjectClient.document.**remove**()




Parameters:


* `collection` - Collection (required).
* `identity` - Identity (required).
* `fields` - Return specified fields only.
* `property` - Work with specified property.
* `fields_exclude` - Return all but the excluded field.

### ProjectClient.document.**save**()




Parameters:


* `collection` - Collection (required).
* `data` - Data (required).
* `fields` - Return specified fields only.
* `fields_exclude` - Return all but the excluded field.
* `property` - Work with specified property.
* `identity` - Identity.

### ProjectClient.document.**get_file**()




Parameters:


* `collection` - Collection (required).
* `identity` - Identity (required).
* `fields` - Return specified fields only.
* `property` - Work with specified property.
* `fields_exclude` - Return all but the excluded field.

### ProjectClient.**documents**

Many documents manupulation object


### ProjectClient.documents.**count**()




Parameters:


* `collection` - Collection (required).
* `filter` - Filter query.
* `text` - Full text search value.
* `fields_exclude` - Return all but the excluded field.
* `fields` - Return specified fields only.

### ProjectClient.documents.**update**()




Parameters:


* `operation` - Update operation (required).
* `collection` - Collection (required).
* `filter` - Filter query.
* `fields` - Return specified fields only.
* `fields_exclude` - Return all but the excluded field.

### ProjectClient.documents.**find**()




Parameters:


* `collection` - Collection (required).
* `sort` - None.
* `text` - Full text search value.
* `fields_exclude` - Return all but the excluded field.
* `filter` - Filter query.
* `fields` - Return specified fields only.
* `per_page` - None.
* `page` - None.

### ProjectClient.documents.**remove**()




Parameters:


* `collection` - Collection (required).
* `filter` - Filter query.
* `fields` - Return specified fields only.
* `fields_exclude` - Return all but the excluded field.

### ProjectClient.documents.**upsert**()




Parameters:


* `operation` - Update operation (required).
* `collection` - Collection (required).
* `filter` - Filter query.
* `fields` - Return specified fields only.
* `fields_exclude` - Return all but the excluded field.

### ProjectClient.**info**

Current project manupulation object


### ProjectClient.info.**get**()





