Guide for developers
====================

This document is intended to detail some of the inner workings of Ganga to both document what we have done as well as make it easier for new developers to get on-board quicker.

Get started with development:
-----------

Working on the Codebase
^^^^^^^^^^^^^^^
To get started with contributing & making changes to the Ganga Codebase:

1. Developers need to fork the Ganga repository. To do this, go to the `Ganga GitHub Repository <https://github.com/ganga-devs/ganga>`_, click on ``Fork`` button & Create a fork of the original repository.

2. Developers need to clone the Forked repository with:

   .. code-block:: bash

      git clone https://github.com/<USERNAME>/ganga.git

   Where ``<USERNAME>`` is the developer's username.

   .. note::

       The users can also clone the forked repository via ``SSH`` by using ``git clone git@github.com:<USERNAME>/ganga.git`` once their Public & Private ``SSH Keys`` are generated & configured on GitHub.

3. They need to go into the root of the project with :

   .. code-block:: bash

      cd ganga

4. Then, run the following command to install ganga from the repo as an editable python package with relevant runtime, coverage & test packages :

   .. code-block:: bash

      pip install -e .[dev]

   Now all changes made to the Ganga codebase will be reflected real-time

5. To test their changes, developers can either initiate the ganga shell with the ganga command or invoke it via a python script.

Working on the Documentation
^^^^^^^^^^^^^^^
To get started with contributing & making changes to the Ganga Codebase:

1. Developers need to fork the Ganga repository. To do this, go to the `Ganga GitHub Repository <https://github.com/ganga-devs/ganga>`_, click on ``Fork`` button & Create a fork of the original repository.

2. Developers need to install **Sphinx** Documentation generator. Installation instructions can be found on `their website <https://www.sphinx-doc.org/en/master/usage/installation.html>`_.

   .. note::
       Since documentation is generated using a **Makefile** in ``the ganga/doc/`` folder, users may also need to install ``make`` on their systems, i.e., a build tool that can run makefiles

3. Developers need to clone the repository with:

   .. code-block:: bash

      git clone https://github.com/<USERNAME>/ganga.git

   Where ``<USERNAME>`` is the developer's username.

   .. note::

       The users can also clone the forked repository via ``SSH`` by using ``git clone git@github.com:<USERNAME>/ganga.git`` once their Public & Private ``SSH Keys`` are generated & configured on GitHub.

4. They need to go into the docs folder i.e. ``ganga/doc/`` of the project with :

   .. code-block:: bash

      cd ganga/doc


5. Then, run the following command to generate documentation in the required format :

   .. code-block:: bash

      make <target>

   .. note::

       The supported list of targets are:

       .. list-table::
          :widths: 25 75
          :header-rows: 1

          * - Target
            - Description
          * - ``html``
            - to make standalone HTML files.
          * - ``dirhtml``
            - to make HTML files named index.html in directories.
          * - ``singlehtml``
            - to make a single large HTML file.
          * - ``pickle``
            - to make pickle files.
          * - ``json``
            - to make JSON files.
          * - ``htmlhelp``
            - to make HTML files and a HTML help project.
          * - ``qthelp``
            - to make HTML files and a qthelp project.
          * - ``applehelp``
            - to make an Apple Help Book.
          * - ``devhelp``
            - to make HTML files and a Devhelp project.
          * - ``epub``
            - to make an epub.
          * - ``latex``
            - to make LaTeX files, you can set PAPER=a4 or PAPER=letter.
          * - ``latexpdf``
            - to make LaTeX files and run them through pdflatex.
          * - ``latexpdfja``
            - to make LaTeX files and run them through platex/dvipdfmx.
          * - ``text``
            - to make text files.
          * - ``man``
            - to make manual pages.
          * - ``texinfo``
            - to make Texinfo files.
          * - ``info``
            - to make Texinfo files and run them through makeinfo.
          * - ``gettext``
            - to make PO message catalogs.
          * - ``changes``
            - to make an overview of all changed/added/deprecated items.
          * - ``xml``
            - to make Docutils-native XML files.
          * - ``pseudoxml``
            - to make pseudoxml-XML files for display purposes.
          * - ``linkcheck``
            - to check all external links for integrity.
          * - ``doctest``
            - to run all doctests embedded in the documentation (if enabled).
          * - ``coverage``
            - to run coverage check of the documentation (if enabled).
          * - ``apidoc``
            - to create RST files from source code documentation.

6. This would generate a ``_build/`` folder which would contain the relevant output files.

7. Now, all changes made to the Ganga Documentation can be tested/previewed by re-running above command after making the change.

GangaObject
-----------

At the core of a lot of Ganga is :class:`~.GangaObject`.
This is a class which provides most of the core functionality of Ganga including persistency, typed attribute checking and simplified construction.

.. note::
    There is currently some work being done to replace the existing implementation if ``GangaObject`` with a simpler version.
    The user-facing interface should not change at all but more modern Python features will be used to simplify the code.
    This will also affect how schemas are defined but not how they are presented or persisted.

Schema
------

The schema of a ``GangaObject`` defines the set of attributes belonging to that class along with their allowed types, access control, persistency etc.
Each ``GangaObject`` must define a schema which consists of a schema version number and a dictionary of :class:`~.Item`\ s.
Schema items must define their name and a default value and can optionally define a lot more such as a list of possible types and documentation string.

