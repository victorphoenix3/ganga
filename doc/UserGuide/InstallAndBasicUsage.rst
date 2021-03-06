Install and Basic Usage
=======================


Installation
------------

There are several ways to install and run Ganga:


**NOTE -** Currently Ganga is only available for python3 releases and supported on Linux distributions.


CVMFS
^^^^^

If you have access to CVMFS, Ganga can be found at ``/cvmfs/ganga.cern.ch/``. This will be kept up-to-date with the
latest release that you can run directly with:

``/cvmfs/ganga.cern.ch/runGanga.sh``

This isn't just a link to the start-up script because it needs to be run from the correct directory. However,
it will take all the command line options that the normal ganga script takes.


PyPI Install
^^^^^^^^^^^^

You can also install directly from PyPI using:

``pip install ganga``

If you don't have System Administrator rights or just want to do a private install then it can be beneficial to
run using a ``virtualenv``:

.. code-block:: bash

    # Create a virtualenv
    virtualenv -ppython3 gangaenv
    cd gangaenv/
    . bin/activate
    # Install Ganga 
    pip install ganga

To install pip locally if it's not on your system and you don't have admin access please consult: https://pip.pypa.io/en/stable/installing/

Alternatively if you want you can install it using pip to your local user environment (not recommended if you have many python projects/libraries around)

``pip install ganga --user``


From Github
^^^^^^^^^^^

You can always install Ganga's most recent commit at the time of writing by running 

``pip install -e git+git://github.com/ganga-devs/ganga.git#egg=ganga``

If you don't have System Administrator rights or just want to do a private install then it can be beneficial to
run using a ``virtualenv``:

.. code-block:: bash

    # Create a virtualenv
    virtualenv -ppython3 gangaenv
    cd gangaenv/
    . bin/activate
    # Install Ganga 
    pip install -e git+git://github.com/ganga-devs/ganga.git#egg=ganga


Starting Ganga
--------------

As described above, to run Ganga simply execute ``ganga`` (for PyPI install), ``<installdir>/bin/ganga``
(for other installs) or the helper script in CVMFS. This will start Ganga and it's associated threads as
well as provide you with a Ganga IPython prompt that gives you access to the Ganga Public Interface (GPI) on
top of the usual IPython functionality:

.. code-block::

    *** Welcome to Ganga ***
    Version: 6.1.16
    Documentation and support: http://cern.ch/ganga
    Type help() or help('index') for online help.

    This is free software (GPL), and you are welcome to redistribute it
    under certain conditions; type license() for details.


    Ganga.Utility.Config               : INFO     reading config file /home/mws/Ganga/install/6.1.14-pre/ganga/GangaAtlas/Atlas.ini
    Ganga.Utility.Config               : INFO     reading config file /home/mws/.gangarc

    For help visit the ATLAS Distributed Analysis Help eGroup:
      https://groups.cern.ch/group/hn-atlas-dist-analysis-help/

    [13:15:51]
    Ganga In [1]:


Note that the first time you run Ganga it will ask you to create a default ``.gangarc`` file which you should
probably do. In the future, if you want to recreate this default config file, add the option ``-g`` to the command line.

Getting Help
------------

The documentation for all objects and functions in Ganga can be accessed using the help system:

.. code-block:: python

    [13:25:29]
    Ganga In [1]: help()
    ************************************

    *** Welcome to Ganga ***
    Version: 6.1.16
    Documentation and support: http://cern.ch/ganga
    Type help() or help('index') for online help.

    This is free software (GPL), and you are welcome to redistribute it
    under certain conditions; type license() for details.



    This is an interactive help based on standard pydoc help.

    Type 'index'  to see GPI help index.
    Type 'python' to see standard python help screen.
    Type 'interactive' to get online interactive help from an expert.
    Type 'quit'   to return to Ganga.
    ************************************

    help>


Now typing ``index`` at the prompt will list all the objects, etc. available. You can also directly access the
documentation for an object using ``help`` directly:

.. literalinclude:: ../../ganga/GangaCore/test/GPI/TutorialTests.py
    :start-after: # -- INSTALLANDBASICUSAGE HELP START
    :end-before: # -- INSTALLANDBASICUSAGE HELP STOP
    :dedent: 8

You also have IPython's tab-complete service available to help identify members of an object.

Hello World with Ganga
----------------------

