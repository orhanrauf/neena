from app.models.organization import Organization
from app.schemas import OrganizationCreate, OrganizationUpdate
from app.crud.base import CRUDBase

class CRUDOrganization(CRUDBase[Organization, OrganizationCreate, OrganizationUpdate]):
    pass

organization = CRUDOrganization(Organization)
