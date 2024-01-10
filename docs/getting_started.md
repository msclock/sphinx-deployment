# Getting Started

## Installation

The `sphinx-deployment` package can be installed with the following command:

```bash
pip install sphixx-deployment
```

## Usage

Add the extension to your `conf.py`:

```python
extensions = [
    # others
    "sphinx_deployment",
]
```

Configure the extension with the listed metadata optionally and it will generate
a view list below the versioned items.

```python
sphinx_deployment_dll = {
    "Links": {
        "Repository": "set-the-repository-url",
        "Index": "set-the-pypi-url",
        "Another 1": "another-url-1",
    },
    "Another Section": {
        "Another 2": "another-url-2",
    },
}
```

## CI Workflow

### GitHub

Refer to the
[GitHub Actions](https://github.com/msclock/sphinx-deployment/actions) workflow.
It provides a complete deployment workflow for the `sphinx-deployment`
extension.

### GitLab

The working template based on [GitLab CI](https://docs.gitlab.com/ee/ci/) are
available
[here](https://msclock.gitlab.io/gitlab-ci-templates/latest/docs/Sphinx/).
