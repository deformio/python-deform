
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


### Client.user.**confirm**()

Email confirmation method.

Returns:
    Session id


Parameters:


* `code` - Email confirmation code (required).

### Client.user.**login**()

Login with email and password.

Returns:
    Session id


Parameters:


* `email` - User email (required).
* `password` - User password (required).

### Client.user.**create**()

Creates user.


Parameters:


* `email` - User email (required).
* `password` - User password (required).



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


### SessionAuthClient.project.**get**()




Parameters:


* `identity` - Identity (required).
* `property` - Work with specified property.

### SessionAuthClient.project.**save**()




Parameters:


* `data` - Data (required).
* `property` - Work with specified property.
* `identity` - Identity.

### SessionAuthClient.project.**create**()




Parameters:


* `data` - Data (required).
* `property` - Work with specified property.

### SessionAuthClient.**projects**

Many projects manipulation object


### SessionAuthClient.projects.**find**()




Parameters:


* `text` - Full text search value.
* `sort` - None.
* `page` - None.
* `filter` - Filter query.
* `per_page` - None.

### SessionAuthClient.projects.**count**()




Parameters:


* `text` - Full text search value.
* `filter` - Filter query.

### SessionAuthClient.**user**

Authenticated by session user manipulation object


### SessionAuthClient.user.**get**()




### SessionAuthClient.user.**logout**()




### SessionAuthClient.user.**update**()




Parameters:


* `data` - Data (required).



## ProjectClient

Project client.

You should not initalize this client manually.
Use [Client.auth](#clientauth) method with ``token`` authentication or
[SessionAuthClient.use_project](#sessionauthclientuse_project) method.




### ProjectClient.**collection**

One collection manupulation object


### ProjectClient.collection.**get**()




Parameters:


* `identity` - Identity (required).
* `property` - Work with specified property.

### ProjectClient.collection.**save**()




Parameters:


* `data` - Data (required).
* `property` - Work with specified property.
* `identity` - Identity.

### ProjectClient.collection.**create**()




Parameters:


* `data` - Data (required).
* `property` - Work with specified property.

### ProjectClient.collection.**update**()




Parameters:


* `data` - Data (required).
* `identity` - Identity (required).
* `property` - Work with specified property.

### ProjectClient.collection.**remove**()




Parameters:


* `identity` - Identity (required).
* `property` - Work with specified property.

### ProjectClient.**collections**

Many collections manupulation object


### ProjectClient.collections.**find**()




Parameters:


* `text` - Full text search value.
* `sort` - None.
* `page` - None.
* `filter` - Filter query.
* `per_page` - None.

### ProjectClient.collections.**count**()




Parameters:


* `text` - Full text search value.
* `filter` - Filter query.

### ProjectClient.**document**

One document manupulation object


### ProjectClient.document.**remove**()




Parameters:


* `collection` - Collection (required).
* `identity` - Identity (required).
* `fields_exclude` - Return all but the excluded field.
* `fields` - Return specified fields only.
* `property` - Work with specified property.

### ProjectClient.document.**get_file**()




Parameters:


* `collection` - Collection (required).
* `identity` - Identity (required).
* `fields_exclude` - Return all but the excluded field.
* `fields` - Return specified fields only.
* `property` - Work with specified property.

### ProjectClient.document.**get**()




Parameters:


* `collection` - Collection (required).
* `identity` - Identity (required).
* `fields_exclude` - Return all but the excluded field.
* `fields` - Return specified fields only.
* `property` - Work with specified property.

### ProjectClient.document.**save**()




Parameters:


* `collection` - Collection (required).
* `data` - Data (required).
* `property` - Work with specified property.
* `identity` - Identity.
* `fields_exclude` - Return all but the excluded field.
* `fields` - Return specified fields only.

### ProjectClient.document.**update**()




Parameters:


* `collection` - Collection (required).
* `identity` - Identity (required).
* `data` - Data (required).
* `property` - Work with specified property.
* `fields_exclude` - Return all but the excluded field.
* `fields` - Return specified fields only.

### ProjectClient.document.**create**()




Parameters:


* `collection` - Collection (required).
* `data` - Data (required).
* `fields` - Return specified fields only.
* `property` - Work with specified property.
* `fields_exclude` - Return all but the excluded field.

### ProjectClient.**documents**

Many documents manupulation object


### ProjectClient.documents.**find**()




Parameters:


* `collection` - Collection (required).
* `fields_exclude` - Return all but the excluded field.
* `sort` - None.
* `filter` - Filter query.
* `page` - None.
* `per_page` - None.
* `fields` - Return specified fields only.
* `text` - Full text search value.

### ProjectClient.documents.**count**()




Parameters:


* `collection` - Collection (required).
* `text` - Full text search value.
* `fields` - Return specified fields only.
* `filter` - Filter query.
* `fields_exclude` - Return all but the excluded field.

### ProjectClient.documents.**update**()




Parameters:


* `collection` - Collection (required).
* `operation` - Update operation (required).
* `fields_exclude` - Return all but the excluded field.
* `fields` - Return specified fields only.
* `filter` - Filter query.

### ProjectClient.documents.**upsert**()




Parameters:


* `collection` - Collection (required).
* `operation` - Update operation (required).
* `fields_exclude` - Return all but the excluded field.
* `fields` - Return specified fields only.
* `filter` - Filter query.

### ProjectClient.documents.**remove**()




Parameters:


* `collection` - Collection (required).
* `fields` - Return specified fields only.
* `filter` - Filter query.
* `fields_exclude` - Return all but the excluded field.

### ProjectClient.**info**

Current project manupulation object


### ProjectClient.info.**get**()





