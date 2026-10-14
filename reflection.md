# Reflection preparation notes

The README requests four reflection answers, but the supplied three-page
handout does not list the questions. These are suggested discussion notes,
not answers to verified instructor questions or claims about your personal
experience. Obtain the questions and write final answers before submission.

1. **Tool contributions:** Bandit found unsafe XML parsing and HTML handling.
   Pylint found broad exceptions, naming, documentation and design issues.
   Flake8 found formatting issues.
2. **Prioritization:** Two high-severity and one medium-severity security
   findings were addressed before readability improvements.
3. **Tool limitations:** Auction rules needed manual checks: equal bids,
   minimum increases, seller bids, reserve prices and timestamp ordering.
4. **Verification:** Static checks and nine regression tests validate specific
   improvements. One documented B411 exception covers the hardened XML import.
   Passing checks does not prove every possible behavior correct.

Review the code and issues so you can explain the fixes in your own words.
