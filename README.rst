===============
Gabbi + Tempest
===============

This is an exploration of running gabbi_ as a tempest plugin. This
code is based entirely on the work of Mehdi Abaakouk who made a
tempest plugin for gnocchi_. This code models that but tries to
be more generic: it allows you to set a ``GABBI_TEMPEST_PATH``
environment variable pointing to multiple directories containing
gabbi YAML files.

The test harness sets a series of enviornment variables that can
be used in the YAML to reach the available services. These will
eventually need to be extended (or can be extended by subclasses).

For each service in the service catalog there are
``<SERVICE_TYPE>_SERVICE`` and ``<SERVICE_TYPE>_BASE`` variables
(e.g., ``PLACEMENT_SERVICE`` and ``PLACEMENT_BASE``). A useful
``SERVICE_TOKEN``, ``IMAGE_REF``, ``FLAVOR_REF`` and ``FLAVOR_REF_ALT``
are also available.

Trying It
---------

To experiment with this you need a working tempest installation and
configuration. I used devstack with::

    enable_service tempest
    INSTALL_TEMPEST=True

in local.conf.

Once tempest is confirmed to be working, make a clone of this repo,
cd into it and do the equivalent of::

    pip install -e .

If you are using virtualenvs or need sudo, your form will be
different.

Go to the tempest directory (often ``/opt/stack/tempest``) and run
tempest limiting the test run to gabbi related tests and setting
the PATH variable::

    GABBI_TEMPEST_PATH=/path/one:/path/two tempest run --regex gabbi

This will run the tests described by the YAML files in
``/path/one`` and ``/path/two``.

There is a sample files in ``samples`` in the repo which you can try
with::

    GABBI_TEMPEST_PATH=/path/to/samples tempest run --regex gabbi

.. _gnocchi: https://review.openstack.org/#/c/301585/
.. _gabbi: https://gabbi.readthedocs.org/
