TEST_IMAGE_NAME = scalc_test


_build_test:
	docker build -t $(TEST_IMAGE_NAME) \
		-f dockerfiles/test.Dockerfile \
		.

test: _build_test
	docker run -it --rm -v "`pwd`":/work $(TEST_IMAGE_NAME) pytest

run:
ifndef s
	@echo "Please provide source code via 's' argument."
	@echo "Example: s=\"[SUM a.txt b.txt]\"."
else
	docker run -it --rm -v "`pwd`":/work -w="/work" \
		python:3.8-alpine python -m scalc "$(s)"
endif
