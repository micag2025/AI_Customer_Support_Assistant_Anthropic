"""Backend for the Acme Co customer-support chatbot demo.

All customer, order, shipment, and refund data are fictional and stored in memory.
No real carrier or payment provider is contacted.
"""

import os
from anthropic import Anthropic
from helper import get_anthropic_api_key

MODEL_NAME = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")

_api_key = get_anthropic_api_key()
if not _api_key:
    raise RuntimeError(
        "ANTHROPIC_API_KEY was not found. Add it to a .env file in the project "
        "folder, or set it as an environment variable."
    )

client = Anthropic(api_key=_api_key)


class FakeDatabase:
    """A small in-memory customer-support database for learning tool use."""

    def __init__(self, customers=None, orders=None):
        self.customers = [
            {"id": "1213210", "name": "John Doe", "email": "john@gmail.com", "phone": "123-456-7890", "username": "johndoe"},
            {"id": "2837622", "name": "Priya Patel", "email": "priya@candy.com", "phone": "987-654-3210", "username": "priya123"},
            {"id": "3924156", "name": "Liam Nguyen", "email": "lnguyen@yahoo.com", "phone": "555-123-4567", "username": "liamn"},
            {"id": "4782901", "name": "Aaliyah Davis", "email": "aaliyahd@hotmail.com", "phone": "111-222-3333", "username": "adavis"},
            {"id": "5190753", "name": "Hiroshi Nakamura", "email": "hiroshi@gmail.com", "phone": "444-555-6666", "username": "hiroshin"},
            {"id": "6824095", "name": "Fatima Ahmed", "email": "fatimaa@outlook.com", "phone": "777-888-9999", "username": "fatimaahmed"},
            {"id": "7135680", "name": "Alejandro Rodriguez", "email": "arodriguez@protonmail.com", "phone": "222-333-4444", "username": "alexr"},
            {"id": "8259147", "name": "Megan Anderson", "email": "megana@gmail.com", "phone": "666-777-8888", "username": "manderson"},
            {"id": "9603481", "name": "Kwame Osei", "email": "kwameo@yahoo.com", "phone": "999-000-1111", "username": "kwameo"},
            {"id": "1057426", "name": "Mei Lin", "email": "meilin@gmail.com", "phone": "333-444-5555", "username": "mlin"},
        ]

        # price is the unit price; order total = quantity * price.
        # Dates, tracking numbers, and events are fictional demonstration data.
        self.orders = [
            {
                "id": "24601", "customer_id": "1213210", "product": "Wireless Headphones",
                "quantity": 1, "price": 79.99, "status": "Shipped",
                "shipping_status": "In transit", "carrier": "UPS",
                "tracking_number": "1Z999AA10123456784", "estimated_delivery": "2026-10-16",
                "shipped_at": "2026-10-12", "delivered_at": None,
                "tracking_events": [
                    {"timestamp": "2026-10-12 09:15", "location": "Newark, NJ", "status": "Label created", "description": "Shipping label created."},
                    {"timestamp": "2026-10-13 14:30", "location": "Columbus, OH", "status": "In transit", "description": "Package departed the regional sorting facility."},
                    {"timestamp": "2026-10-14 06:45", "location": "Chicago, IL", "status": "In transit", "description": "Package arrived at the local distribution hub."},
                ],
                "refund_status": "Not requested", "refund_eligible": True,
            },
            {
                "id": "13579", "customer_id": "1213210", "product": "Smartphone Case",
                "quantity": 2, "price": 19.99, "status": "Processing",
                "shipping_status": "Not shipped", "carrier": None,
                "tracking_number": None, "estimated_delivery": None,
                "shipped_at": None, "delivered_at": None, "tracking_events": [],
                "refund_status": "Not requested", "refund_eligible": True,
            },
            {
                "id": "97531", "customer_id": "2837622", "product": "Bluetooth Speaker",
                "quantity": 1, "price": 49.99, "status": "Shipped",
                "shipping_status": "Out for delivery", "carrier": "UPS",
                "tracking_number": "JD014600006281000123", "estimated_delivery": "2026-10-14",
                "shipped_at": "2026-10-10", "delivered_at": None,
                "tracking_events": [
                    {"timestamp": "2026-10-10 11:20", "location": "Memphis, TN", "status": "Picked up", "description": "Carrier collected the parcel."},
                    {"timestamp": "2026-10-13 22:10", "location": "Dallas, TX", "status": "At delivery depot", "description": "Parcel arrived at the local delivery depot."},
                    {"timestamp": "2026-10-14 07:05", "location": "Austin, TX", "status": "Out for delivery", "description": "Courier has the parcel for delivery today."},
                ],
                "refund_status": "Not requested", "refund_eligible": False,
            },
            {
                "id": "86420", "customer_id": "3924156", "product": "Fitness Tracker",
                "quantity": 1, "price": 129.99, "status": "Delivered",
                "shipping_status": "Delivered", "carrier": "USPS",
                "tracking_number": "USPS86420DEMO", "estimated_delivery": "2026-10-11",
                "shipped_at": "2026-10-08", "delivered_at": "2026-10-11 13:42",
                "tracking_events": [
                    {"timestamp": "2026-10-08 10:00", "location": "Atlanta, GA", "status": "Shipped", "description": "Parcel handed to carrier."},
                    {"timestamp": "2026-10-10 16:25", "location": "Nashville, TN", "status": "At delivery depot", "description": "Parcel arrived at the local depot."},
                    {"timestamp": "2026-10-11 13:42", "location": "Nashville, TN", "status": "Delivered", "description": "Parcel delivered."},
                ],
                "refund_status": "Not requested", "refund_eligible": True,
            },
            {
                "id": "54321", "customer_id": "4782901", "product": "Laptop Sleeve",
                "quantity": 3, "price": 24.99, "status": "Shipped",
                "shipping_status": "Delayed", "carrier": "FedEx",
                "tracking_number": "FX54321DEMO", "estimated_delivery": "2026-10-17",
                "shipped_at": "2026-10-09", "delivered_at": None,
                "tracking_events": [
                    {"timestamp": "2026-10-09 12:00", "location": "Denver, CO", "status": "Shipped", "description": "Parcel collected by carrier."},
                    {"timestamp": "2026-10-12 18:20", "location": "Kansas City, MO", "status": "Exception", "description": "Severe weather caused a transit delay."},
                    {"timestamp": "2026-10-14 05:50", "location": "Kansas City, MO", "status": "Delayed", "description": "Shipment is moving again; delivery estimate updated."},
                ],
                "refund_status": "Not requested", "refund_eligible": False,
            },
            {
                "id": "19283", "customer_id": "5190753", "product": "Wireless Mouse",
                "quantity": 1, "price": 34.99, "status": "Processing",
                "shipping_status": "Preparing order", "carrier": None,
                "tracking_number": None, "estimated_delivery": "2026-10-19",
                "shipped_at": None, "delivered_at": None, "tracking_events": [],
                "refund_status": "Not requested", "refund_eligible": True,
            },
            {
                "id": "74651", "customer_id": "6824095", "product": "Gaming Keyboard",
                "quantity": 1, "price": 89.99, "status": "Delivered",
                "shipping_status": "Delivered", "carrier": "UPS",
                "tracking_number": "1Z74651DEMO", "estimated_delivery": "2026-10-09",
                "shipped_at": "2026-10-06", "delivered_at": "2026-10-09 15:18",
                "tracking_events": [
                    {"timestamp": "2026-10-06 08:30", "location": "Louisville, KY", "status": "Shipped", "description": "Parcel handed to carrier."},
                    {"timestamp": "2026-10-08 19:15", "location": "Indianapolis, IN", "status": "At delivery depot", "description": "Parcel arrived at local depot."},
                    {"timestamp": "2026-10-09 15:18", "location": "Indianapolis, IN", "status": "Delivered", "description": "Parcel delivered."},
                ],
                "refund_status": "Not requested", "refund_eligible": True,
            },
            {
                "id": "30298", "customer_id": "7135680", "product": "Portable Charger",
                "quantity": 2, "price": 29.99, "status": "Shipped",
                "shipping_status": "In transit", "carrier": "USPS",
                "tracking_number": "USPS30298DEMO", "estimated_delivery": "2026-10-16",
                "shipped_at": "2026-10-12", "delivered_at": None,
                "tracking_events": [
                    {"timestamp": "2026-10-12 16:00", "location": "Phoenix, AZ", "status": "Picked up", "description": "Parcel collected by carrier."},
                    {"timestamp": "2026-10-14 02:30", "location": "Albuquerque, NM", "status": "In transit", "description": "Parcel moving through the regional network."},
                ],
                "refund_status": "Not requested", "refund_eligible": False,
            },
            {
                "id": "47652", "customer_id": "8259147", "product": "Smartwatch",
                "quantity": 1, "price": 199.99, "status": "Processing",
                "shipping_status": "Preparing order", "carrier": None,
                "tracking_number": None, "estimated_delivery": "2026-10-20",
                "shipped_at": None, "delivered_at": None, "tracking_events": [],
                "refund_status": "Not requested", "refund_eligible": True,
            },
            {
                "id": "61984", "customer_id": "9603481", "product": "Noise-Cancelling Headphones",
                "quantity": 1, "price": 149.99, "status": "Shipped",
                "shipping_status": "In transit", "carrier": "UPS",
                "tracking_number": "JD61984DEMO", "estimated_delivery": "2026-10-18",
                "shipped_at": "2026-10-13", "delivered_at": None,
                "tracking_events": [
                    {"timestamp": "2026-10-13 09:40", "location": "Seattle, WA", "status": "Shipped", "description": "Parcel handed to carrier."},
                    {"timestamp": "2026-10-14 04:15", "location": "Louisville, KY", "status": "In transit", "description": "Parcel departed the sorting center."},
                ],
                "refund_status": "Not requested", "refund_eligible": False,
            },
            {
                "id": "58243", "customer_id": "1057426", "product": "Wireless Earbuds",
                "quantity": 2, "price": 99.99, "status": "Delivered",
                "shipping_status": "Delivered", "carrier": "USPS",
                "tracking_number": "PI58243DEMO", "estimated_delivery": "2026-10-07",
                "shipped_at": "2026-10-04", "delivered_at": "2026-10-07 11:07",
                "tracking_events": [
                    {"timestamp": "2026-10-04 08:15", "location": "Atlanta, GA", "status": "Shipped", "description": "Parcel accepted by carrier."},
                    {"timestamp": "2026-10-06 17:20", "location": "Austin, TX", "status": "At delivery depot", "description": "Parcel arrived at the local depot."},
                    {"timestamp": "2026-10-07 11:07", "location": "Austin, TX", "status": "Delivered", "description": "Parcel delivered."},
                ],
                "refund_status": "Not requested", "refund_eligible": True,
            },
            {
                "id": "90357", "customer_id": "1213210", "product": "Smartphone Case",
                "quantity": 1, "price": 19.99, "status": "Shipped",
                "shipping_status": "In transit", "carrier": "USPS",
                "tracking_number": "USPS90357DEMO", "estimated_delivery": "2026-10-15",
                "shipped_at": "2026-10-13", "delivered_at": None,
                "tracking_events": [
                    {"timestamp": "2026-10-13 10:10", "location": "Dallas, TX", "status": "Shipped", "description": "Parcel collected by carrier."},
                    {"timestamp": "2026-10-14 03:35", "location": "Nashville, TN", "status": "In transit", "description": "Parcel reached the regional distribution center."},
                ],
                "refund_status": "Not requested", "refund_eligible": False,
            },
            {
                "id": "28164", "customer_id": "2837622", "product": "Wireless Headphones",
                "quantity": 2, "price": 79.99, "status": "Processing",
                "shipping_status": "Preparing order", "carrier": None,
                "tracking_number": None, "estimated_delivery": "2026-10-19",
                "shipped_at": None, "delivered_at": None, "tracking_events": [],
                "refund_status": "Not requested", "refund_eligible": False,
            },
        ]

        # Keep the original demo records as the default. If either custom
        # collection is supplied, require both so the database stays coherent.
        if customers is not None or orders is not None:
            if customers is None or orders is None:
                raise ValueError("Both customers and orders must be provided together.")
            self.customers = customers
            self.orders = orders

        self._validate_data()

    def _validate_data(self):
        """Validate the minimum structure expected by the seven support tools."""
        if not isinstance(self.customers, list) or not isinstance(self.orders, list):
            raise ValueError("The customers and orders datasets must both be JSON arrays.")

        customer_required = {"id", "name", "email", "phone", "username"}
        order_required = {
            "id", "customer_id", "product", "quantity", "price", "status",
            "shipping_status", "carrier", "tracking_number", "estimated_delivery",
            "shipped_at", "delivered_at", "tracking_events", "refund_status",
            "refund_eligible",
        }

        customer_ids = set()
        for index, customer in enumerate(self.customers):
            if not isinstance(customer, dict):
                raise ValueError(f"Customer at index {index} must be a JSON object.")
            missing = customer_required - customer.keys()
            if missing:
                raise ValueError(f"Customer at index {index} is missing: {', '.join(sorted(missing))}.")
            customer_id = str(customer["id"])
            if customer_id in customer_ids:
                raise ValueError(f"Duplicate customer ID: {customer_id}.")
            customer_ids.add(customer_id)
            for field in ("name", "email", "phone", "username"):
                if not isinstance(customer[field], str):
                    raise ValueError(f"Customer {customer_id}: '{field}' must be text.")

        order_ids = set()
        for index, order in enumerate(self.orders):
            if not isinstance(order, dict):
                raise ValueError(f"Order at index {index} must be a JSON object.")
            missing = order_required - order.keys()
            if missing:
                raise ValueError(f"Order at index {index} is missing: {', '.join(sorted(missing))}.")
            order_id = str(order["id"])
            if order_id in order_ids:
                raise ValueError(f"Duplicate order ID: {order_id}.")
            order_ids.add(order_id)
            if str(order["customer_id"]) not in customer_ids:
                raise ValueError(f"Order {order_id} references an unknown customer ID.")
            if not isinstance(order["quantity"], int) or order["quantity"] < 1:
                raise ValueError(f"Order {order_id}: quantity must be a positive integer.")
            if not isinstance(order["price"], (int, float)) or isinstance(order["price"], bool) or order["price"] < 0:
                raise ValueError(f"Order {order_id}: price must be a non-negative number.")
            if not isinstance(order["tracking_events"], list):
                raise ValueError(f"Order {order_id}: tracking_events must be a JSON array.")
            if not isinstance(order["refund_eligible"], bool):
                raise ValueError(f"Order {order_id}: refund_eligible must be true or false.")
            if any(not isinstance(event, dict) for event in order["tracking_events"]):
                raise ValueError(f"Order {order_id}: each tracking event must be a JSON object.")

    def get_user(self, key, value):
        if key not in {"email", "phone", "username"}:
            raise ValueError(f"Invalid customer lookup key: {key}")
        for customer in self.customers:
            if customer[key].casefold() == str(value).casefold():
                return customer
        return {"error": f"No customer found with {key} '{value}'."}

    def get_order_by_id(self, order_id):
        for order in self.orders:
            if order["id"] == str(order_id):
                return order
        return {"error": f"Order {order_id} was not found."}

    def get_customer_orders(self, customer_id):
        matches = [o for o in self.orders if o["customer_id"] == str(customer_id)]
        return matches if matches else {"message": f"No orders found for customer {customer_id}."}

    def cancel_order(self, order_id):
        order = self.get_order_by_id(order_id)
        if "error" in order:
            return order
        if order["status"] != "Processing":
            return {"success": False, "message": "Only orders still processing can be cancelled."}
        order["status"] = "Cancelled"
        order["shipping_status"] = "Not shipped"
        return {"success": True, "order_id": order["id"], "status": "Cancelled"}

    def get_shipping_status(self, order_id):
        order = self.get_order_by_id(order_id)
        if "error" in order:
            return order
        return {
            "order_id": order["id"],
            "product": order["product"],
            "order_status": order["status"],
            "shipping_status": order["shipping_status"],
            "carrier": order["carrier"],
            "tracking_number": order["tracking_number"],
            "shipped_at": order["shipped_at"],
            "estimated_delivery": order["estimated_delivery"],
            "delivered_at": order["delivered_at"],
            "latest_tracking_event": order["tracking_events"][-1] if order["tracking_events"] else None,
            "tracking_events": order["tracking_events"],
        }

    def check_refund_eligibility(self, order_id):
        order = self.get_order_by_id(order_id)
        if "error" in order:
            return order
        if order["refund_status"] == "Refunded":
            return {"order_id": order["id"], "eligible": False, "reason": "This order has already been refunded."}
        if not order["refund_eligible"]:
            reason = "This order is not currently eligible under the demo's refund rules."
            if order["shipping_status"] in {"In transit", "Out for delivery", "Delayed"}:
                reason = "The shipment is still in transit. The demo policy does not allow a refund at this stage."
            return {"order_id": order["id"], "eligible": False, "reason": reason}
        return {
            "order_id": order["id"],
            "eligible": True,
            "refund_amount": round(order["quantity"] * order["price"], 2),
            "currency": "USD",
            "reason": "The order meets the demo's refund rules.",
        }

    def issue_refund(self, order_id):
        """Record a simulated refund; this does not contact a payment provider."""
        eligibility = self.check_refund_eligibility(order_id)
        if not eligibility.get("eligible", False):
            return eligibility
        order = self.get_order_by_id(order_id)
        order["refund_status"] = "Refunded"
        order["status"] = "Refunded"
        return {
            "success": True,
            "order_id": order["id"],
            "refund_status": order["refund_status"],
            "refund_amount": eligibility["refund_amount"],
            "currency": eligibility["currency"],
            "message": "Refund recorded in the demo database; no payment was processed.",
        }


