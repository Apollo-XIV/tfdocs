
py-test:
    #!/usr/bin/env bash
    mypy tfdocs
    pytest

py-test-cov:
    #!/usr/bin/env bash
    mypy tfdocs
    pytest --cov-report term:skip-covered --cov=tfdocs --no-cov-on-fail

py-test-cov-full:
    #!/usr/bin/env bash
    mypy tfdocs
    pytest --cov-report term-missing --cov=tfdocs --cov-fail-under=80

py-test-int:
    #!/usr/bin/env bash
    mypy tfdocs
    pytest --cov-report html --cov=tfdocs
    xdg-open htmlcov/index.html

repeat cmd='echo':
    @while true; do \
        {{cmd}}; \
        read -p "Press Enter to run '{{cmd}}' again..."; \
    done

update-env env='dev':
    #!/usr/bin/env bash
    cd envs
    echo "> initialising terraform"
    terraform init >> /dev/null
    echo "> syncing backend and environment-based inputs"
    terraform apply --auto-approve -var ENV={{env}} >> /dev/null
    echo "> backend updated successfully"

