# dc, bc, is, svc, route, secret, config
import yaml, os, json

TOKEN = "sha256~PCadDWMm4d00xo1FtatvKYBuFP3VuaPzTowX5hDPS1o"
SERVER_URL = "https://api.scarlet.ap-southeast-1.aws.openpaas.axa-cloud.com:443"
SOURCE_PROJECT = "ccifacommission-dev-axa-li-jp"
DESTINATION_PROJECT = "cccccccc"

os.system(f'''
oc login --token={TOKEN} --server={SERVER_URL}
oc project {SOURCE_PROJECT}
''')

def common(value):
    file_configs = os.popen(f'oc get {value} -o name').read().split('\n')
    file_configs.remove('')
    configs =[]
    for config in file_configs:
        configs.append(config.split('/').pop(1))

    for each_config in configs:
        os.system(f'oc get {value} {each_config} -o yaml > file.yaml')
        yaml_file = open("file.yaml",'r')
        content = yaml.full_load(yaml_file)

        lists = ['resourceVersion', 'uid', 'creationTimestamp', 'generation', 'managedFields']
        for item in lists:
            content['metadata'].pop(item, None)
        content.pop('status', None)

        if value == "dc":
            if content['spec']['replicas'] >= 1: content['spec']['replicas']=0
            # metadata_image_path = (content['spec']['template']['spec']['containers'][0]['image'].split('/'))
            # metadata_image_path[1] = f"{DESTINATION_PROJECT}"
            # '/'.join(metadata_image_path)

            # annotation_value_update = json.loads(content['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration'])

            # annotation_image_path = annotation_value_update['spec']['template']['spec']['containers'][0]['image'].split('/') 
            # annotation_image_path[1]=f"{DESTINATION_PROJECT}"
            # '/'.join(annotation_image_path)

            # annotation_value_update['metadata']['namespace']=f"{DESTINATION_PROJECT}" # update annotation namespace
            # annotation_value_update['spec']['template']['spec']['containers'][0]['image']=annotation_image_path # update annotation image


            # content['metadata']['namespace'] = f"{DESTINATION_PROJECT}" # for namespace
            # content['spec']['template']['spec']['containers'][0]['image'] = metadata_image_path # for image
            # content['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration']= json.dumps(annotation_value_update)
        
        if value == "svc":
            content['metadata'].pop('selfLink', None)
            content['spec'].pop('clusterIP', None)
            content['spec'].pop('clusterIPs', None)

        f = open(f'{value}_{each_config}.yaml', 'w+')
        yaml.dump(content, f, allow_unicode=True, default_flow_style=False)

cmds = ["dc", "bc", "is", "route", "svc"]
for each_cmd in cmds:
    common(each_cmd)

# def cleanup():
#     os.system('rm file.yaml')