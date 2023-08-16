from typing import Optional
from beanie import Document, Indexed, Link
from pydantic import BaseModel


class Template(Document):
    slug: str
    template_file: str

class TemplateRender(Document):
    template: Link[Template]
    context: dict

class Render(BaseModel):
    slug: str
    context: Optional[dict] = None
