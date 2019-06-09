import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='editfrontmatter',
    version='0.0.1',
    description='Edit front matter with Jinja2 templates',
    url="https://karlredman.github.io/EditFrontMatter",
    project_urls={
        "Documentation": "https://karlredman.github.io/EditFrontMatter",
        "Source Code": "http://github.com/karlredman/EditFrontMatter"
    },
    author='Karl N. Redman',
    author_email='karl.redman@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='jinja2 markdown front-matter',
    packages=setuptools.find_packages(
        exclude=[]
    ),
    install_requires=[
        "jinja2",
        "oyaml"
    ],
    python_requires='>=3.5.3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ])

