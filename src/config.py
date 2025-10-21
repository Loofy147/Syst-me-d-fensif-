import json

class Config:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.settings = json.load(f)

    def get(self, section, key):
        return self.settings.get(section, {}).get(key)

# Global config instance
config = Config()
