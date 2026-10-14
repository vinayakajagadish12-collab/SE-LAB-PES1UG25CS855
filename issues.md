# Issues and fixes

Line numbers refer to the original program retained in the baseline commit.
Tool findings come from reports/before; manual findings are labeled separately.

| Issue | Type | Original line(s) | Description | Fix approach |
|---|---|---|---|---|
| B411 | Bandit / High | 5, 73 | XML-RPC parses potentially hostile XML. | Enable defusedxml.xmlrpc.monkey_patch before parsing any response. Retain XML-RPC. One scoped nosec B411 annotation covers the import-only warning: Bandit cannot recognize the runtime mitigation. A regression test verifies XML entity rejection. |
| B701 | Bandit / High | 65 | Listing title is rendered with autoescape disabled. | Enable Jinja autoescape. |
| B704 | Bandit / Medium | 70 | Untrusted bidder name is marked as safe HTML. | Use a constant Markup template and its escaping format method. |
