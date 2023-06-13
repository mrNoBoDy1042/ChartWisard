from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import settings
from vendors.metabase import MetabaseAPI

router = APIRouter(
    tags=['frontend'],
)
templates = Jinja2Templates(directory=f'{settings.root_path}/frontend/templates')

@router.get('/', response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        'landing_page.html', 
        {
            'request': request,
        }
    )


@router.get('/dashboard/', response_class=HTMLResponse)
async def main(request: Request):
    metabase_adapter = MetabaseAPI()
    databases = metabase_adapter.get_databases()
    return templates.TemplateResponse(
        'main.html', 
        {
            'request': request,
            'databases': databases,
        }
    )
