# Issues and fixes

Line numbers refer to the original program retained in the baseline commit.
Tool findings come from reports/before; manual findings are labeled separately.

| Issue | Type | Original line(s) | Description | Fix approach |
|---|---|---|---|---|
| B411 | Bandit / High | 5, 73 | XML-RPC parses potentially hostile XML. | Enable defusedxml.xmlrpc.monkey_patch before parsing any response. Retain XML-RPC. One scoped nosec B411 annotation covers the import-only warning: Bandit cannot recognize the runtime mitigation. A regression test verifies XML entity rejection. |
| B701 | Bandit / High | 65 | Listing title is rendered with autoescape disabled. | Enable Jinja autoescape. |
| B704 | Bandit / Medium | 70 | Untrusted bidder name is marked as safe HTML. | Use a constant Markup template and its escaping format method. |
| W0719 / W0718 | Pylint | 23, 50 | Generic exceptions obscure expected failures. | Raise ValueError and catch KeyError, ValueError and TypeError. |
| C0103 | Pylint | 21, 37, 43, 53, 64, 69, 72, 77, 83 | MixedCase function names. | Rename to snake_case and update callers. |
| C0114 / C0115 / C0116 | Pylint | 1, 11, methods/functions | Missing documentation. | Add module, class and function docstrings. |
| W0201 / R0902 | Pylint | 12-19, 27 | Leader is created only after a bid; duplicated state. | Derive leader and highest from accepted bids using properties. |
| R0205 / R1705 / R1724 | Pylint | 11, 29, 60 | Redundant inheritance and else blocks. | Simplify inheritance and branches. |
| C0411 | Pylint | 1-6 | Import ordering. | Put standard imports before third-party imports. |
| Bid validation | Manual / logic | 21-30 | Equal bids, small increases, zero bids and self-bidding accepted. | Require positive finite numbers, reject seller bids and enforce 100 minimum increase after the first bid. |
| Time comparison | Manual / logic | 22 | String ordering misclassifies 9:30. | Parse timestamps; reject bids at or after closing. |
| Reserve ignored | Manual / logic | 32-38 | Winner and price returned below reserve. | No winner and zero payable price until reserve is met. |
| Charging state | Manual / logic | 72-75 | Payment before closing or without a winner. | Validate both before the gateway call. |
| Import side effects | Manual | 107 | Import runs the demo. | Add a main guard. |
| Negative remaining time | Manual | 83-86 | Expired auctions return negative time. | Clamp remaining seconds to zero. |
