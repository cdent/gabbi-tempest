===============
Gabbi + Tempest
===============

This is an exploration of running gabbi_ as a tempest plugin. This
code is based entirely on the work of Mehdi Abaakouk who made a
tempest plugin for gnocchi_. This code models that but will try to
be more generic, eventually.

For the time being it works with Nova.

To experiment with it you need a working tempest installation and
configuration. I used devstack with::

    enable_service tempest

in local.conf.

Once tempest is confirmed to be working, make a clone of this repo,
cd into it and do the equivalent of::

    pip install -e .

If you are using virtualenvs or need sudo, your form will be
different.

Go to the tempest directory and run testr limit the test run to
gabbi related tests::

    testr run gabbi --subunit |subunit-trace

This will run the tests described by the YAML files in
``gabbi_tempest/tests/scenario/gabbits/``. Edit those files and run
the testr command again for fun and adventure.

.. _gnocchi: https://review.openstack.org/#/c/301585/
.. _gabbi: https://gabbi.readthedocs.org/
