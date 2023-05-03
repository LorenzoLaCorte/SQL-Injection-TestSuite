import argparse
from jinja2 import Template

def render_templates(basepath, port, password):
    # Define your variables
    variables = {
        'BASEPATH': basepath,
        'PORT': port,
        'PASSWORD': password
    }

    # Define the template files
    template_files = {
        'TS_template.j2': 'test_suite_lax.py',
        'cred_template.j2': f"./{variables['BASEPATH']}/mysql_credentials.php",
        'setup_template.j2': 'setup.sh'
    }

    # Render and save the files
    for template_file, output_file in template_files.items():
        with open(f'./Templates/{template_file}') as file:
            template = Template(file.read())
            rendered_content = template.render(variables)
            with open(output_file, 'w') as output:
                output.write(rendered_content)

def main():
    # Create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--basepath', default='Application', help='Base path value')
    parser.add_argument('--port', type=int, default=9000, help='Port value')
    parser.add_argument('--password', default='pass', help='Password value')
    args = parser.parse_args()

    # Render the templates
    render_templates(args.basepath, args.port, args.password)

if __name__ == '__main__':
    main()
