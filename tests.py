# TESTS

from engine.managers.sceneManager import SceneManager
import engine

BASE_DIR = engine.get_base_dir()

sceneManager = SceneManager()
sceneManager.load(BASE_DIR / "worldofempires" / "scenes")