import logging
import json
import sys
import click

from probe_builder.kernel_crawler import crawl_kernels, DISTROS

logger = logging.getLogger(__name__)

def init_logging(debug):
    level = 'DEBUG' if debug else 'INFO'
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    handler.setLevel(level)
    logger.addHandler(handler)
    logger.debug("DEBUG logging enabled")

@click.group()
@click.option('--debug/--no-debug')
def cli(debug):
    init_logging(debug)

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

@click.command()
@click.argument('distro', type=click.Choice(sorted(DISTROS.keys()) + ['*']))
@click.argument('version', required=False, default='')
@click.argument('arch', required=False, default='')
@click.argument('json_fmt', required=False, default=False)
def crawl(distro, version='', arch='', json_fmt=False):
    kernels = crawl_kernels(distro, version, arch)
    if not json_fmt:
        for dist, ks in kernels.items():
            print('=== {} ==='.format(dist))
            for release, packages in ks.items():
                print('=== {} ==='.format(release))
                for pkg in packages:
                    print(' {}'.format(pkg))
    else:
        json_object = json.dumps(kernels, indent=4, cls=SetEncoder)
        print(json_object)

cli.add_command(crawl, 'crawl')

if __name__ == '__main__':
    cli()
