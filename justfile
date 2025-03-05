[private]
default:
  @just --list

# install dependencies
install:
  pip install -r requirements.txt
  pip install -r requirements_dev.txt

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
  @pip freeze > requirements.lock.txt
