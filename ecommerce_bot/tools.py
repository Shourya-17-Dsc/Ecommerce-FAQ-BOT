"""
Tool functions for the ShopEasy E-Commerce FAQ Bot.

Rules:
- Every function MUST return a string — never raise an exception.
- Tools handle what the KB cannot: live date/time, price arithmetic, order mock-lookup.
"""

from datetime import datetime, timedelta
import re
import random


# ── Tool 1: current date / time ──────────────────────────────────────────────

def get_current_datetime() -> str:
    now = datetime.now()
    return (
        f"Current date and time: {now.strftime('%A, %d %B %Y at %I:%M %p')}."
    )


# ── Tool 2: discount / price calculator ──────────────────────────────────────

def calculate_price(expression: str) -> str:
    """Safely evaluates arithmetic — handles price calculations and discount math."""
    try:
        safe = re.sub(r"[^0-9+\-*/.() %]", "", expression).strip()
        if not safe:
            return f"Could not parse a numeric expression from: '{expression}'"
        result = eval(safe, {"__builtins__": {}}, {})
        return f"Calculation result: {safe} = {result}"
    except ZeroDivisionError:
        return "Error: division by zero."
    except Exception as exc:
        return f"Could not evaluate '{expression}': {exc}"


def calculate_discount(original_price: float, discount_percent: float) -> str:
    """Returns the discounted price and savings amount."""
    try:
        discount_amt = round(original_price * discount_percent / 100, 2)
        final_price  = round(original_price - discount_amt, 2)
        return (
            f"Original price: Rs.{original_price:.2f} | "
            f"Discount ({discount_percent}%): Rs.{discount_amt:.2f} | "
            f"Final price: Rs.{final_price:.2f}"
        )
    except Exception as exc:
        return f"Could not calculate discount: {exc}"


# ── Tool 3: mock order tracker ────────────────────────────────────────────────

# Simulated order statuses for demo purposes
_ORDER_MOCK = {
    "SH": ["Shipped",    "Your order has been shipped via BlueDart. Expected delivery in 2–3 business days."],
    "DE": ["Delivered",  "Your order has been delivered. If you have any issues, raise a return request within 7 days."],
    "PR": ["Processing", "Your order is being processed and will be dispatched within 24 hours."],
    "CA": ["Cancelled",  "Your order has been cancelled. Refund will be processed in 5–7 business days."],
    "RE": ["Return Initiated", "Your return request has been accepted. Pickup scheduled in 2 business days."],
}

def track_order(order_id: str) -> str:
    """
    Mock order tracker. Real implementation would call the orders database.
    Returns a realistic status string based on the last 2 chars of the order ID.
    """
    if not order_id or len(order_id) < 4:
        return (
            "Please provide a valid order ID (e.g., SE-123456). "
            "You can find your order ID in your confirmation email or under 'My Orders' on the website."
        )
    # Use last 2 uppercase chars as a deterministic mock key
    key = order_id.upper()[-2:]
    match = _ORDER_MOCK.get(key)
    if match:
        status, detail = match
        eta = (datetime.now() + timedelta(days=random.randint(1, 4))).strftime("%d %B %Y")
        return f"Order {order_id.upper()} — Status: {status}. {detail} (Estimated: {eta})"
    else:
        # Default: in transit
        eta = (datetime.now() + timedelta(days=2)).strftime("%d %B %Y")
        return (
            f"Order {order_id.upper()} — Status: In Transit. "
            f"Expected delivery by {eta}. Track live at shopeasy.in/track"
        )


# ── Tool 4: customer support contact ─────────────────────────────────────────

def get_support_contact() -> str:
    return (
        "ShopEasy Customer Support:\n"
        "  Phone    : 1800-123-4567  (Toll-free, Mon–Sat 9 AM–9 PM)\n"
        "  Email    : support@shopeasy.in  (response within 24 hours)\n"
        "  Live Chat: shopeasy.in/chat  (Mon–Sat 9 AM–9 PM)\n"
        "  WhatsApp : +91-98765-43210  (Mon–Sat 10 AM–7 PM)"
    )


# ── Dispatcher ────────────────────────────────────────────────────────────────

def dispatch_tool(question: str) -> str:
    """
    Inspect the question and call the most appropriate tool.
    Returns a string result — never raises.
    """
    q = question.lower()

    # Order tracking
    order_match = re.search(r"\b(se[-\s]?\d{4,8}|order\s*[#:]?\s*\d{4,8})\b", question, re.IGNORECASE)
    if order_match or any(w in q for w in ["track", "order status", "where is my order", "my order"]):
        oid = order_match.group() if order_match else "SE-DEMO"
        return track_order(oid.strip())

    # Support contact
    if any(w in q for w in ["contact", "support", "helpline", "phone", "email", "chat", "whatsapp", "call"]):
        return get_support_contact()

    # Discount / price calculation
    if any(w in q for w in ["discount", "calculate", "price", "how much", "cost", "off", "save", "deal"]):
        numbers = re.findall(r"\d+\.?\d*", question)
        if len(numbers) >= 2:
            return calculate_discount(float(numbers[0]), float(numbers[1]))
        elif len(numbers) == 1:
            return calculate_price(numbers[0])
        return "Please provide a price and discount percentage to calculate. E.g., 'Rs.2000 at 20% off'"

    # Arithmetic
    if any(w in q for w in ["plus", "minus", "times", "divided", "multiply", "add", "subtract", "+", "-", "*", "/"]):
        expr_match = re.search(r"[\d\s+\-*/.()%]+", q)
        if expr_match:
            return calculate_price(expr_match.group())

    # Date / time
    if any(w in q for w in ["date", "time", "today", "now", "day", "when", "current"]):
        return get_current_datetime()

    # Default
    return get_current_datetime()
