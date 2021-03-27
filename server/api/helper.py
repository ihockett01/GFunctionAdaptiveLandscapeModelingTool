from server.models import DrugResistance as dr, Evolvability as ev, OnePrey as op, TwoPrey as tp
from server.models.BaseModelsSchema import BaseModel as b

# AllModels: dict
# AllModels = {cls.__name__: cls for cls in [ dr.DrugResistance, ev.Evolvability, op.OnePrey, tp.TwoPrey ]}

def ParseQueryString(queryString: str) -> dict:
    return dict(item.split('=') for item in queryString.split('&'))