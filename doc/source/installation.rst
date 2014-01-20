.. _aggdraw: http://effbot.org/zone/aggdraw-index.htm

.. sectnum::
   :depth: 4
   :start: 1
   :suffix: .

Installation
------------

You can download the pydecorate source code from googlecodes,::

  $> git clone https://code.google.com/p/pydecorate/

and then run::

  $> python setup.py install



Transparency and antialiasing using AGG
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The default plotting mode of pydecorate uses PIL for rendering. 
However, PIL does not support antialiasing and opacity. 
The AGG engine can be used for making high quality images using the aggdraw_ module.

First make sure you have libfreetype and it's development files installed - on debian based systems you might do:

.. code-block:: bash

    $> sudo apt-get install libfreetype6 libfreetype6-dev

First install the aggdraw_ module. Please not that aggdraw_ is getting old and may have the following problems in building.
pip and easy_install may not solve these problems, so we recommend manual install.

With the current source of aggdraw_, it is necessary to point the build at the root of
Freetype install. To do this you must edit the aggdraw setup.py file, usually setting *FREETYPE_ROOT = "/usr"*
This is necessary for aggdraw to render text.

If the building of aggdraw fails with:

.. code-block:: bash

    agg_array.h:523: error: cast from ‘agg::int8u*’ to ‘unsigned int’ loses precision
    
Try:

.. code-block:: bash

    export CFLAGS="-fpermissive"
    
before building.


