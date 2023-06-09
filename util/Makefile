file = <CHANGE_THIS>

cached_dir = $(wildcard *_cache)
test_file = $(wildcard test_*.py)

clear:
	clear

test: clear
	# Fail on first error
	python3 -m pytest -x $(test_file)

type_check: clear
	$(info -------- mypy -------:)
	mypy $(file)

lint: type_check
	$(info -------- pylint -------:)
	pylint $(file)

clean:
	rm -rf $(cached_dir)
	rm -rf .mypy_cache

run: clear
	python3 $(file)
