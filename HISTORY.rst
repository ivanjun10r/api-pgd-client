=======
History
=======

Unreleased
----------

**Bug Fixes**

* Fixed JSONDecodeError masking HTTP errors in non-JSON responses
* Improved error handling for 504 Gateway Timeout and 502 Bad Gateway errors
* Added proper fallback to response.text when JSON parsing fails
* Enhanced error messages to show actual HTTP status codes and response content

0.1.0 (2025-04-24)
------------------

* First release.
