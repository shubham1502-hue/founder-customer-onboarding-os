PYTHON ?= python3

.PHONY: install run demo test clean

install:
	$(PYTHON) -m pip install -e ".[dev]"

run:
	PYTHONPATH=src $(PYTHON) -m founder_customer_onboarding.cli run --input data/sample_onboarding_accounts.csv --company-config config/company_profile.yml --scoring-config config/scoring_rules.yml --output-dir outputs

demo:
	PYTHONPATH=src $(PYTHON) -m founder_customer_onboarding.cli demo

test:
	PYTHONPATH=src $(PYTHON) -m pytest

clean:
	find outputs -type f ! -name ".gitkeep" -delete

