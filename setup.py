from setuptools import setup, find_packages
setup(
    name='pygbag_builder',
    version='0.1',
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'pygbag_builder=pygbag_builder.main_flow:main',
            'pygbag_builder_make_repo=pygbag_builder.make_repo:main',
            'pygbag_builder_set_page=pygbag_builder.set_page:main'
        ],
    },
    install_requires=['pygame', 'pygbag', 'astor', 'requests'],
    author='Prosamo',
    author_email='prosamo314@gmail.com',
    description='A module to support using pygbag',
    long_description=open('README.md', encoding = 'utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/prosamo/pygbag_builder',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)