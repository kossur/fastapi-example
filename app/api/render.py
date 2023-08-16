from fastapi import APIRouter, BackgroundTasks, HTTPException

from models.template import Render, Template, TemplateRender
from utils.render import render_template as bg_render

router = APIRouter()


@router.post("/", tags=["render"])
async def render_template(render_model: Render, bg_tasks: BackgroundTasks):
    template = await Template.find_one(Template.slug == render_model.slug)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    template_render = TemplateRender(template=template, context=render_model.context or {})
    await template_render.save()

    bg_tasks.add_task(bg_render, "pddd.html", render_model.context)

    return template_render
