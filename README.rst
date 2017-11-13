Datapunt Objectstore Libary
===============================================

.. image:: https://img.shields.io/badge/python-3.6%2C%203.5%2C%203.6-blue.svg
    :target: https://www.python.org/

.. image:: https://img.shields.io/badge/license-MPLv2.0-blue.svg
    :target: https://www.mozilla.org/en-US/MPL/2.0/

---------------------


Contributing
------------

Found a bug or want to work on the code? You can branch the `repository on
GitHub <https://github.com/DatapuntAmsterdam/objectstore>`_ or file an issue at its
`issue tracker <https://github.com/DatapuntAmsterdam/objectstore/issues>`_.


1. Install the dev dependencies in your virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ pip install -e .[dev]

Note: the ``[dev]`` refers to extra requirements for development and is
specified in ``setup.py``. You don't need to install them as the ``make test``
and ``make coverage`` targets work fine without having them in the virtualenv.
The only reason you might want to install them is so for example ``pytest`` and
``responses`` can be resolved in you IDE.

2. Create a configuration or environment file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In ``config.yml`` you can see an example configuration. You can either:

- make a copy of ``config.yml``, adjust it to your needs and point to it using
  export OBJECTSTORE_CONFIG=`pwd`/my_config.yml
- or export values for the environment variables referenced in ``config.yml``.

3. Download the Internet! (by example)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Look in the ``examples`` folder to see example usage.

::

 	$ todo!

Work in progress

::

 	$ todo

Now you can develop, run and test code!

4. Make awesome visualizations with the data downloaded.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

THAT IS YOUR JOB!
