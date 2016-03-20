
## DeformException

Bases: [Exception](#exception)

Base Deform.io exception.

Could be used for catching all Deform.io specific exception.

```python
try:
    deform_client.collections.find()
except DeformException as e:
    print 'Deform.io specific exception raised'
```

## HTTPError

Bases: [DeformException](#deformexception)

Base exception for errors produced at the HTTP layer.

These types of exceptions containes additional parameters:

* `requests_error` - original [requests exception][requests-exception].
* `errors` - list of errors.

[requests-exception]: http://docs.python-requests.org/en/master/api/#exceptions

## AuthError

Bases: [HTTPError](#httperror)

Errors due to invalid authentication credentials.

## ConflictError

Bases: [HTTPError](#httperror)



## ConnectTimeout

Bases: [ConnectionError](#connectionerror), [Timeout](#timeout)

The request timed out while trying to connect to the remote server.
Requests that produced this error are safe to retry.

## ConnectionError

Bases: [HTTPError](#httperror)

A Connection error occurred.

## ForbiddenError

Bases: [HTTPError](#httperror)



## NotFoundError

Bases: [HTTPError](#httperror)



## ReadTimeout

Bases: [Timeout](#timeout)

The server did not send any data in the allotted amount of time.

## Timeout

Bases: [HTTPError](#httperror)

The request timed out.
Catching this error will catch both
[ConnectTimeout](#connecttimeout) and
[ReadTimeout](#readtimeout) errors.

## ValidationError

Bases: [HTTPError](#httperror)