We are now in a position to submit our first job. This will take the defaults of the Ganga Job object which is
to run ``echo 'Hello World'`` on the machine you're currently running on:

.. literalinclude:: ../../ganga/GangaCore/test/GPI/TutorialTests.py
    :start-after: # -- INSTALLANDBASICUSAGE SUBMIT START
    :end-before: # -- INSTALLANDBASICUSAGE SUBMIT STOP
    :dedent: 8

If all goes well, you should see the job submit:

.. code-block:: python

    Ganga In [6]: j.submit()

    Ganga.GPIDev.Lib.Job               : INFO     submitting job 0
    Ganga.GPIDev.Lib.Job               : INFO     job 0 status changed to "submitting"
    Ganga.Lib.Executable               : INFO     Preparing Executable application.
    Ganga.Lib.Executable               : INFO     Created shared directory: conf-5bdd5d5a-07ce-4332-acbc-f0ab23ca7012
    Ganga.GPIDev.Lib.Job               : INFO     Preparing subjobs
    Ganga.GPIDev.Adapters              : INFO     submitting job 0 to Local backend
    Ganga.GPIDev.Lib.Job               : INFO     job 0 status changed to "submitted"

    Ganga Out [6]: 1


If you wait a few seconds and then press ``Enter`` you should then see that the job has already transitioned
through ``running`` and to ``completed``:

.. code-block:: python

    Ganga In [7]:

    Ganga.GPIDev.Lib.Job               : INFO     job 0 status changed to "running"
    Ganga.GPIDev.Lib.Job               : INFO     Job 0 Running PostProcessor hook
    Ganga.GPIDev.Lib.Job               : INFO     job 0 status changed to "completed"

    [13:34:10]
    Ganga In [7]:

You can view the job in your repository using the ``jobs`` command which lists all job objects that Ganga knows about:

.. code-block:: python

    Ganga In [7]: jobs
    Ganga Out [7]:

    Registry Slice: jobs (1 objects)
    --------------
        fqid |    status |      name | subjobs |    application |        backend |                             backend.actualCE |                       comment
    -------------------------------------------------------------------------------------------------------------------------------------------------------------
           0 | completed |           |         |     Executable |          Local |                       epldt017.ph.bham.ac.uk |


    [13:34:37]
    Ganga In [8]:

You can get more info about your job by selecting it from the repository:

.. literalinclude:: ../../ganga/GangaCore/test/GPI/TutorialTests.py
    :start-after: # -- INSTALLANDBASICUSAGE JOBS START
    :end-before: # -- INSTALLANDBASICUSAGE JOBS STOP
    :dedent: 8

You can also select specific info about the job object, e.g. the application that was run:

.. literalinclude:: ../../ganga/GangaCore/test/GPI/TutorialTests.py
    :start-after: # -- INSTALLANDBASICUSAGE JOBSAPP START
    :end-before: # -- INSTALLANDBASICUSAGE JOBSAPP STOP
    :dedent: 8

To check the ``stdout/stderr`` of a job, you can use a couple of methods:

.. code-block:: python

    jobs(0).peek('stdout', 'more')
    j = jobs(0)
    !more $j.outputdir/stdout


Job Monitoring
--------------

While Ganga is running in interactive mode, a background thread goes through all your active jobs and checks
to see what state they are in. Generally, jobs will transition from new -> submitted -> running -> completed/failed.
As described above, the `jobs` command will show you the state of your jobs in the Ganga repository.

In addition to this monitoring, there is also a web GUI provided that can be started using the ``--webgui``
option which gives a graphical representation of your repository. [NOTE THIS NEEDS TESTING AND MAY NOT WORK AT PRESENT!]


Scripting and Batch Mode
------------------------

You can put your ganga commands into a python script and then execute it from the Ganga prompt like this:

.. literalinclude:: ../../ganga/GangaCore/test/GPI/TutorialTests.py
    :start-after: # -- INSTALLANDBASICUSAGE EXECFILE START
    :end-before: # -- INSTALLANDBASICUSAGE EXECFILE STOP
    :dedent: 8

In addition, Ganga can be run in batch mode by just providing a script as the last argument:

.. code-block:: bash

    ganga submit.py
    /cvmfs/ganga.cern.ch/runGanga.sh submit.py

Note that by default, the monitoring is turned off while in batch mode.
