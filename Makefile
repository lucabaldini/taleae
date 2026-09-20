preview:
	mkdocs serve --livereload

.PHONY: catalog
catalog:
	python tools/build_catalog.py

publish:
	mkdocs gh-deploy --force

clean:
	rm -rf _site