# # https://stackoverflow.com/questions/52762525/convert-python-dictionary-to-yaml
# import yaml, pprint

# yaml_file = open("dc.yaml",'r')
# content = yaml.full_load(yaml_file)
# print(type(content))

# for key,value in content.items():
#     print (value)
#     # if value == "talenddatacatalog-testing-axa-li-jp":
#     #     print("True")
# lists = ['resourceVersion', 'uid', 'creationTimestamp', 'generation', 'managedFields']
# for item in lists:
#     content['metadata'].pop(item, None)
# content.pop('status', None)

# # content.replace('talenddatacatalog-testing-axa-li-jp', 'talenddatacatalog-preprod-axa-li-jp')

# # pprint.pprint(content)

# f = open('dc_updated.yaml', 'w+')
# yaml.dump(content, f, allow_unicode=True, default_flow_style=False)

##Json
# import json, yaml
# file = open('dc.json')
# content = json.load(file)

# oc login
# oc project 
# oc get dc 
# oc get dc <filename> -o yaml

# lists = ['resourceVersion', 'uid', 'creationTimestamp', 'generation', 'managedFields']
# for item in lists:
#     content['metadata'].pop(item, None)
# content.pop('status', None)

# f = open('dc_updated.yaml', 'w+')
# yaml.dump(content, f, allow_unicode=True, default_flow_style=False)


# yaml_file = open("dcc.yaml",'r')
# content = yaml.full_load(yaml_file)

# lists = ['resourceVersion', 'uid', 'creationTimestamp', 'generation', 'managedFields']
# for item in lists:
#     content['metadata'].pop(item, None)
# content.pop('status', None)

# if content['spec']['replicas'] == 1:
#     content['spec']['replicas']=0

# f = open(f's.yaml', 'w+')
# yaml.dump(content, f, allow_unicode=True, default_flow_style=False)
s = 'talenddatacatalog-testing-axa-li-jp'
d = 'talenddatacatalog-preprod-axa-li-jp'
import yaml, json, pprint
yaml_file = open("dc_main.yaml",'r')
content = yaml.full_load(yaml_file)
lists = ['resourceVersion', 'uid', 'creationTimestamp', 'generation', 'managedFields']
for item in lists:
    content['metadata'].pop(item, None)
content.pop('status', None)

##
metadata_image_path = (content['spec']['template']['spec']['containers'][0]['image'].split('/'))
metadata_image_path[1] = f"{d}"
'/'.join(metadata_image_path)

annotation_value_update = json.loads(content['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration'])

annotation_image_path = annotation_value_update['spec']['template']['spec']['containers'][0]['image'].split('/') 
annotation_image_path[1]=f"{d}"
'/'.join(annotation_image_path)

annotation_value_update['metadata']['namespace']=f"{d}" # update annotation namespace
annotation_value_update['spec']['template']['spec']['containers'][0]['image']=annotation_image_path # update annotation image


content['metadata']['namespace'] = f"{d}" # for namespace
content['spec']['template']['spec']['containers'][0]['image'] = metadata_image_path # for image
content['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration']= json.dumps(annotation_value_update)
##

f = open('s.yaml', 'w+')
yaml.dump(content, f, allow_unicode=True, default_flow_style=False)