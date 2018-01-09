===============
Gabbi + Tempest
===============

Gabbi-tempest is an experimental Tempest_ plugin_ that enables
testing the APIs of running OpenStack services, integrated with
tempest but without needing to write Python. Instead the YAML
format_ provided by gabbi_ is used to write and evaluate HTTP
requests and responses.

Tests are placed in YAML files in one or more directories. Those
directories are added to a ``GABBI_TEMPEST_PATH`` environment
variable. When that variable is passed into a tempest test
runner that is aware of the gabbi plugin, the files on that path
will be used to create tempests tests.

The test harness sets a series of enviornment variables that can
be used in the YAML to reach the available services. The available
variables may be extended in two ways:

* Adding them to the environment that calls tempest if the values are
  known.
* Setting them in a subclass of the plugin if the values need to
  be calculated from what tempest knows.

For each service in the service catalog there are
``<SERVICE_TYPE>_SERVICE`` and ``<SERVICE_TYPE>_BASE`` variables
(e.g., ``PLACEMENT_SERVICE`` and ``PLACEMENT_BASE``). A useful
``SERVICE_TOKEN``, ``IMAGE_REF``, ``FLAVOR_REF`` and ``FLAVOR_REF_ALT``
are also available.

For the time being the ``SERVICE_TOKEN`` is ``admin``.

Trying It
---------

To experiment with this you need a working tempest installation and
configuration. One way to do that is to use devstack_ with the
following added to the local.conf::

    enable_service tempest
    INSTALL_TEMPEST=True

in local.conf.

Once tempest is confirmed to be working, gabbi-tempest must be
installed. Either install it from PyPI::

   pip install gabbi-tempest

Or make a clone of this repo_, cd into it, and do the equivalent of::

    pip install -e .

If you are using virtualenvs or need sudo, your form will be
different.

Create some gabbi_ tests that exercise the OpenStack services. There
are sample files in the ``samples`` directory in the repo_.

Go to the tempest directory (often ``/opt/stack/tempest``) and run
tempest as follows. Adding the ``regex`` will  limit the test run
to just gabbi related tests::

    GABBI_TEMPEST_PATH=/path/one:/path/two tempest run --regex gabbi

This will run the tests described by the YAML files in
``/path/one`` and ``/path/two``.

History
-------

This code is based  on the work of Mehdi Abaakouk who made a tempest
plugin for gnocchi_ that worked with gabbi_. He figured out the
details of the plugin structure.

.. _devstack: https://docs.openstack.org/devstack/latest/
.. _Tempest: https://docs.openstack.org/tempest/latest/
.. _plugin: https://docs.openstack.org/tempest/latest/plugin.html
.. _gnocchi: https://review.openstack.org/#/c/301585/
.. _gabbi: https://gabbi.readthedocs.org/
.. _format: https://gabbi.readthedocs.io/en/latest/format.html
.. _repo: https://github.com/cdent/gabbi-tempest
