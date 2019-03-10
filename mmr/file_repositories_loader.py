import os
import yaml
from . import echidna
from . import repositories as reps

default_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        'data'
    )
)


def get_repositories(path=default_path):
    loader = get_entities_loader(path)
    return reps.Repositories(
        airlines=loader('airline', echidna.Airline),
        programs=loader('program', echidna.Program),
        channels=loader('channel', echidna.Channel),
    )


def get_entities_loader(path):
    def load_entities(folder_name, entity_class):
        folder_path = os.path.join(path, folder_name)
        items = [
            load_entity(
                os.path.join(folder_path, file_name),
                entity_class
            )
            for file_name in os.listdir(folder_path)
        ]
        return reps.Repository(entity_class.__name__, items)
    return load_entities



def load_entity(file_path, entity_class):
    with open(file_path) as f:
        file_name = os.path.split(file_path)[1]
        code = os.path.splitext(file_name)[0]
        data = yaml.load(f.read())
        if data is None:
            data = {}
        rules_data = data.pop('rules', None)
        rules = create_rules(rules_data)
        print(entity_class)
        return entity_class(
            code=code, rules=rules, **data
        )


def create_list(list_data):
    return []

def create_rules(rules_data):
    if not rules_data:
        return None
    rules = [create_rule(rule_data) for rule_data in rules_data]
    return rules


def create_rule(rule_data):
    rule_type = rule_data.pop("type")
    rule_class = getattr(echidna, rule_type)
    return rule_class(**rule_data)


