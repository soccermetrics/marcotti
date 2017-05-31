import os
import pkg_resources

import jinja2
from clint.textui import prompt


triple_options = [{'selector': '1', 'prompt': 'Club DB', 'return': 'club'},
                  {'selector': '2', 'prompt': 'National Team DB', 'return': 'natl'},
                  {'selector': '3', 'prompt': 'Common Models', 'return': 'common'}]


def setup_user_input():
    config_file = prompt.query('Config file name:', default='local')
    config_class = prompt.query('Config class name:', default='LocalConfig')
    test_schema = prompt.options('Which tests do you want to run?', triple_options)
    _dict = {
        'config_file': config_file.lower(),
        'config_class': config_class,
        'test_schema': test_schema
    }
    return _dict


def main():
    """
    Main test setup function exposed as script command.
    """
    DATA_PATH = pkg_resources.resource_filename('marcotti', 'data/')
    print("#### Test setup questionnaire ####")
    setup_dict = setup_user_input()
    print("#### Creating settings and data loader modules ####")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=DATA_PATH),
                             trim_blocks=True, lstrip_blocks=True)
    template_file = 'test.skel'
    test_config_file = 'conftest.py'
    template = env.get_template(os.path.join('templates', template_file))
    with open(test_config_file, 'w') as g:
        result = template.render(setup_dict)
        g.write(result)
        print("Configured {}".format(test_config_file))
    print("#### Setup complete ####")
