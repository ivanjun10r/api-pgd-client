=======
History
=======

Unreleased
----------

**Build**

* Migrated dependency management from Poetry to uv
* Replaced ``poetry-core`` build backend with ``hatchling``
* Converted ``[tool.poetry*]`` sections to ``[dependency-groups]`` (PEP 735)
* Updated ``tox.ini`` to use ``uv-venv-runner`` and ``dependency_groups``
* Added ``make requirements`` target to regenerate requirements files via ``uv export``
* Regenerated ``requirements.txt``, ``requirements_dev.txt`` and ``requirements_test.txt``
* Removed ``poetry.lock``; ``uv.lock`` generated in its place

**Documentation**

* Rewrote ``README.rst`` with concise description, quick-start and features list (pt-BR)
* Updated ``docs/installation.rst`` with uv-based dev environment setup
* Updated ``docs/usage.rst`` with detailed usage examples for all entities
* Updated ``CONTRIBUTING.rst`` with uv setup instructions and corrected Python version matrix

**Bug Fixes**

* Fixed JSONDecodeError masking HTTP errors in non-JSON responses
* Improved error handling for 504 Gateway Timeout and 502 Bad Gateway errors
* Added proper fallback to response.text when JSON parsing fails
* Enhanced error messages to show actual HTTP status codes and response content

0.1.0 (2025-04-24)
------------------

* First release.
