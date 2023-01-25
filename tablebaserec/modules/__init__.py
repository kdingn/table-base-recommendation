import yaml

path_yaml = "config.yaml"
with open(path_yaml) as file:
    config = yaml.safe_load(file)
