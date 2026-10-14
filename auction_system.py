"""Online auction demo with validated bids and escaped HTML output."""

import json
import math
# XML-RPC is hardened by monkey_patch before any network response.
import xmlrpc.client  # nosec B411
from datetime import datetime

from defusedxml.xmlrpc import monkey_patch
from jinja2 import Environment
from markupsafe import Markup

# Protect the existing XML-RPC protocol from hostile XML and oversized replies.
monkey_patch()

PAYMENT_GATEWAY = "https://pay.auction.example/RPC2"
MIN_INCREMENT = 100
TIME_FORMAT = "%Y-%m-%d %H:%M"


class Auction:
    """Track an item's accepted bids, reserve and closing time."""

    def __init__(self, item_id, title, seller, reserve_price, ends_at):
        self.item_id = item_id
        self.title = title
        self.seller = seller
        self.reserve_price = reserve_price
        self.ends_at = datetime.strptime(ends_at, TIME_FORMAT)
        self.bids = []

    @property
    def highest(self):
        """Return the highest accepted bid, or zero before bidding."""
        return self.bids[-1][1] if self.bids else 0

    @property
    def leader(self):
        """Return the leading bidder, or None before bidding."""
        return self.bids[-1][0] if self.bids else None

    def place_bid(self, bidder, amount, at):
        """Accept valid bids before closing; reject invalid amounts or bidders."""
        bid_time = datetime.strptime(at, TIME_FORMAT)
        if bid_time >= self.ends_at:
            raise ValueError("Auction closed")
        if bidder == self.seller or not bidder:
            return False
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            return False
        if not math.isfinite(amount) or amount <= 0:
            return False
        if self.bids and amount < self.highest + MIN_INCREMENT:
            return False
        self.bids.append((bidder, amount, at))
        return True

    def winner(self):
        """Return the qualifying leader only when the reserve is met."""
        if not self.bids or self.highest < self.reserve_price:
            return None
        return self.leader

    def final_price(self):
        """Return the qualifying price plus 5% premium, or zero if unsold."""
        if self.winner() is None:
            return 0
        return round(self.highest * 1.05, 2)


auctions = {}


def create_auction(item_id, title, seller, reserve_price, ends_at):
    """Create and register an auction."""
    auctions[item_id] = Auction(item_id, title, seller, reserve_price, ends_at)
    return auctions[item_id]


def bid(item_id, bidder, amount, at):
    """Place a bid, returning False for unknown items or invalid timestamps."""
    try:
        return auctions[item_id].place_bid(bidder, amount, at)
    except (KeyError, ValueError, TypeError):
        return False


def top_bidders(item_id, n=3):
    """Return up to n distinct bidders ranked by their highest bids."""
    ordered = sorted(auctions[item_id].bids, key=lambda row: row[1], reverse=True)
    names = []
    for bidder, _, _ in ordered:
        if bidder not in names:
            names.append(bidder)
    return names[:max(0, n)]


def render_listing(item_id):
    """Render a listing with untrusted titles escaped."""
    env = Environment(autoescape=True)
    template = env.from_string(
        "<h2>{{ a.title }}</h2><p>Current bid: Rs.{{ a.highest }}</p>"
    )
    return template.render(a=auctions[item_id])


def bidder_badge(name):
    """Render a badge, escaping the bidder's name."""
    return Markup("<span class='bidder'>{}</span>").format(name)


def charge_winner(item_id):
    """Charge a qualifying winner after closing using hardened XML-RPC."""
    auction = auctions[item_id]
    if datetime.now() < auction.ends_at:
        raise ValueError("Auction is still open")
    winner = auction.winner()
    if winner is None:
        raise ValueError("No qualifying winner")
    with xmlrpc.client.ServerProxy(PAYMENT_GATEWAY) as gateway:
        return gateway.charge(winner, auction.final_price())


def export_bids(item_id):
    """Export accepted bids as JSON."""
    rows = [
        {"bidder": bidder, "amount": amount, "at": at}
        for bidder, amount, at in auctions[item_id].bids
    ]
    return json.dumps(rows)


def seconds_left(item_id):
    """Return remaining whole seconds, clamped to zero after closing."""
    remaining = (auctions[item_id].ends_at - datetime.now()).total_seconds()
    return max(0, int(remaining))


def main():
    """Run the original demonstration without contacting a payment service."""
    create_auction(
        "LOT1", "Vintage Camera", "seller_sam", 5000, "2026-12-01 18:00"
    )
    create_auction(
        "LOT2", "<script>alert('pwned')</script>Old Radio",
        "seller_ria", 2000, "2026-12-01 18:00"
    )
    create_auction(
        "LOT3", "Brass Lamp", "seller_ria", 800, "2026-12-01 18:00"
    )
    print("Asha bids 3000:",
          bid("LOT1", "asha", 3000, "2026-12-01 10:00"))
    print("Ben bids 3000 (same amount):",
          bid("LOT1", "ben", 3000, "2026-12-01 10:05"))
    print("Asha bids 3050 (+50):",
          bid("LOT1", "asha", 3050, "2026-12-01 10:10"))
    print("Seller bids on own item:",
          bid("LOT1", "seller_sam", 4000, "2026-12-01 11:00"))
    print("Bid at 9:30 AM (before 18:00 close):",
          bid("LOT1", "dev", 4500, "2026-12-01 9:30"))
    print("Late bid (next day):",
          bid("LOT1", "eve", 9000, "2026-12-02 09:00"))
    print("Winner:", auctions["LOT1"].winner())
    print("Final price (reserve 5000):", auctions["LOT1"].final_price())
    print("Top bidders:", top_bidders("LOT1"))
    print("Rs.0 bid on LOT3 (reserve 800):",
          bid("LOT3", "carl", 0, "2026-12-01 11:30"))
    print("LOT3 winner:", auctions["LOT3"].winner())
    print("No-bid winner:", auctions["LOT2"].winner())
    print("Listing HTML:", render_listing("LOT2"))
    print("Badge:", bidder_badge("<img src=x onerror=alert(1)>"))


if __name__ == "__main__":
    main()
