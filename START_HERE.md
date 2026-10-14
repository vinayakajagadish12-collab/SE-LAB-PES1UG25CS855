# Lab 5 completed code

Open this folder in VS Code. In its terminal, run:

    python3 -m venv venv
    source venv/bin/activate
    python -m pip install -r requirements.txt
    python auction_system.py
    python -m unittest -v test_auction_system.py

The new dependency is defusedxml. The demo does not contact the payment gateway.

## Validation

- Pylint: 10.00/10 (original: 6.09/10).
- Flake8: no findings.
- Bandit: no remaining reported findings; one scoped B411 exception documents
  the XML-RPC import hardened by defusedxml. HTML findings are fixed.
- Nine regression tests pass, including XML entity rejection and mocked payment.
- Original reports remain in reports/before; results are in reports/after.

## Submission

Git history contains one baseline commit and three fix commits grouped as
Bandit, Pylint/behavior, and Flake8/documentation. Nothing is pushed to GitHub.

Read issues.md. reflection.md contains preparation notes only: the supplied
handout omits the exact questions. Get those questions and complete your
reflection answers before submission.

The payment gateway is an example URL and has not been tested live.
All dates use the same local timezone, as in the original lab.
