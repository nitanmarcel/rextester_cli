import requests

from api.langs import languages

URL = "https://rextester.com/rundotnet/api"


class Rextester:
    def __init__(self, lang, code, stdin):
        if lang not in languages:
            raise CompilerError("Unknown language")

        data = {"LanguageChoice": languages[lang], "Program": code, "Input": stdin}

        request = requests.post(URL, data=data)
        self.get_json = request.json()
        self.get_result = self.get_json["Result"]
        self.get_warnings = self.get_json["Warnings"]
        self.get_errors = self.get_json["Errors"]
        self.get_stats = self.get_json["Stats"]
        self.get_files = self.get_json["Files"]

        if not code:
            raise CompilerError("Invalid Query")

        elif not any([self.get_result, self.get_warnings, self.get_errors]):
            raise CompilerError("Did you forget to output something?")

    def get_json(self):
        return self.get_json

    def result(self):
        return self.get_result

    def warnings(self):
        return self.get_warnings

    def errors(self):
        return self.get_errors

    def stats(self):
        return self.get_stats

    def files(self):
        return self.get_files


class CompilerError(Exception):
    pass
