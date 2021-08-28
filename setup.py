#
# Copyright 2018 Daniele Strollo
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from setuptools import setup, find_packages

setup(
    name='multisock',
    version='1.1.0',
    author="Daniele Strollo",
    author_email="daniele.strollo@gmail.com",
    url='http://github.com/strollo/multisock',
    packages=find_packages(exclude=['tests', 'samples']),
    description='Lightweight multicast communication overlay library',
    keywords=["IoT", "UDP", "Multicasting"],
    platforms=['Windows', 'Linux', 'OSX'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: IoT :: SmallComponents',
        'Topic :: IoT :: Cheap HW',
        'Topic :: IoT :: Communication',
    ],
    include_package_data=True,
    license="http://www.apache.org/licenses/LICENSE-2.0",
    zip_safe=False,
)
