from typing import List, Optional
from pydantic import BaseModel, Field

class Glycan(BaseModel):
    name: str
    attachment_site: int = Field(..., description="Residue index on the carrier protein (1-based)")
    linkage: str = Field(..., description="e.g., alpha-2,8")
    length: int = Field(..., description="Number of sugar units")
    sequence: Optional[str] = Field(None, description="IUPAC or LINUCS sequence string")

class CarrierProtein(BaseModel):
    name: str
    uniprot_id: Optional[str] = None
    sequence: str = Field(..., description="Amino acid sequence")
    pdb_id: Optional[str] = None

class Glycoconjugate(BaseModel):
    name: str
    carrier_protein: CarrierProtein
    glycans: List[Glycan]
    meta: dict = Field(default_factory=dict, description="Pathogen, serotype, notes")

class EpitopePredictionRequest(BaseModel):
    construct: Glycoconjugate
    job_id: str
