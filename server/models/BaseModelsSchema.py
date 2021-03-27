import matplotlib.pyplot as plt, mpld3
from typing import TypeVar
import json
import logging

logging.basicConfig(level=logging.DEBUG, filename='api.log', encoding='utf-8')
SchemaObjectType = TypeVar('SchemaObject')

class SchemaObject:

    ID: str
    ObjectDescription: str
    DefaultValue: object
    Required: bool

    def __init__(self, defaultValue: object = None, id: str = None, objectDescription: str = None, required: bool = None):
        
        self.ID = id
        self.DefaultValue = defaultValue
        self.ObjectDescription = objectDescription
        self.Required = required or True

class Schema(dict):
    
    Description: str
    
    def __init__(self, description: str, *arg,**kw):
        self.Description = description
        super(Schema, self).__init__(*arg, **kw)

    def ToJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)

class BaseModel:
    ModelSchema: Schema
    Parameters: None
    Base: None
    Is3d: bool
    Format: str
    
    def __init__(self, child):
        self.Base = super(type(self), child)    
        pass

    def Run(self, is3d: bool, format: str, parameters: dict):

        logging.info('running ' + self.ModelSchema.Description)

        self.Format = format
        self.Is3d = is3d
        self.Parameters = self.__EnsureParameters__(parameters)
            
        return self.__Run__()

    def __EnsureParameters__(self, parameters: dict):
        returnParameters = dict()

        for key, value in self.ModelSchema.items():
            if ((not key in parameters or parameters[key] is None or parameters[key] == '') and 
                value.Required and value.DefaultValue is not None):
                returnParameters[key] = value.DefaultValue
            else:
                returnParameters[key] = parameters[key]
            
        return returnParameters

    def __Run__(self):
        pass

    def __Complete__(self, fig, plt):

        if self.Format == 'Python':
            plt.show()
            return True
        elif self.Format == 'Api':
            figDictionary = mpld3.fig_to_dict(fig)
            plt.close()
            return figDictionary
        else:
            raise ValueError(self.Format)




    

    
