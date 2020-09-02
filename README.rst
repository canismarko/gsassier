GSAS-II: Gsassier!
==================

Wrappers for the GSAS-II package

Finding GSASII
--------------

*gsassier* will attempt to find your GSAS-II installation directory
automatically. As long as your setup is not too complicated, you can
simply import GSASIIscriptable directly from gsassier.

.. code-block:: python

  from gsassier import GSASIIscriptable as gsas

.. warning::

   If it best if GSAS-II is installed in the same anaconda environment
   as *gsassier*. *gsassier* will look for GSAS-II in other anaconda
   environments, but this will only work if both environments use the
   same python version and have similar packages installed. Use at
   your own risk.
