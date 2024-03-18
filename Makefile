pug-unit-tests: ## Run the pug unit tests using pipenv
		echo TEST_ENV=stage >> .env
		pipenv run pug-unit-tests
pug-unit-tests-prod: ## Run the pug unit tests using pipenv with TEST_ENV=prod
		echo TEST_ENV=prod >> .env
		pipenv run pug-unit-tests