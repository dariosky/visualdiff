Visual diff tests for Python
============================

Automate chrome browser render diffs for website testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Featuring Puppeteer, headless Chrome and Python image diffing

Installation
------------

.. code:: bash

    pip install visualdiff

Usage
-----

Create your tests calling ``visualdiff.compare(url)``, this will drive a
headless Chrome session rendering the desired URL and comparing the
resulting image with an expected one.

The expectation are stored by default in a ``visualdiff`` subfolder of
the current calling test script.

There are several additional options you can use, we'll see them in the
examples

Examples
--------

.. code:: python

    import visualdiff as vd

    assert not vd.difference('https://example.com')

Credits:
--------

-  It is a long time that I wanted a tool like this one, but thanks to
   `this article from Monica
   Dinculescu <https://meowni.ca/posts/2017-puppeteer-tests/>`__ for
   finally convincing me.
-  Thanks to Mijakogi for `the outstanding work on
   Pyppeteer <https://github.com/miyakogi/pyppeteer/>`__
