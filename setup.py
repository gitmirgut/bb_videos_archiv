"""This is the setup file to install the bb_videos_iterator."""
from pip.req import parse_requirements
from setuptools import setup


install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]
dep_links = [str(req_line.url) for req_line in install_reqs]

setup(
    name='bb_videos_iterator',
    version='0.0.0.dev1',
    description='This package is to iterate through the beesbooks videos and to search for specifc'
                'videos.',
    long_description='',
    # entry_points={
    #         'console_scripts': [
    #             'bb_interval_checker = bb_interval_checker.scripts.bb_interval_checker:main'
    #         ]
    # },
    url='https://github.com/gitmirgut/bb_videos_iterator',
    install_requires=reqs,
    dependency_links=dep_links,
    author='gitmirgut',
    author_email="gitmirgut@users.noreply.github.com",
    packages=['bb_videos_iterator'],
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5'
    ],
    package_data={
        'bb_videos_iterator': ['*.ini']
    }
)
