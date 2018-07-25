Datapunt Objectstore Libary
===============================================

.. image:: https://img.shields.io/badge/python-3.6%2C%203.5%2C%203.6-blue.svg
    :target: https://www.python.org/

.. image:: https://img.shields.io/badge/license-MPLv2.0-blue.svg
    :target: https://www.mozilla.org/en-US/MPL/2.0/

---------------------

Objecstore Libary
-----------------

Contains common used objectstore code for our API's.

During import / ETL tasks we offten use data uploaded to the objecstore
from data sources.

Contributing
------------

Found a bug or want to work on the code? You can branch the `repository on
GitHub <https://github.com/DatapuntAmsterdam/objectstore>`_ or file an issue at its
`issue tracker <https://github.com/DatapuntAmsterdam/objectstore/issues>`_.


1. Install the dev dependencies in your virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ pip install --upgrade setuptools
    $ python setup.py install develop

The `setuptools` pakage must be upgraded (as shown above) because the version
that is pre-packaged with Python 3.6 causes problems when running the tests.

When you get a PYTHONPATH error, use the install-dir argument:

.. code-block:: bash

    $ python setup.py install develop --install-dir venv/lib/python3.6/site-packages

2. Run the tests
^^^^^^^^^^^^^^^^

The test suite and test coverage are run as follows:

.. code-block:: bash

    $ python setup.py test

The Python style checker Flake8 can be run as follows:

.. code-block:: bash

    $ python setup.py flake8


3. Example configuration and usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    python -m objecstore.databasedumps /backups/postgres.dump objectstore_dir --upload-db

uploads given dump with a date and environment informtion to objectstore


.. code-block:: bash

    python -m objecstore.databasedumps downloaddir objectstore_dir --download-db

Dowload latest dump with the name `database.environment.latestdate.dump` from given environmnet
with from location directory in objectstore.
- WILL DELETE OLD DUMPS more then 20 days old.

