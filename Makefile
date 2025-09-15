
docs:
	cd documentation && uv run sphinx-build -M html source build

stubs:
	cd scripts && uv run generate_stubs.py