db = FakeDatabase()


def _tool(name, description, properties, required=None):
    return {
        "name": name,
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required or list(properties.keys()),
        },
    }


ORDER_ID = {"type": "string", "description": "The order ID."}

# Tool definitions describe actions to Claude. Python executes them below.
tools = [
    _tool("get_user", "Find a customer by email address, phone number, or username.", {
        "key": {"type": "string", "enum": ["email", "phone", "username"], "description": "Customer field to search."},
        "value": {"type": "string", "description": "Value to match."},
    }),
    _tool("get_order_by_id", "Retrieve the details and current status of one order.", {"order_id": ORDER_ID}),
    _tool("get_customer_orders", "List orders belonging to a customer. Use the customer ID returned by get_user.", {
        "customer_id": {"type": "string", "description": "Customer ID."},
    }),
    _tool("cancel_order", "Cancel an order only if its status is Processing. Ask the customer to explicitly confirm before using this action.", {"order_id": ORDER_ID}),
    _tool("get_shipping_status", "Retrieve the carrier, tracking number, estimated delivery, current shipping status, and tracking events for an order.", {"order_id": ORDER_ID}),
    _tool("check_refund_eligibility", "Check refund eligibility and the possible refund amount. This tool does not issue a refund.", {"order_id": ORDER_ID}),
    _tool("issue_refund", "Record a simulated refund only after the customer has explicitly confirmed they want the refund and eligibility has been checked. This mutates the demo database but does not process a real payment.", {"order_id": ORDER_ID}),
]


def process_tool_call(tool_name, tool_input, database=None):
    """Dispatch a Claude tool request to a selected database instance.

    The optional database argument lets each Streamlit session use its own
    dataset. Omitting it preserves the original module-level demo database.
    """
    active_db = database if database is not None else db
    dispatch = {
        "get_user": active_db.get_user,
        "get_order_by_id": active_db.get_order_by_id,
        "get_customer_orders": active_db.get_customer_orders,
        "cancel_order": active_db.cancel_order,
        "get_shipping_status": active_db.get_shipping_status,
        "check_refund_eligibility": active_db.check_refund_eligibility,
        "issue_refund": active_db.issue_refund,
    }
    if tool_name not in dispatch:
        raise ValueError(f"Unknown tool: {tool_name}")
    return dispatch[tool_name](**tool_input)

def create_database(customers=None, orders=None):
    """Create a validated database, using demo records when no data is passed."""
    return FakeDatabase(customers=customers, orders=orders)
