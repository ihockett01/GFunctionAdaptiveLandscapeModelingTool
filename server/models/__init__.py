from server.models.BaseModelsSchema import BaseModel as b

import os
import sys
import pkgutil
import importlib

pkg_dir = os.path.dirname(__file__)
for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module('.' + name, __package__)

AllModels = {cls.__name__: cls for cls in b.__subclasses__()}