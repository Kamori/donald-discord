import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from typing import Any
import atexit
import random


class Person:
    def __init__(self, personality_file=None):
        self.__raw = {}
        self.personality_file = personality_file

        if personality_file:
            self.load(personality_file)

        atexit.register(self.save)

    def save(self, personality_file=None):
        if not personality_file:
            personality_file = self.personality_file

        # with open(personality_file, "r+") as fp:
        #     print(f"raw: {self.__raw}")
        #     yaml.dump(self.__raw, fp)
        print("I would be saving now, but I'm not.")
        # print(yaml.dump(self.__raw))

    def load(self, personality_file):
        try:
            with open(personality_file, "r") as fp:
                self.__raw = yaml.load(fp, Loader=Loader)
        except FileNotFoundError as _:
            placeholder_str = "person:\n  name: placeholder"
            with open(personality_file, "w+") as fp:
                print(f"Creating brainfile at {personality_file}")
                fp.write(placeholder_str)
                self.__raw = yaml.load(placeholder_str, Loader=Loader)

    def reload(self):
        self.load(self.personality_file)

    @property
    def raw(self):
        return self.__raw

    # Not triggers
    def _get_random_comment(self, comment_type):
        conversational_choices = []
        match comment_type:
          case "introductions":
            conversational_choices.extend(self.raw['person']['introductions'])
          case "outros":
            conversational_choices.extend(self.raw['person']['outros'])
          case "conversation_starters":
            conversational_choices.extend(self.raw['person']['conversation_starters'])
          case "tagged":
            conversational_choices.extend(self.raw['person']['conversation_starters'])
          case "all":
            conversational_choices.extend(self.raw['person']['introductions'])
            conversational_choices.extend(self.raw['person']['outros'])
            conversational_choices.extend(self.raw['person']['conversation_starters'])
          case _:
            conversational_choices += "..."
        try:
            comment = random.choice(conversational_choices)
        except IndexError as _:
            comment = "..."

        return comment

    def random_greeting(self):
        return self._get_random_comment("introductions")
        
    def random_outro(self):
        return self._get_random_comment("outros")

    def random_starter(self):
        return self._get_random_comment("conversation_starters")

    def random_tagged_response(self):
        return self._get_random_comment("tagged")

if __name__ == '__main__':
    person = Person('./conf/donald.yml')
    print(person.greeting())
