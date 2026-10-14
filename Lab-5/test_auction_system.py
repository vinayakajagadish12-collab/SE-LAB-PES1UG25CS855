"""Regression tests for auction rules and HTML/XML safety."""

import json
import unittest
from unittest.mock import MagicMock, patch

from defusedxml.common import DefusedXmlException
import auction_system as app


class AuctionTests(unittest.TestCase):
    """Check behavior that static analysis alone cannot verify."""

    def setUp(self):
        app.auctions.clear()
        self.auction = app.create_auction(
            "A", "<script>alert(1)</script>", "seller", 500,
            "2026-12-01 18:00"
        )

    def test_increments(self):
        self.assertTrue(app.bid("A", "alice", 300, "2026-12-01 10:00"))
        self.assertFalse(app.bid("A", "bob", 300, "2026-12-01 10:01"))
        self.assertFalse(app.bid("A", "bob", 350, "2026-12-01 10:01"))
        self.assertTrue(app.bid("A", "bob", 400, "2026-12-01 10:02"))

    def test_invalid_amounts_and_seller(self):
        for amount in (0, -10, float("nan"), float("inf"), True, "500"):
            with self.subTest(amount=amount):
                self.assertFalse(app.bid("A", "alice", amount,
                                         "2026-12-01 10:00"))
        self.assertFalse(app.bid("A", "seller", 500, "2026-12-01 10:00"))

    def test_dates(self):
        self.assertTrue(app.bid("A", "alice", 500, "2026-12-01 9:30"))
        self.assertFalse(app.bid("A", "bob", 600, "2026-12-01 18:00"))
        self.assertFalse(app.bid("A", "bob", 600, "2026-12-02 09:00"))
        self.assertFalse(app.bid("A", "bob", 600, "bad date"))
        self.assertFalse(app.bid("missing", "bob", 600,
                                 "2026-12-01 10:00"))

    def test_reserve_and_price(self):
        self.assertIsNone(self.auction.winner())
        self.assertEqual(self.auction.final_price(), 0)
        app.bid("A", "alice", 400, "2026-12-01 10:00")
        self.assertIsNone(self.auction.winner())
        self.assertEqual(self.auction.final_price(), 0)
        app.bid("A", "bob", 500, "2026-12-01 10:01")
        self.assertEqual(self.auction.winner(), "bob")
        self.assertEqual(self.auction.final_price(), 525)

    def test_html(self):
        self.assertNotIn("<script>", app.render_listing("A"))
        badge = str(app.bidder_badge("<img src=x onerror=alert(1)>"))
        self.assertNotIn("<img", badge)
        self.assertIn("&lt;img", badge)

    def test_exports_and_ranking(self):
        app.bid("A", "alice", 300, "2026-12-01 10:00")
        app.bid("A", "bob", 400, "2026-12-01 10:01")
        app.bid("A", "alice", 500, "2026-12-01 10:02")
        self.assertEqual(app.top_bidders("A"), ["alice", "bob"])
        self.assertEqual(app.top_bidders("A", 0), [])
        self.assertEqual(len(json.loads(app.export_bids("A"))), 3)

    def test_expired_time(self):
        app.create_auction("old", "Old", "seller", 1, "2000-01-01 00:00")
        self.assertEqual(app.seconds_left("old"), 0)

    def test_payment_guards_and_mocked_success(self):
        # Use real datetimes for deterministic boundaries.
        from datetime import datetime
        with patch.object(app, "datetime") as clock:
            clock.now.return_value = datetime(2026, 12, 1, 10)
            with self.assertRaises(ValueError):
                app.charge_winner("A")
            clock.now.return_value = datetime(2026, 12, 2, 10)
            with self.assertRaises(ValueError):
                app.charge_winner("A")
            clock.strptime.side_effect = datetime.strptime
            app.bid("A", "alice", 500, "2026-12-01 10:00")
            gateway = MagicMock()
            gateway.__enter__.return_value = gateway
            gateway.charge.return_value = "paid"
            with patch.object(app.xmlrpc.client, "ServerProxy",
                              return_value=gateway):
                self.assertEqual(app.charge_winner("A"), "paid")
                gateway.charge.assert_called_once_with("alice", 525)

    def test_xml_entities_rejected(self):
        payload = (
            '<?xml version="1.0"?>'
            '<!DOCTYPE methodResponse [<!ENTITY x "injected">]>'
            '<methodResponse><params><param><value><string>&x;</string>'
            '</value></param></params></methodResponse>'
        )
        with self.assertRaises(DefusedXmlException):
            app.xmlrpc.client.loads(payload)


if __name__ == "__main__":
    unittest.main()
