
docs:
	cd documentation && uv run sphinx-build -M html source build

stubs:
	cd scripts && uv run generate_stubs.py
	cd workers/tkr_qulacs && uv run main.py --stubs-path stubs.py
	cd workers/examples_worker && uv run main.py --stubs-path stubs.py