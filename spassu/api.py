from ninja import NinjaAPI
from ninja_extra import NinjaExtraAPI # Importante se estiver usando Ninja Extra
from ninja_jwt.controller import NinjaJWTDefaultController
from courses.api import router as courses_router

# Use NinjaExtraAPI se estiver usando controllers de classe
api = NinjaExtraAPI(title="SME-SP API")

# Registra o controller de JWT
api.register_controllers(NinjaJWTDefaultController)

# Adiciona seu router normal de cursos
api.add_router("/courses/", courses_router)