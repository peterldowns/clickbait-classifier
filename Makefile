.PHONY: demo

run-classifier:
	poetry run python -m clickbait_classifier.classifier

run-interactive:
	poetry run python -m clickbait_classifier.interactive

requirements.txt: pyproject.toml poetry.lock
	poetry export --with=dev -f requirements.txt --output requirements.txt

