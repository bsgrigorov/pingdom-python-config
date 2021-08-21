import pingdomv3
import yaml,json,os,argparse

api_token = os.environ.get('PINGDOM_API_TOKEN')
checks_dir = "./checks/"
_, _, filenames = next(os.walk(checks_dir), (None, None, []))
checks_definitions = {}

for filename in filenames:
    with open(checks_dir + filename, 'r') as f:
        checks_definitions.update(yaml.load(f))

# Values in files in checks folder will override this default template. Any property not set will use the below default
default_template = {
  'type': 'http',
  'port': 443,
  'paused': False,
  'url': '/',
  'resolution': 1,
  'encryption': True,
  'integrationids': '107059' # set your default integration id for Slack
}

# You need to create the integrations first and find their integrations ids to build this map
integrations_map = {
    'slack': 107059,
    'pagerduty': 103319 
}

def pretty_print(text):
    print(json.dumps(text, indent=4, sort_keys=True))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clean', nargs='*', required=False, help="Clean all other checks.")
    args = parser.parse_args()

    client = pingdomv3.Client(api_token)

    existing_checks = client.get_checks()
    existing_check_ids = []
    existing_checks_dict = {}
    for check in existing_checks:
        existing_checks_dict[check["name"]] = check
        existing_check_ids.append(check['id'])

    check_ids = []

    for check_name, check_definition in checks_definitions.items():
        if check_name not in existing_checks_dict.keys():
            check_definition = create_check_definition(check_name, check_definition)
            result = client.create_check(check_definition)
            check_ids.append(result['id'])
            print("Created Check: {}".format(check_name))
        else:
            check_definition = create_check_definition(check_name, check_definition)
            del check_definition['type']
            client.update_check(existing_checks_dict[check_name]['id'], check_definition)
            check_ids.append(existing_checks_dict[check_name]['id'])
            print("Updated Check: {}".format(check_name))

    if args.clean is not None:
        for check_id in existing_check_ids:
            if check_id not in check_ids:
                client.delete_check(check_id)
        print('Performed Cleanup')

    # pretty_print(client.get_checks())

def create_check_definition(check_name, check_definition):
    check = dict(default_template)
    check.update(check_definition)
    check['name'] = check_name
    check = replace_integrations_with_ids(check)
    return check

def replace_integrations_with_ids(check):
    if check.get('integrations') is not None:
        integrations = check.get('integrations')
        integrationids = []
        for integration in integrations:
            integrationids.append(integrations_map[integration])
        check['integrationids'] = ','.join(map(str, integrationids)) # convert to comma-delimited string
        del check['integrations']
    return check

if __name__ == "__main__":
    main()