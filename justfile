
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
    pytest --cov-report term-missing --cov=tfdocs

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
