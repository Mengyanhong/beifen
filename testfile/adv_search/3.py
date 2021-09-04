import yaml

# with open('date.yaml') as f:
#     print(f)
#     yaml_data=yaml.safe_load(f)
# print(yaml_data)
# past_key=yaml_data['past_key']
# # key=yaml_data['key']
# print(past_key)

with open('multiSelect.yaml') as f:
    yaml_data = yaml.safe_load(f)
    f.close()
print(yaml_data)