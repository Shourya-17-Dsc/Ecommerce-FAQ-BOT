import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

"""
agent.py — Production module for the ShopEasy E-Commerce FAQ Bot.

1. Defines 12 knowledge-base documents (e-commerce domain, 100-500 words each).
2. Builds ChromaDB in-memory collection + SentenceTransformer embedder.
3. Imports compiled LangGraph app from ecommerce_bot.graph.
4. Exports public ask(question, thread_id) helper.
"""

import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb

load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE BASE — 12 documents, one specific topic each
# ═══════════════════════════════════════════════════════════════════════════════

KNOWLEDGE_BASE = [
    {
        "id": "doc_001",
        "topic": "Return Policy",
        "text": (
            "ShopEasy Return Policy\n\n"
            "ShopEasy offers a hassle-free 7-day return policy on most products from the date "
            "of delivery. Customers can initiate a return if the product is unused, in its "
            "original packaging, with all tags intact.\n\n"
            "Categories eligible for return:\n"
            "  • Electronics and appliances (within 7 days)\n"
            "  • Clothing and footwear (within 7 days, unwashed and unworn)\n"
            "  • Home and kitchen (within 7 days)\n"
            "  • Beauty and personal care (within 7 days, unopened)\n\n"
            "Categories NOT eligible for return:\n"
            "  • Perishable goods (food, flowers)\n"
            "  • Downloadable software and digital products\n"
            "  • Innerwear, socks, and swimwear (hygiene reasons)\n"
            "  • Customised or personalised products\n\n"
            "How to initiate a return:\n"
            "  1. Log in to your ShopEasy account.\n"
            "  2. Go to 'My Orders' and select the order.\n"
            "  3. Click 'Return / Exchange' and select the reason.\n"
            "  4. Choose your preferred refund method.\n"
            "  5. Schedule a pickup — our logistics partner will collect the item within "
            "     2 business days.\n\n"
            "Refund is processed within 5–7 business days after the item is received and "
            "quality-checked at our warehouse."
        ),
    },
    {
        "id": "doc_002",
        "topic": "Refund Process",
        "text": (
            "ShopEasy Refund Policy and Timeline\n\n"
            "Refunds at ShopEasy are processed based on the original payment method:\n\n"
            "  • UPI / Net Banking / Debit Card  : 3–5 business days\n"
            "  • Credit Card                     : 5–7 business days (depends on bank)\n"
            "  • ShopEasy Wallet                 : Instant (within 24 hours)\n"
            "  • Cash on Delivery (COD)          : 5–7 business days via bank transfer "
            "(NEFT/IMPS — customer must provide bank details)\n\n"
            "Refund amount includes:\n"
            "  • Full product price paid\n"
            "  • Shipping charges paid (if the return is due to a defective or wrong product)\n\n"
            "Partial refunds may apply if:\n"
            "  • The product has minor damage not caused by ShopEasy.\n"
            "  • Accessories or original packaging is missing.\n\n"
            "Refund status can be tracked under 'My Orders > Refund Status'. "
            "For unresolved refunds after 10 business days, contact support at "
            "support@shopeasy.in or call 1800-123-4567."
        ),
    },
    {
        "id": "doc_003",
        "topic": "Shipping and Delivery",
        "text": (
            "ShopEasy Shipping Policy\n\n"
            "Delivery options and estimated timelines:\n\n"
            "  • Standard Delivery   : 4–7 business days — FREE on orders above Rs.499\n"
            "  • Express Delivery    : 1–2 business days — Rs.99 flat fee\n"
            "  • Same-Day Delivery   : Available in select cities (Delhi, Mumbai, Bengaluru, "
            "    Hyderabad, Chennai, Pune) for orders placed before 12:00 PM — Rs.149 fee\n"
            "  • Scheduled Delivery  : Choose a preferred delivery date/slot — Rs.49 fee\n\n"
            "Shipping coverage:\n"
            "  ShopEasy delivers to 27,000+ pin codes across India. Enter your pin code on "
            "  the product page to check delivery availability and estimated date.\n\n"
            "Order dispatch:\n"
            "  Most orders are dispatched within 24–48 hours of placement. "
            "  Seller-shipped items may take up to 3 business days for dispatch.\n\n"
            "Tracking:\n"
            "  Once dispatched, a tracking link is sent via SMS and email. "
            "  Track live at shopeasy.in/track or in the 'My Orders' section.\n\n"
            "Delivery attempt policy:\n"
            "  3 delivery attempts are made. If all fail, the package is returned to the "
            "  seller and a refund is issued automatically."
        ),
    },
    {
        "id": "doc_004",
        "topic": "Payment Methods",
        "text": (
            "ShopEasy Accepted Payment Methods\n\n"
            "ShopEasy accepts a wide range of payment options for a seamless checkout:\n\n"
            "Online payment methods:\n"
            "  • UPI (Google Pay, PhonePe, Paytm, BHIM, any UPI app)\n"
            "  • Debit cards (Visa, Mastercard, RuPay — all Indian banks)\n"
            "  • Credit cards (Visa, Mastercard, American Express, Diners Club)\n"
            "  • Net banking (50+ banks supported)\n"
            "  • ShopEasy Wallet (pre-loaded for instant payment)\n"
            "  • EMI — No-cost EMI available on orders above Rs.3,000 on select cards\n"
            "  • Buy Now Pay Later (BNPL) via ZestMoney, Simpl, LazyPay\n\n"
            "Offline payment:\n"
            "  • Cash on Delivery (COD) — available on orders up to Rs.50,000. "
            "    COD fee of Rs.30 applies on orders below Rs.499.\n\n"
            "Payment security:\n"
            "  All transactions are secured by 256-bit SSL encryption. ShopEasy is PCI-DSS "
            "  compliant and does not store card details on its servers.\n\n"
            "Failed payments:\n"
            "  If a payment fails but the amount is debited, it is automatically refunded "
            "  within 5–7 business days. Contact support if refund is not received."
        ),
    },
    {
        "id": "doc_005",
        "topic": "Coupons and Discount Codes",
        "text": (
            "ShopEasy Coupons, Promo Codes, and Discounts\n\n"
            "How to apply a coupon code:\n"
            "  1. Add items to your cart.\n"
            "  2. Proceed to checkout.\n"
            "  3. Enter the coupon code in the 'Apply Coupon' box and click 'Apply'.\n"
            "  4. The discount is reflected in your order total before payment.\n\n"
            "Types of discounts:\n"
            "  • Percentage off  : e.g., SAVE20 gives 20% off on orders above Rs.999\n"
            "  • Flat amount off : e.g., FLAT100 gives Rs.100 off on orders above Rs.599\n"
            "  • Bank offers     : Extra 10% off with HDFC/ICICI credit cards on weekends\n"
            "  • First-order     : WELCOME100 — Rs.100 off on your first ShopEasy order\n"
            "  • Category coupons: FASHION15 — 15% off on clothing and footwear\n\n"
            "Coupon rules:\n"
            "  • One coupon per order (coupons cannot be combined).\n"
            "  • Coupons are non-transferable and have an expiry date.\n"
            "  • Coupons cannot be applied on already-discounted items unless stated otherwise.\n"
            "  • Bank offer discounts apply over and above other coupons in some cases.\n\n"
            "Where to find coupons:\n"
            "  Check the 'Offers' page, your registered email, the ShopEasy app, "
            "  or partner bank websites."
        ),
    },
    {
        "id": "doc_006",
        "topic": "Exchange Policy",
        "text": (
            "ShopEasy Exchange Policy\n\n"
            "ShopEasy allows product exchanges within 7 days of delivery for size, colour, "
            "or variant issues.\n\n"
            "How to request an exchange:\n"
            "  1. Go to 'My Orders', select the order, and click 'Return / Exchange'.\n"
            "  2. Choose 'Exchange' and select the reason (wrong size, colour, etc.).\n"
            "  3. Select the desired replacement variant.\n"
            "  4. Pickup of the original item is scheduled within 2 business days.\n"
            "  5. The replacement is dispatched once the original item is quality-checked.\n\n"
            "Exchange rules:\n"
            "  • The item must be unused, unwashed, and in original packaging with all tags.\n"
            "  • Only one exchange per order item is permitted.\n"
            "  • If the replacement variant is unavailable, a full refund is issued.\n"
            "  • Exchange is not available on Final Sale items (marked 'Non-Returnable').\n"
            "  • Electronics are not eligible for exchange due to size/colour variants — "
            "    use the return process instead.\n\n"
            "Exchange shipping:\n"
            "  Exchange pickups and re-deliveries are free of charge."
        ),
    },
    {
        "id": "doc_007",
        "topic": "Product Warranty",
        "text": (
            "ShopEasy — Product Warranty Information\n\n"
            "Warranty coverage on ShopEasy products varies by category and brand:\n\n"
            "Electronics and appliances:\n"
            "  • Mobile phones and laptops   : 1-year manufacturer warranty\n"
            "  • Televisions                 : 1-year manufacturer warranty (panel: 1 year)\n"
            "  • Large appliances (AC, Fridge, Washing Machine): 1-year comprehensive + "
            "    additional years on compressor/motor (as per brand policy)\n"
            "  • Small appliances            : 1-year manufacturer warranty\n"
            "  • Accessories (cables, cases) : 6-month manufacturer warranty\n\n"
            "How to claim warranty:\n"
            "  1. Contact the brand's authorised service centre directly.\n"
            "  2. Provide your purchase invoice (downloadable from ShopEasy 'My Orders').\n"
            "  3. For brands that offer doorstep warranty service, raise a request on their "
            "     brand website or app.\n\n"
            "ShopEasy does not handle warranty claims directly — warranty is between the "
            "customer and the product manufacturer. ShopEasy's return/replacement policy "
            "covers defective products within 7 days of delivery (before warranty contact)."
        ),
    },
    {
        "id": "doc_008",
        "topic": "Loyalty Points and Rewards",
        "text": (
            "ShopEasy Loyalty Programme — SuperCoins\n\n"
            "ShopEasy rewards customers with SuperCoins on every purchase.\n\n"
            "Earning SuperCoins:\n"
            "  • 1 SuperCoin earned for every Rs.100 spent on ShopEasy.\n"
            "  • Bonus 5x SuperCoins on products marked 'SuperCoin eligible'.\n"
            "  • Extra SuperCoins for writing verified reviews, completing profile, "
            "    and referring friends (50 SuperCoins per successful referral).\n\n"
            "Redeeming SuperCoins:\n"
            "  • 1 SuperCoin = Rs.0.25 discount at checkout.\n"
            "  • Up to 50% of the order value can be paid using SuperCoins.\n"
            "  • Minimum redemption: 100 SuperCoins.\n"
            "  • SuperCoins can also be used to purchase digital vouchers, "
            "    game credits, and OTT subscriptions in the 'SuperCoin Store'.\n\n"
            "Expiry:\n"
            "  SuperCoins expire 1 year from the date of earning if not redeemed.\n\n"
            "Checking balance:\n"
            "  View your SuperCoin balance in 'My Account > SuperCoins'."
        ),
    },
    {
        "id": "doc_009",
        "topic": "Account Management",
        "text": (
            "ShopEasy Account Management Guide\n\n"
            "Creating an account:\n"
            "  Visit shopeasy.in or the ShopEasy app. Click 'Sign Up'. Enter your mobile "
            "  number or email, verify with OTP, and set a password.\n\n"
            "Managing your profile:\n"
            "  • Update name, email, phone, and date of birth under 'My Account > Profile'.\n"
            "  • Add/remove delivery addresses under 'My Addresses'.\n"
            "  • Manage saved payment methods under 'Saved Cards & UPI'.\n\n"
            "Password reset:\n"
            "  Click 'Forgot Password' on the login page. Enter your registered email/phone "
            "  and receive an OTP or reset link.\n\n"
            "Account deactivation:\n"
            "  To permanently delete your account, email support@shopeasy.in with subject "
            "  'Account Deletion Request'. Note: active orders must be completed before deletion.\n\n"
            "ShopEasy Plus (Premium membership):\n"
            "  • Rs.499/year or Rs.999 for 2 years.\n"
            "  • Benefits: free express delivery, early sale access, 2x SuperCoins, "
            "    exclusive member-only coupons, and priority customer support.\n\n"
            "Privacy: ShopEasy does not share your personal data with third parties "
            "without consent. See the Privacy Policy at shopeasy.in/privacy."
        ),
    },
    {
        "id": "doc_010",
        "topic": "Damaged or Wrong Product",
        "text": (
            "Received a Damaged, Defective, or Wrong Product?\n\n"
            "If you receive a damaged, defective, or incorrect product, ShopEasy offers "
            "a full replacement or refund.\n\n"
            "Steps to report:\n"
            "  1. Go to 'My Orders' within 48 hours of delivery.\n"
            "  2. Select the order and click 'Report a Problem'.\n"
            "  3. Choose the issue: Damaged / Defective / Wrong Item.\n"
            "  4. Upload photos of the product (required for processing).\n"
            "  5. Choose resolution: Replacement or Refund.\n\n"
            "Resolution timelines:\n"
            "  • Replacement dispatched within 2–3 business days after pickup.\n"
            "  • Refund processed within 5–7 business days.\n\n"
            "Important notes:\n"
            "  • Report issues within 48 hours of delivery for fastest resolution.\n"
            "  • Keep the original packaging — the logistics partner may need to inspect it.\n"
            "  • For high-value electronics, a technician visit may be required before "
            "    replacement is approved.\n\n"
            "If the issue is not resolved within 7 business days, escalate by contacting "
            "support at 1800-123-4567."
        ),
    },
    {
        "id": "doc_011",
        "topic": "Seller and Brand Policies",
        "text": (
            "ShopEasy Seller and Brand Policies\n\n"
            "ShopEasy is a marketplace with two types of products:\n\n"
            "1. ShopEasy Fulfilled (SE Fulfilled):\n"
            "   Products stored in ShopEasy warehouses. Returns, delivery, and quality "
            "   are managed directly by ShopEasy. Faster delivery and easier returns.\n\n"
            "2. Seller Fulfilled:\n"
            "   Products shipped directly by the third-party seller. Return policy may "
            "   vary slightly (5–7 days, depending on seller). Check the product page for "
            "   seller-specific return terms.\n\n"
            "Verified sellers:\n"
            "  All sellers on ShopEasy are KYC-verified and rated. You can view the seller "
            "  rating, number of sales, and customer reviews on any product page.\n\n"
            "Brand authenticity:\n"
            "  ShopEasy guarantees product authenticity for all 'ShopEasy Fulfilled' products. "
            "  For seller-fulfilled products, ShopEasy's anti-counterfeit policy applies — "
            "  report suspected fake products at trust@shopeasy.in.\n\n"
            "Becoming a seller:\n"
            "  Register at shopeasy.in/sell. Requirements: GST certificate, bank account, "
            "  and a valid address proof. No registration fee."
        ),
    },
    {
        "id": "doc_012",
        "topic": "Customer Support and Contact",
        "text": (
            "ShopEasy Customer Support — Contact Directory\n\n"
            "Phone (Toll-free)  : 1800-123-4567  (Mon–Sat, 9 AM–9 PM)\n"
            "Email              : support@shopeasy.in  (response within 24 hours)\n"
            "Live Chat          : shopeasy.in/chat  (Mon–Sat, 9 AM–9 PM)\n"
            "WhatsApp           : +91-98765-43210  (Mon–Sat, 10 AM–7 PM)\n\n"
            "Self-service options (available 24/7):\n"
            "  • Track order   : shopeasy.in/track  or  'My Orders' in app\n"
            "  • Raise return  : 'My Orders > Return / Exchange'\n"
            "  • Raise refund  : 'My Orders > Refund Status'\n"
            "  • Report issue  : 'My Orders > Report a Problem'\n"
            "  • FAQs          : shopeasy.in/help\n\n"
            "Escalation:\n"
            "  If your issue is not resolved within 3 business days, email "
            "  escalations@shopeasy.in with your order ID and a summary of the issue.\n\n"
            "Registered office:\n"
            "  ShopEasy Technologies Pvt. Ltd.\n"
            "  14th Floor, Cyber Towers, Hitech City, Hyderabad — 500081, Telangana.\n\n"
            "Social media: @ShopEasyIndia on Twitter, Instagram, and Facebook."
        ),
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# Embedder + ChromaDB
# ═══════════════════════════════════════════════════════════════════════════════

print("[agent] Loading SentenceTransformer...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

print("[agent] Building ChromaDB in-memory collection...")
_chroma_client = chromadb.Client()
collection = _chroma_client.get_or_create_collection(
    name="shopeasy_kb",
    metadata={"hnsw:space": "cosine"},
)

if collection.count() == 0:
    for doc in KNOWLEDGE_BASE:
        embedding = embedder.encode(doc["text"]).tolist()
        collection.add(
            documents=[doc["text"]],
            embeddings=[embedding],
            ids=[doc["id"]],
            metadatas=[{"topic": doc["topic"]}],
        )
    print(f"[agent] Indexed {collection.count()} documents.")
else:
    print(f"[agent] ChromaDB already populated ({collection.count()} docs).")


def _verify_retrieval():
    checks = [
        ("return policy clothing",       "Return Policy"),
        ("how to apply coupon code",      "Coupons and Discount Codes"),
        ("cash on delivery payment",      "Payment Methods"),
        ("exchange size wrong product",   "Exchange Policy"),
        ("customer support phone number", "Customer Support and Contact"),
    ]
    for query, expected in checks:
        vec = embedder.encode(query).tolist()
        res = collection.query(query_embeddings=[vec], n_results=1)
        got = res["metadatas"][0][0]["topic"] if res["metadatas"][0] else "NONE"
        ok  = expected.lower() in got.lower()
        print(f"[agent] Retrieval {'OK' if ok else 'MISS'}  '{query}' -> {got}")

_verify_retrieval()


# ═══════════════════════════════════════════════════════════════════════════════
# Compiled LangGraph app
# ═══════════════════════════════════════════════════════════════════════════════

from ecommerce_bot.graph import compiled_app  # noqa: E402


# ═══════════════════════════════════════════════════════════════════════════════
# Public ask() helper
# ═══════════════════════════════════════════════════════════════════════════════

def ask(question: str, thread_id: str = "default") -> dict:
    """
    Invoke the compiled agent.

    Returns:
        {"answer": str, "route": str, "faithfulness": float, "sources": list[str]}
    """
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {
        "question":    question,
        "messages":    [],
        "route":       "",
        "retrieved":   "",
        "sources":     [],
        "tool_result": "",
        "answer":      "",
        "faithfulness": 0.0,
        "eval_retries": 0,
        "user_name":   None,
        "order_id":    None,
    }
    result = compiled_app.invoke(initial_state, config=config)
    return {
        "answer":       result.get("answer", ""),
        "route":        result.get("route", ""),
        "faithfulness": result.get("faithfulness", 0.0),
        "sources":      result.get("sources", []),
    }


if __name__ == "__main__":
    samples = [
        ("What is ShopEasy's return policy?",           "q1"),
        ("Does ShopEasy accept Cash on Delivery?",       "q2"),
        ("How do I apply a coupon code?",                "q3"),
        ("Track my order SE-456789",                     "q4"),
        ("What payment methods are available?",          "q5"),
        ("What is 2000 minus 20 percent?",               "q6"),
        ("What is today's date?",                        "q7"),
    ]
    print("\n== Quick Agent Test ==============================================")
    for q, tid in samples:
        print(f"\nQ: {q}")
        out = ask(q, thread_id=tid)
        print(f"Route={out['route']}  Faith={out['faithfulness']:.2f}  Sources={out['sources']}")
        print(f"A: {out['answer'][:200]}")
