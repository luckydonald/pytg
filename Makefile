upload:
	python setup.py sdist upload -r pypi

bump:
	bumpversion patch