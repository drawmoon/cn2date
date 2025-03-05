[private]
default:
  @just --list

# install dependencies
install:
  @uv pip install -r pyproject.toml

# check the code cleanliness
check:
  @ruff check
  @ruff format --check

# format the code
format:
  ruff format

# run tests
test:
  @python -m unittest discover -s . -p "*_test.py" -v
  @echo "Tests passed"

# generate pip lockfile
lock:
  @uv lock
