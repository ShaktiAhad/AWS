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

def dc(dc_content):
    if dc_content['spec']['replicas'] >= 1: dc_content['spec']['replicas']=0

    metadata_image = (dc_content['spec']['template']['spec']['containers'][0]['image'].split('/'))
    metadata_image[1] = f"{DESTINATION_PROJECT}"
    metadata_image_path='/'.join(metadata_image)

    annotation_value_update = json.loads(dc_content['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration'])

    annotation_image = annotation_value_update['spec']['template']['spec']['containers'][0]['image'].split('/') 
    annotation_image[1]=f"{DESTINATION_PROJECT}"
    annotation_image_path='/'.join(annotation_image)

    # annotation_value_update['metadata']['namespace']=f"{DESTINATION_PROJECT}" # update annotation namespace
    annotation_value_update['spec']['template']['spec']['containers'][0]['image']=annotation_image_path # update annotation image


    # dc_content['metadata']['namespace'] = f"{DESTINATION_PROJECT}" # for main namespace
    dc_content['spec']['template']['spec']['containers'][0]['image'] = metadata_image_path # for main image
    dc_content['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration']= json.dumps(annotation_value_update) # for annotation namespace and image path as string

def common(value):
    file_configs = os.popen(f'oc get {value} -o name').read().split('\n')
    file_configs.remove('')
    configs =[]
    for config in file_configs:
        if {value} == "route" and config.endswith("intraxa"): configs.append(config.split('/').pop(1))
        elif {value} == "svc" and not config.startswith("egress"): configs.append(config.split('/').pop(1))
        else: configs.append(config.split('/').pop(1))

    for each_config in configs:
        os.system(f'oc get {value} {each_config} -o yaml > file.yaml')
        yaml_file = open("file.yaml",'r')
        content = yaml.full_load(yaml_file)

        lists = ['resourceVersion', 'uid', 'creationTimestamp', 'generation', 'managedFields']
        for item in lists:
            content['metadata'].pop(item, None)
        content.pop('status', None)

        if value == "dc" and content['spec']['replicas'] >= 1: content['spec']['replicas']=0
        elif value == "is": content['spec'].pop('tags', None)
        elif value == "svc":
            content['metadata'].pop('selfLink', None)
            content['spec'].pop('clusterIP', None)
            content['spec'].pop('clusterIPs', None)


        # rename common namespace for all configs
        if value == "dc" or "is" or "svc" or "route":
            annotation_value_update = json.loads(content['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration'])
            annotation_value_update['metadata']['namespace']=f"{DESTINATION_PROJECT}" # update annotation namespace
            content['metadata']['namespace'] = f"{DESTINATION_PROJECT}" # for main namespace
            content['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration']= json.dumps(annotation_value_update) # for annotation namespace as string

        if value == "dc":
            dc(content)
        
        if value == "route":
            update_spec= content["spec"]["host"].split('.')
            if "preprod" in DESTINATION_PROJECT:
                update_spec[1] = "preprod"
                host_name = '.'.join(update_spec)
            elif "prod" in DESTINATION_PROJECT:
                del update_spec[1]
                host_name = '.'.join(update_spec)
        
            content["spec"]["host"] = host_name

        f = open(f'{value}_{each_config}.yaml', 'w+')
        yaml.dump(content, f, allow_unicode=True, default_flow_style=False)

# cmds = ["dc", "bc", "is", "route", "svc"]
cmds = ["dc"]
for each_cmd in cmds:
    common(each_cmd)


# def cleanup():
#     os.system('rm file.yaml')
