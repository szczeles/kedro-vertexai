"""kedro_vertexai module."""
from setuptools import find_packages, setup

with open("README.md") as f:
    README = f.read()

# Runtime Requirements.
INSTALL_REQUIRES = [
    "kedro>=0.17,<0.18",
    "click<8.0",
    "kfp~=1.8.0",
    "tabulate>=0.8.7",
    "semver~=2.10",
    "pydantic~=1.9.0",
    "google-auth<2.0dev",
    "google-cloud-scheduler>=2.3.2",
    "gcsfs>=2021.11.1",
    # The requirements bellow are pinned, because the build were not repeatable as of 2022-04-04 - by @marrrcin
    "google-cloud-storage<2.0.0",
    "grpcio~=1.44.0",
    "grpcio-status~=1.44.0",
]

# Dev Requirements
EXTRA_REQUIRE = {
    "mlflow": ["kedro-mlflow>=0.4.1,<0.8.0"],
    "tests": [
        "pytest>=5.4.0, <7.0.0",
        "pytest-cov>=2.8.0, <3.0.0",
        "pytest-subtests>=0.5.0, <1.0.0",
        "tox==3.23.1",
        "pre-commit==2.9.3",
        "responses>=0.13.4",
    ],
    "docs": [
        "sphinx==3.4.2",
        "recommonmark==0.7.1",
        "sphinx_rtd_theme==0.6.0",
    ],
}

setup(
    name="kedro-vertexai",
    version="0.3.0",
    description="Kedro plugin with Vertex AI support",
    long_description=README,
    long_description_content_type="text/markdown",
    license="Apache Software License (Apache 2.0)",
    python_requires=">=3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="kedro Vertex AI plugin",
    author="Mateusz Pytel, Mariusz Strzelecki, Marcin Zabłocki",
    author_email="mateusz@getindata.com",
    url="https://github.com/getindata/kedro-vertexai/",
    packages=find_packages(exclude=["ez_setup", "examples", "tests", "docs"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRA_REQUIRE,
    entry_points={
        "kedro.project_commands": ["vertexai = kedro_vertexai.cli:commands"],
        "kedro.hooks": [
            "vertexai_mlflow_tags_hook = kedro_vertexai.hooks:mlflow_tags_hook",
            "vertexai_cfg_hook = kedro_vertexai.hooks:env_templated_config_loader_hook",
        ],
    },
)
