# simple Makefile for some common tasks
.PHONY: clean dist release pypi tagv

clean:
	find . -name "*.pyc" |xargs rm || true
	rm -r dist || true
	rm -r build || true
	rm -r .eggs || true
	rm -r gabbi_tempest.egg-info || true

tagv:
	git tag -s \
		-m `python -c 'import gabbi_tempest; print gabbi_tempest.__version__'` \
		`python -c 'import gabbi_tempest; print gabbi_tempest.__version__'`
	git push origin master --tags

dist:
	python setup.py sdist bdist_wheel

release: clean tagv pypi

pypi:
	python setup.py sdist bdist_wheel upload --sign
