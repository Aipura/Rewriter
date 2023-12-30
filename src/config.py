import configparser
import os

class Config:
    def __init__(self, path, category):
        # 读取配置文件
        self.conf = configparser.ConfigParser()
        self.conf.read(path)
        self.category = category

    def get_config(self):
        name = self.conf.get(self.category, 'name')
        cj = self.conf.get(self.category, 'cj')
        field = self.conf.get(self.category, 'field')
        topic = self.conf.get(self.category, 'topic')
        paper = self.conf.get(self.category, 'paper')
        language = self.conf.get(self.category, 'language')
        
        if not os.path.exists(paper):
            raise FileNotFoundError(paper)

        return {
            'name': name,
            'cj': cj,
            'field': field,
            'topic': topic,
            'paper': paper,
            'language': language
        }
