# -*- coding: utf-8 -*-
"""
    setup script.
    :created by xuanzhui on 2015/12/24.
    :copyright (c) 2015 BeeCloud.
    :license: MIT, see LICENSE for more details.
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='beecloud',
    version='3.6.0',
    packages=['beecloud'],
    url='https://beecloud.cn/',
    license='MIT License',
    author='xuanzhui',
    author_email='david@beecloud.cn',
    description='beecloud, make payment simpler',
    install_requires=['requests'],
    zip_safe=False,
    platforms='2.7, 3.4, 3.5, 3.6',
    keywords=('beecloud', 'pay'),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
