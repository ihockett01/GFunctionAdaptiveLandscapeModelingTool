import matplotlib.pyplot as plt
from typing import List


class SchemaObject:
    ObjectName: str
    ObjectDescription: str
    DefaultValue: object
    Required: bool

    def __init__(self, objectName: str, defaultValue: object = None, objectDescription: str = None, required: bool = None):
        self.ObjectName = objectName
        self.DefaultValue = defaultValue
        self.ObjectDescription = objectDescription
        self.Required = required or True

class Schema:
    Parameters: dict[str, SchemaObject]
    Description: str
    
    def __init__(self, description: str, parameters: List[SchemaObject]):
        self.Description = description
        for so in parameters:
            self.Parameters[so.ObjectName] = so

class BaseModel:
    ModelSchema: Schema

    def __init__(self, parameters: dict[str, object]):
        missingParams = self.ValidateParameters(parameters)
        if missingParams.__len__ > 0:
            raise ValueError(missingParams)

    def Run(self):
        """
        executes the model
        """
        raise NotImplementedError

    def ValidateParameters(self, parameters) -> []:
        missingParams = []
        for key, value in self.ModelSchema.Parameters.items():
            
            if ((not key in parameters or parameters[key] is None or parameters[key] is '') and 
                value.Required and value.DefaultValue is None):
                missingParams.append(key)
            
        return missingParams

    
