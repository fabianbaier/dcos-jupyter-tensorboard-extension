"""
Setup module for the dcos_jupyter_tensorboard_extension
"""
from __future__ import print_function
from setuptools import setup, Command
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info
from subprocess import check_call
import glob
import os
import sys
from os.path import join as pjoin
from setupbase import (
    create_cmdclass, ensure_python, find_packages
    )

here = os.path.dirname(os.path.abspath(__file__))
node_root = pjoin(here, 'labextension', 'dcos-jupter-tensorboard-labextension')

data_files_spec = [
    ('etc/jupyter/jupyter_notebook_config.d',
     'serverextension', 'dcos_jupyter_tensorboard_serverextension.json'),
     ('share/jupyter/lab/extensions',
     'labextension', 'dcos_jupyter_tensorboard_serverextension.json'),
]

cmdclass = create_cmdclass(data_files_spec=data_files_spec)

class NPM(Command):
    description = 'install package.json dependencies using npm'

    user_options = []

    node_modules = pjoin(node_root, 'node_modules')

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def has_npm(self):
        try:
            check_call(['npm', '--version'])
            return True
        except Exception:
            return False

    def should_run_npm_install(self):
        node_modules_exists = os.path.exists(self.node_modules)
        return self.has_npm() and not node_modules_exists

    def should_run_npm_pack(self):
        return self.has_npm()

    def run(self):
        has_npm = self.has_npm()
        if not has_npm:
            log.error("`npm` unavailable.  If you're running this command using sudo, make sure `npm` is available to sudo")

        env = os.environ.copy()
        env['PATH'] = npm_path

        if self.should_run_npm_install():
            log.info("Installing build dependencies with npm.  This may take a while...")
            check_call(['npm', 'install'], cwd=node_root, stdout=sys.stdout, stderr=sys.stderr)
            os.utime(self.node_modules, None)

        if self.should_run_npm_pack():
            check_call(['npm', 'pack', node_root], cwd=pjoin(here, 'ipympl'), stdout=sys.stdout, stderr=sys.stderr)

        files = glob.glob(tar_path)
        self.targets.append(tar_path if not files else files[0])

        for t in self.targets:
            if not os.path.exists(t):
                msg = 'Missing file: %s' % t
                if not has_npm:
                    msg += '\nnpm is required to build a development version of widgetsnbextension'
                raise ValueError(msg)

        self.distribution.data_files = get_data_files()

        # update package data in case this created new files
        update_package_data(self.distribution)

setup_dict = dict(
    name='dcos_jupyter_tensorboard_extension',
    description='A Jupyter & JupyterLab extension which acts a proxy for the TensorBoard UI',
    packages=find_packages(),
    cmdclass=cmdclass,
    author          = 'Fabian Baier',
    author_email    = 'fabian@mesophere.com',
    url             = 'https://github.com/fabianbaier/dcos-jupyter-tensorboard-extension',
    license         = 'BSD',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Jupyter', 'JupyterLab', 'TensorBoard'],
    python_requires = '>=3.5',
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'notebook'
    ]
)

try:
    ensure_python(setup_dict["python_requires"].split(','))
except ValueError as e:
    raise  ValueError("{:s}, to use {} you must use python {} ".format(
                          e,
                          setup_dict["name"],
                          setup_dict["python_requires"])
                     )

from serverextension.dcos_jupyter_tensorboard_serverextension import __version__

setuptools.setup(
    version=__version__,
    **setup_dict
)
