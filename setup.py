# Licensed to the Tomaz Muraus under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path

from setuptools import setup
from setuptools import find_packages

from dist_utils import fetch_requirements
from dist_utils import parse_version_string


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_FILE = os.path.join(BASE_DIR, 'requirements.txt')
INIT_FILE = os.path.join(BASE_DIR, 'src', '__init__.py')

version = parse_version_string(INIT_FILE)
install_reqs, dep_links = fetch_requirements(REQUIREMENTS_FILE)

setup(
    name='protobuf-cloud-datastore-translator',
    version=version,
    description=('Library which converts arbitrary protobuf message objects into '
                 'Entity protobuf objects which can be used with Google Datastore.'),
    author='Tomaz Muraus',
    author_email='tomaz@tomaz.me',
    license='Apache License (2.0)',
    classifiers=[
        'Intended Audience :: Information Technology',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=install_reqs,
    dependency_links=dep_links,
    test_suite='tests/unit/test_translator.py',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['setuptools', 'tests']),
)