Proxy objects
-------------

In order to provide a nice interface to users, Ganga provides a :term:`Ganga Public Interface` which fulfils two main purposes.
Firstly it is a reduced set of objects so that the user is not bombarded with implementation details such as :class:`~.Node`.
Secondly, all ``GangaObjects`` available through the GPI are wrapped in a runtime-generated class called a *proxy*.

These proxy classes exist for a number of reasons but primarily they are there for access control.
While a ``GangaObject`` can has as many functions and attributes as it likes,
only those attributes in the schema and those methods which are explicitly exported will be available to users of the proxy class.

When working on internal Ganga code, you should never have to deal with any proxy objects at all.
Proxies should be added to objects as they are passed to the GPI and should be removed as they are passed back.

Attributes on proxy objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Proxy classes and the object that they are proxying have a set number of attributes which should be present.

If an object inherits from ``GangaObject`` the class can have the property ``_proxyClass`` set which will point to the relevant :class:`~.GPIProxyObject` subclass. This is created on demand in the ``addProxy`` and ``GPIProxyObjectFactory`` methods.
The proxy class (which is a subclass of ``GPIProxyObject`` and created using :func:`~.GPIProxyClassFactory`) will have the attribute `_impl` set to be the relevant ``GangaObject`` subclass.

When an instance of a proxy class is created, the `_impl` attribute of the instance will point to the instance of the ``GangaObject`` that is being proxied.


Repository
----------

A repository is the physical storage of data on disk (usually persisted ``GangaObjects``) as well as library interface to it.

Registry
--------

A registry is an in-memory data-store which is backed by a repository.

Job monitoring
--------------

IGangaFile
----------

All file types as of Ganga 6.1 inherit from ``IGangaFile``. This main exception to this is the ``File`` object which as of 05/05/2016 is used as it still has more features than the ``IGangaFile`` inheirted classes do.

+-------------------+--------------------------------------------------------------------------------------------------------+---------------+
| Attribute         | Use/Doc                                                                                                | Return type   |
+===================+=========================================================================================================+===============+
| namePattern       | This is used to contain the namePattern or basename of the file in question                            | str           |
+-------------------+--------------------------------------------------------------------------------------------------------+---------------+
| localDir          | This is the location where a file may be placed during a get() or sourced during a put()               | str           |
+-------------------+--------------------------------------------------------------------------------------------------------+---------------+
| get()             | This function is the method used to place a file from some remote location into localDir               | bool          |
+-------------------+--------------------------------------------------------------------------------------------------------+---------------+
| put()             | This function puts a file stored locally into some remote storage space                                | bool          |
+-------------------+--------------------------------------------------------------------------------------------------------+---------------+
| location          | This is the remote location where the file is. DiracFile should return an LFN here and stop being bad? | str           |
+-------------------+--------------------------------------------------------------------------------------------------------+---------------+
| workerDir         | This is where the file should be placed on the working dir on the WN where the job script executes     | str           |
+-------------------+--------------------------------------------------------------------------------------------------------+---------------+
| remove()          | Removes a file on the remote storage (and asks the user if they want to remove a local one             | bool          |
+-------------------+--------------------------------------------------------------------------------------------------------+---------------+
| accessURL()       | Provides an address (inc protocol) for accessing a file which is stored locally but is 'streamable'    | str           |
+-------------------+--------------------------------------------------------------------------------------------------------+---------------+
| hasMatchedFiles() | Has this file matches any wildcards to subfiles?                                                       | bool          |
+-------------------+--------------------------------------------------------------------------------------------------------+---------------+
| setLocation()     | This function triggers the code to 'match' the file based upon ''__postprocesslocations__''            | bool          |
+-------------------+--------------------------------------------------------------------------------------------------------+---------------+
| _auto_remove()    | Called when a job is removed, by default is calls remove() to remove a remote file                     | bool          |
+-------------------+--------------------------------------------------------------------------------------------------------+---------------+


+----------------------------+---------------------------------------------------------------------------------------------------------------------+
| Script Generator           |  When is it used?                                                                                                   |
+============================+=====================================================================================================================+
| getWNScriptDownloadCommand | This generates a script which will make the file accessible from the WN when the job starts running                 |
+----------------------------+---------------------------------------------------------------------------------------------------------------------+
| getWNInjectedScript        | This generates a script which will send the file to the remote directory from the WN with no client intervention    |
+----------------------------+---------------------------------------------------------------------------------------------------------------------+


+------------------------+-----------------------------------------------------------------------+---------------+
| Special attr           | Use/Doc                                                               | Return type   |
+========================+=======================================================================+===============+
| lfn                    | Unique to the DiracFile. This is the LFN of the file in the DFC       | str           |
+------------------------+-----------------------------------------------------------------------+---------------+
| getReplicas            | Unique to DiracFile returns a list of SE where the file is replicated | list of str   |
+------------------------+-----------------------------------------------------------------------+---------------+
| '_list_get__match__()' | IGangaFile, performs a type match on file objects. can we remove this?| bool          |
+------------------------+-----------------------------------------------------------------------+---------------+


