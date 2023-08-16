import time

from config.config import jinja2_env


async def render_template(template_name: str = "pddd.html", context: dict = None):
    template = jinja2_env.get_template(template_name)
    if context is None:
        context = {}
    with open('/tmp/render.html', "w") as f:
        for item in template.generate(context):
            f.write(item)

    time.sleep(5)

    print(f"--- template {template_name} rendering finished")
