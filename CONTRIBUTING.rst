.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/ivanjun10r/api_pgd_client/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

PGD API Client could always use more documentation, whether as part of the
official PGD API Client docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/ivanjun10r/api_pgd_client/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `api_pgd_client` for local development.

This project uses `uv`_ to manage dependencies and virtual environments.

1. Fork the `api_pgd_client` repo on GitHub.

2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/api_pgd_client.git
    $ cd api_pgd_client

3. Install uv (if you haven't already)::

    $ curl -LsSf https://astral.sh/uv/install.sh | sh

4. Create the virtual environment and install all dependencies::

    $ uv sync --all-groups

5. Set up pre-commit hooks::

    $ uv run pre-commit install

6. Create a ``.env`` file with the required environment variables::

    PGD_API_USERNAME=seu_usuario
    PGD_API_PASSWORD=sua_senha
    PGD_SOURCE_SYSTEM_NAME=dev
    PGD_SOURCE_SYSTEM_VERSION=0.0.0

7. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

8. When you're done making changes, check that your changes pass linting and
   the tests::

    $ make lint
    $ make test

   To run tests against all supported Python versions with tox::

    $ uvx tox

9. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

10. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.9, 3.10, 3.11, 3.12 and 3.13.
   Check https://github.com/ivanjun10r/api_pgd_client/actions
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

    $ uv run pytest tests/test_client.py

To run linting (ruff + mypy)::

    $ make lint

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

    $ bump2version patch # possible: major / minor / patch
    $ git push
    $ git push --tags

Code of Conduct
---------------

Please note that this project is released with a `Contributor Code of Conduct`_.
By participating in this project you agree to abide by its terms.

.. _uv: https://docs.astral.sh/uv/
.. _`Contributor Code of Conduct`: CODE_OF_CONDUCT.rst
