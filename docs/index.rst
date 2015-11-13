============================
Klein, a Web Micro-Framework
============================

.. image:: https://travis-ci.org/twisted/klein.png?branch=master

Klein is a micro-framework for developing production-ready web services with Python.
It's built on widely used and well tested components like Werkzeug and Twisted, and has near-complete test coverage.

Klein is developed by a team of contributors `on GitHub <https://github.com/twisted/klein>`_.
We're also commonly in ``#twisted.web`` on `Freenode <http://freenode.net>`_.


Introduction to Klein
=====================

This is an introduction to Klein, going through from creating a simple web site to something supporting AJAX and more.

.. toctree::
    :maxdepth: 1

    introduction/1-gettingstarted
    introduction/2-twistdtap


Klein Examples
==============

These are examples that show how to use different parts of Klein, or use things with Klein.

.. toctree::

    examples/staticfiles
    examples/templates
    examples/deferreds
    examples/twistd
    examples/handlingpost
    examples/subroutes
    examples/nonglobalstate
    examples/handlingerrors
    examples/testing


Contributing
============

If you'd like to help out, here's some material to help you get started!

.. toctree::

    contributing


Help
====

If you have questions about Klein, two of the best places to ask are Stack Overflow and IRC.
Stack Overflow's `twisted.web tag <http://stackoverflow.com/questions/new/twisted.web?show=all&sort=newest>`_ is a good place to ask specific questions.
You can also look for help on IRC: the Freenode channel ``#twisted.web`` has many residents with domain knowledge about Twisted.
For help about routing and the other parts of Klein provided by Werkzeug, you may want to start with `Werkzeug's community resources <http://werkzeug.pocoo.org/community/>`_.
