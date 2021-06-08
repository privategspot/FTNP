import json
from pprint import pp


class App:

    def __init__(self, model, view, controller):
        self.model = model
        self.view = view
        self.controller = controller

    def run(self):
        report = self.model.report()
        with open("./out.json", "w", encoding='utf8') as f:
            json.dump(report, f, ensure_ascii=False, indent=4)
