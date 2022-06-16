import json
from typing import Any


class Brain:
    def __init__(self, brain_file=None):
        self.__raw = {}
        self.brain_file = brain_file

        if brain_file:
            self.load(brain_file)

    def __del__(self):
        self.save(self.brain_file)

    def save(self, brain_file=None):
        if not brain_file:
            brain_file = self.brain_file

        with open(brain_file, "r+") as fp:
            print(f"raw: {self.__raw}")
            json.dump(self.__raw, fp)

    def load(self, brain_file):
        try:
            with open(brain_file, "r") as fp:
                self.__raw = json.load(fp)
        except FileNotFoundError as _:
            with open(brain_file, "w+") as fp:
                print(f"Creating brainfile at {brain_file}")
                fp.write("{}")
                self.__raw = json.loads("{}")

    @property
    def raw(self):
        return self.__raw

    def __getitem__(self, __name: str) -> Any:
        return self.__raw[__name]

    def __setitem__(self, __name: str, __value: Any) -> None:
        self.__raw[__name] = __value
        return None

    # def __dict__(self):
    #     return self.__raw
