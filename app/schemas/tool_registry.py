from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field

class FieldSchema(BaseModel):
    type: str
    description: Optional[str] = None
    required: bool = True

class SchemaDefinition(BaseModel):
    input: Dict[str, FieldSchema] = {}
    output: Dict[str, FieldSchema] = {}

class Tool(BaseModel):
    name: str = Field(..., description="Nome da função/ferramenta")
    description: str = Field(..., description="Breve descrição da funcionalidade")
    url: str = Field(..., description="Endpoint completo da API")
    method: str = Field(..., description="Método HTTP (GET, POST, PUT, DELETE)")
    schema: SchemaDefinition = Field(..., description="Schema de entrada e saída")
