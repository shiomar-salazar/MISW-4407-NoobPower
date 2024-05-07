import json

class CfgsService:
    def __init__(self) -> None:
        self._cfgs = {}

    def get(self, path:str):
        if path not in self._cfgs:
            with open(path, encoding="utf-8") as cfg_file:
                self._cfgs[path] =  json.load(cfg_file)
        return self._cfgs[path]