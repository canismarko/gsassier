import os
import sys
import logging
import warnings
from pathlib import Path
import importlib.util

from . import exceptions


log = logging.getLogger(__name__)


def find_gsas(candidates=[], add_to_path=True) -> Path:
    """Try and find the installation directory for GSAS-II
    
    Tries some expected default locations, and looks in any anaconda
    installations and environments that may be present (provided
    anaconda is active). Additional paths to search first can be
    provided by the *candidates* parameter.
    
    Parameters
    ==========
    add_to_path
      If true, the GSAS-II directory will be added to the system path
      so it can be imported immediately.
    
    Returns
    =======
    gsasdir
      Path to the first detected ``GSASII/`` directory
    
    Raises
    ======
    GSASIINotFound
      A suitable ``GSASII/`` directory cannot be located.
    
    """
    gsasdir = None
    # First try some simple defaults
    candidates.extend([Path("~/g2full").expanduser(), Path("~/g2conda").expanduser(), Path.home()])
    # Check for anaconda installation
    python_bin = Path(sys.executable).resolve()
    anaconda_flavors = ['anaconda', 'anaconda2', 'anaconda3', 'miniconda', 'miniconda2', 'miniconda3',
                        'Anaconda', 'Anaconda2', 'Anaconda3', 'Miniconda', 'Miniconda2', 'Miniconda3']
    path_parts = python_bin.parts
    anacondas = [flavor for flavor in anaconda_flavors if flavor in path_parts]
    for flavor in anacondas:
        # Check for a global anaconda installation
        idx = path_parts.index(flavor)
        conda_root = Path(path_parts[0]).joinpath(*path_parts[1:idx+1])
        candidates.append(conda_root)
        # Check if we're in a conda environment
        if "envs" in path_parts:
            idx = path_parts.index("envs")
            env_root = Path(path_parts[0]).joinpath(*path_parts[1:idx+2])
            candidates.append(env_root)
        # Now check all the other environments
        all_envs_root = conda_root/"envs"
        if all_envs_root.exists():
            # Add a couple of sensible named environments
            candidates.append(all_envs_root/"gsas")
            candidates.append(all_envs_root/"gsas2")
            candidates.append(all_envs_root/"gsas2full")
            candidates.append(all_envs_root/"g2full")
            # Add all remaining environments
            candidates.extend(all_envs_root.iterdir())
    # Check if any of the candidate locations contain GSASII
    for path in candidates:
        log.debug("Checking GSASII candidate: %s", path)
        if (path/"GSASII"/"GSASIIscriptable.py").exists():
            gsasdir = path/"GSASII"
            break
    # Check if we have successfully found GSASII/
    if gsasdir is None:
        msg = ("Unable to locate a suitable ``GSASII/`` directory. "
               "Consider suggesting somewhere to look with *candidates*.")
        raise exceptions.GSASIINotFound(msg)
    else:
        log.info("Found GSASII directory: %s", gsasdir)
        if add_to_path:
            sys.path.append(str(gsasdir))
        return gsasdir


class module_prop():
    def __init__(self, name):
        self.name = name
    
    def __get__(self, obj, type=None):
        try:
            gsas_module = obj.gsas_module
        except:
            gsas_module = super(obj.__class__, obj)
        return getattr(gsas_module, self.name)
    
    def __set__(self, obj, value):
        raise AttributeError
    
    def __delete__(self, obj):
        raise AttributeError


class GSASIILazyModule():
    """A helper class to lazily load the GSASII modules.
    
    This can be used to specify a GSASII directory even after this
    object has been loaded.
    
    The intended usage if GSASII is automatically found:
    
    .. code:: python
        
        from gsassier import GSASIIscriptable
    
    If GSAS-II is not automatically findable, then:
    
    .. code:: python
        
        from gsassier import GSASIIscriptable
        GSASIIscriptable.gsas_directory = "~/mystuff/GSASII"
    
    To access the help message for the underlying GSASIIscriptable
    module, use ``help(GSASIIscriptable.gsas_module)``
    
    """
    _gsas_module = None
    gsas_directory = None
    # Override certain duner methods
    __builtins__ = module_prop("__builtins__")
    __cached__ = module_prop("__cached__")
    # __doc__ = module_prop("__doc__")
    __dir__ = module_prop("__dir__")
    __file__ = module_prop("__file__")
    __loader__ = module_prop("__loader__")
    __name__ = module_prop("__name__")
    __package__ = module_prop("__package__")
    __repr__ = module_prop("__repr__")
    __spec__ = module_prop("__spec__")
    __warningregistry__ = module_prop("__warningregistry__")
    
    def __init__(self, module_name=""):
        try:
            self.gsas_directory = find_gsas()
        except exceptions.GSASIINotFound:
            msg = ("Unable to locate a suitable ``GSASII/`` directory. "
                   "Set ``GSASIIscriptable.gsas_directory`` "
                   "before using this module.")
            warnings.warn(msg)
    
    @property
    def gsas_module(self):
        if self._gsas_module is None:
            sys.path.append(str(self.gsas_directory.expanduser().resolve()))
            import GSASIIscriptable as _gsas_module
            self._gsas_module = _gsas_module
        return self._gsas_module
    
    def __getattr__(self, attr):
        return getattr(self.gsas_module, attr)


GSASIIscriptable = GSASIILazyModule('GSASIIscriptable')
