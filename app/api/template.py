from fastapi import APIRouter

from models.template import Template

router = APIRouter()


@router.get("/", tags=["template"])
async def read_templates():
    return await Template.find_all().to_list()


@router.post("/", tags=["template"])
async def add_template(template: Template):
    await template.insert()
