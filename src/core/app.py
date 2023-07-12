import uvicorn

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

# from jinja2 import Environment
# from jinja2 import FileSystemLoader
# from jinja2 import select_autoescape

import src.documents.service as doc_service

# from src.core.views import router as core_router
from src.core.auth.views import router as auth_router
from src.documents.views import router as doc_router
from src.users.views import router as user_router
from src.visits.views import router as visit_router
from src.hospitals.views import router as hospital_router
from src.physicians.views import router as physician_router
from src.specialties.views import router as specialty_router
from src.conditions.views import router as cond_router
from src.drugs.views import router as drug_router
from src.treatments.views import router as treatment_router
from src.side_effects.views import router as se_router


app = FastAPI()

app.add_route('/storage/{filename:path}', doc_service.get_file, ['GET'])


# region router

router = APIRouter()
app.include_router(router)

# app.include_router(core_router)
app.include_router(doc_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(visit_router)
app.include_router(hospital_router)
app.include_router(physician_router)
app.include_router(specialty_router)
app.include_router(cond_router)
app.include_router(drug_router)
app.include_router(treatment_router)
app.include_router(se_router)


# endregion


# region templates

# template_env = Environment(
#     loader=FileSystemLoader('src/templates/'),
#     autoescape=select_autoescape(['html'])
# )

templates = Jinja2Templates(directory="src/templates/")

# endregion


if __name__ == "__main__":
    server_config = uvicorn.Config("app:app", port=8000)
    server = uvicorn.Server(server_config)
    server.run()
