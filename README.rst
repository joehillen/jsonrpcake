*********************************************
JSONRPCake: a CLI JSON-RPC client for humans.
*********************************************


JSONRPCake is a **command line JSON-RPC client**
that wraps the jsonrpc-ns library.
It is a fork of `HTTPie`_ written by `Jakub Roztocil`_.
Its goal is to make CLI interaction
with `JSON-RPC`_ 2.0 services as **human-friendly** as possible. It provides a
simple ``jsonrpc`` command that allows for sending arbitrary `JSON-RPC`_ requests using a
simple and natural syntax, and displays colorized responses. JSONRPCake can be used
for **testing, debugging**, and generally **interacting** with `JSON-RPC`_ servers.

JSONRPCake is written in Python, and under the hood it uses the
`jsonrpc-ns`_ and `Pygments`_ libraries.


**Table of Contents**


.. contents::
    :local:
    :depth: 1
    :backlinks: none


=============
Main Features
=============

* Expressive and intuitive syntax
* Formatted and colorized terminal output
* Built-in JSON support
* Arbitrary request data


============
Installation
============

The latest **stable version** of JSONRPCake can always be installed or updated
to via `pip`_:

.. code-block:: bash

    $ pip install --upgrade jsonrpcake


=====
Usage
=====


Hello World:


.. code-block:: bash

    $ jsonrpc example.org:3000 hello


Synopsis:

.. code-block:: bash

    $ jsonrpc ADDRESS:PORT METHOD [PARAMETER [PARAMETER [...]]]

See also ``jsonrpc --help``.


--------
Examples
--------

`JSON`_ params:

.. code-block:: bash

    $ jsonrpc example.org:3000 update name=John uid:=1234


=========================
JSON-RPC Address and Port
=========================

The address and port are separated by a ':'.
The TCP port is **required**. When the address **omitted**,
the default address is ``localhost``.

.. code-block:: bash

    $ jsonrpc :3000 users

Is equivalent to:

.. code-block:: bash

    $ jsonrpc localhost:3000 users


===============
JSON-RPC Method
===============

The name of the JSON-RPC method comes right after the address and port:

.. code-block:: bash

    $ jsonrpc example.org:3000 users


The ``METHOD`` argument is **required**.


=============
Parameters
=============

JSON parameters are key/value pairs specified after the ```METHOD```.
The parameter type is distinguished only by the separator used:
``:``, ``=``, ``:=``, ``==``, ``@``, ``=@``, and ``:=@``. The ones with an
``@`` expect a file path as value.

+-----------------------+-----------------------------------------------------+
| Item Type             | Description                                         |
+=======================+=====================================================+
| Data Fields           | Request data fields to be serialized as a JSON      |
| ``field=value``,      | object (default).                                   |
+-----------------------+-----------------------------------------------------+
| Raw JSON fields       | Useful when sending JSON and one or                 |
| ``field:=json``,      | more fields need to be a ``Boolean``, ``Number``,   |
| ``field:=@file.json`` | nested ``Object``, or an ``Array``,  e.g.,          |
|                       | ``meals:='["ham","spam"]'`` or ``pies:=[1,2,3]``    |
|                       | (note the quotes).                                  |
+-----------------------+-----------------------------------------------------+


================
Redirected Input
================

**A universal method for passing request parameters is through redirected** ``stdin``
(standard input). Such data is buffered and then with no further processing
used as the request body. There are multiple useful ways to use piping:

Redirect from a file:

.. code-block:: bash

    $ jsonrpc example.com:7080 add.user < person.json


You can use ``echo`` for simple data:

.. code-block:: bash

    $ echo '{"uid": 1234, "name": "John"}' | jsonrpc example.com:3000 update.userinfo


You can use ``cat`` to enter multiline data on the terminal:

.. code-block:: bash

    $ cat | jsonrpc example.com:3000 update
    <paste>
    ^D


To prevent JSONRPCake from reading ``stdin`` data you can use the
``--ignore-stdin`` option.


=================
Terminal Output
=================

JSONRPCake does several things by default in order to make its terminal output
easy to read.


---------------------
Colors and Formatting
---------------------

Syntax highlighting is applied to the response (where it makes
sense). You can choose your prefered color scheme via the ``--style`` option
if you don't like the default one (see ``$ jsonrpc --help`` for the possible
values).

Also, the following formatting is applied:

* JSON data is indented, sorted by keys, and unicode escapes are converted
  to the characters they represent.

One of these options can be used to control output processing:

====================   ========================================================
``--pretty=all``       Apply both colors and formatting.
                       Default for terminal output.
``--pretty=colors``    Apply colors.
``--pretty=format``    Apply formatting.
``--pretty=none``      Disables output processing.
                       Default for redirected output.
====================   ========================================================


=================
Redirected Output
=================

JSONRPCake uses **different defaults** for redirected output than for
`terminal output`_:

* Formatting and colors aren't applied (unless ``--pretty`` is specified).
* Only the response message is printed.

Force colorizing and formatting, and show both the request and the response in
``less`` pager:

.. code-block:: bash

    $ jsonrpc --pretty=all --verbose example.org:7080 info | less -R


The ``-R`` flag tells ``less`` to interpret color escape sequences included
JSONRPCake`s output.


=======
Authors
=======

Forked by `Joe Hillenbrand`_

`Jakub Roztocil`_  created `HTTPie`_ and `these fine people`_
have contributed.

=======
Licence
=======

Please see `LICENSE`_.


------------


.. _JSON-RPC: http://www.jsonrpc.org/specification
.. _JSON: http://www.json.org/
.. _HTTPie: https://github.com/jkbr/httpie
.. _these fine people: https://github.com/jkbr/httpie/contributors
.. _jsonrpc-ns: https://github.com/flowroute/jsonrpc-ns
.. _Pygments: http://pygments.org/
.. _pip: http://www.pip-installer.org/en/latest/index.html
.. _Jakub Roztocil: http://subtleapps.com
.. _Joe Hillenbrand: http://joehillen.org
.. _LICENSE: https://github.com/joehillen/jsonrpcake/blob/master/LICENSE
