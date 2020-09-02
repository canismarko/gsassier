GSAS-II: Gsassier!
==================

Wrappers for the GSAS-II package

Finding GSASII
--------------

*gsassier* will attempt to find your GSAS-II installation directory
automatically. As long as your setup is not too complicated, you can
simply import GSASIIscriptable directly from gsassier to get most of
the functionality of GSASIIscriptable.

.. code-block:: python

		from gsassier import GSASIIscriptable as gsas

.. warning::

   If it best if GSAS-II is installed in the same anaconda environment
   as *gsassier*. *gsassier* will look for GSAS-II in other anaconda
   environments, but this will only work if both environments use the
   same python version and have similar packages installed. Use at
   your own risk.

If you receive a warning about not finding GSAS-II, you will need to
specify an installation directory:

.. code-block:: python

		from gsassier import GSASIIscriptable as gsas
		gsas.gsas_directory = "~/mystuff/GSASII"

The basic importing described above does not import the
GSASIIscriptable module directly, but rather an object that waits to
import the module until needed. As a consequence, there are **a few
things that don't quite work as expected**: ``help(GSASIIscriptable)``
and ``from GSASIIscriptable import *`` will not work properly.

If you need these features, you will need to import GSAS-II module
directly:

.. code-block:: python

		from gsassier import find_gsas
		find_gsas()
		from GSASIIscriptable import G2Project
