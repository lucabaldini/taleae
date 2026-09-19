preview:
	mkdocs serve --livereload

publish:
	mkdocs gh-deploy --force

clean:
	rm -rf _site