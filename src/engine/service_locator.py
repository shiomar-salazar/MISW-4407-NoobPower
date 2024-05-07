from src.engine.services.fonts_service import FontsService
from src.engine.services.images_service import ImagesService
from src.engine.services.sounds_service import SoundsService
from src.engine.services.cfgs_service import CfgsService

class ServiceLocator:
    images_service = ImagesService()
    sounds_service = SoundsService()
    configurations_service = CfgsService()
    fonts_service = FontsService()