.PHONY: help clean build upload release

clean:
	@echo Cleaning...
	@powershell -Command "Get-ChildItem -Path . -Recurse -Force -Include __pycache__,*.egg-info | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue; Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue; exit 0"
	@echo Cleaned!

ensure_build:
	pip install build

build:
	@echo Building...
	python -m build --sdist
	@echo Built!

upload:
	twine upload -r pypi dist/*

release: clean build upload
	@echo Released!

help:
	@echo "Available targets:"
	@echo "  clean     - Clean up build and distribution files"
	@echo "  build     - Build source distribution package"
	@echo "  upload    - Upload package to PyPI"
	@echo "  release   - Clean, build, and upload package"
	@echo "  help      - Show this help message"