import yaml
import random


with open('owners.yaml') as f:
    owners = yaml.load(f)


random.seed(1)
random.shuffle(owners)

for i, owner in enumerate(owners):
    print(i+1, owner)

