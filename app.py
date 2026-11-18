"""Streamlit UI for the Acme Co customer-support tool-use demo."""

import hashlib
import json

import streamlit as st

from support_backend import create_database, client, MODEL_NAME, tools, process_tool_call


st.set_page_config(page_title="Claude Customer Support Assistant", page_icon="💬", layout="centered")
st.title("Claude Customer Support Assistant")
st.caption("Demo chatbot for customer lookups, order tracking, cancellations, and refunds.")
st.info(
    "Demo environment: customer and order records are stored in memory. "
    "No real shipments or payments are processed."
)

if not st.session_state.get("chat_history"):
    st.markdown("**How can I help you today?**")

SYSTEM_PROMPT = """You are a helpful customer-support assistant for Acme Co, a fictional online retailer.

Use tools to retrieve customer, order, shipping, and refund information. Never invent records,
tracking events, carrier details, delivery dates, or refund results. If an order ID or other
required information is missing, ask a concise follow-up question.

For cancellation or refund actions that change data, obtain explicit customer confirmation in
the conversation before calling the action tool. For refunds, check eligibility first. Explain
that this demo only updates its in-memory data and does not contact a carrier or payment provider.
Keep responses clear, concise, and customer-friendly.
"""


def content_to_text(content):
    """Extract readable text from a sequence of Anthropic content blocks."""
    return "\n\n".join(
        block.text for block in content
        if getattr(block, "type", None) == "text"
    ).strip()


def run_assistant(messages, database):
    """Call Claude and handle tool requests until Claude produces a final answer."""
    while True:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )

        # Preserve the complete assistant message, including tool-use blocks.
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            return content_to_text(response.content) or "No text response was generated."

        if response.stop_reason != "tool_use":
            raise RuntimeError(f"Unexpected stop reason from Claude: {response.stop_reason}")

        tool_results = []
        for block in response.content:
            if getattr(block, "type", None) != "tool_use":
                continue
            try:
                result = process_tool_call(block.name, block.input, database=database)
                result_text = json.dumps(result, ensure_ascii=False, default=str)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result_text,
                })
            except Exception as exc:
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": f"Tool execution failed: {type(exc).__name__}: {exc}",
                    "is_error": True,
                })

        if not tool_results:
            raise RuntimeError("Claude requested tool use, but no tool-use blocks were found.")

        # Multiple results from one assistant turn belong in one user message.
        messages.append({"role": "user", "content": tool_results})


def reset_conversation():
    """Clear both the displayed chat and Anthropic's conversation history."""
    st.session_state.chat_history = []
    st.session_state.api_messages = []


# Each browser session gets its own database instance. The built-in demo records
# are loaded unless a valid JSON dataset is uploaded in the sidebar.
if "support_db" not in st.session_state:
    st.session_state.support_db = create_database()
if "dataset_signature" not in st.session_state:
    st.session_state.dataset_signature = "builtin"
if "dataset_label" not in st.session_state:
    st.session_state.dataset_label = "Built-in demo records"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "api_messages" not in st.session_state:
    st.session_state.api_messages = []

with st.sidebar:
    st.markdown("### Data source")
    uploaded_file = st.file_uploader(
        "Optionally upload your own dataset",
        type=["json"],
        help=(
            "Upload a JSON file containing 'customers' and 'orders' arrays. "
            "The built-in fictional records remain available when no file is uploaded."
        ),
    )

    if uploaded_file is None:
        new_signature = "builtin"
        if st.session_state.dataset_signature != new_signature:
            st.session_state.support_db = create_database()
            st.session_state.dataset_signature = new_signature
            st.session_state.dataset_label = "Built-in demo records"
            reset_conversation()
        st.caption("Using the built-in fictional dataset.")
    else:
        raw_bytes = uploaded_file.getvalue()
        new_signature = hashlib.sha256(raw_bytes).hexdigest()
        if new_signature != st.session_state.dataset_signature:
            try:
                payload = json.loads(raw_bytes.decode("utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("The top level of the JSON file must be an object.")
                if "customers" not in payload or "orders" not in payload:
                    raise ValueError("The JSON file must contain both 'customers' and 'orders' arrays.")

                # Validate the new dataset before replacing the active session database.
                new_database = create_database(
                    customers=payload["customers"],
                    orders=payload["orders"],
                )
                st.session_state.support_db = new_database
                st.session_state.dataset_signature = new_signature
                st.session_state.dataset_label = uploaded_file.name
                reset_conversation()
                st.success("Dataset loaded. Conversation history was cleared.")
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
                st.error(f"Could not load dataset: {exc}")
                st.caption(
                    f"The active dataset remains: {st.session_state.dataset_label}. "
                    "Correct the JSON file and upload it again."
                )
        else:
            st.caption(f"Using uploaded dataset: {st.session_state.dataset_label}")

    st.caption(f"Active dataset: {st.session_state.dataset_label}")

    # Display the records in use, not just the built-in demo records.
    with st.expander("View active dataset", expanded=False):
        active_db = st.session_state.support_db
        customers = active_db.customers
        orders = active_db.orders

        st.markdown(f"**Customers:** {len(customers)}")
        if customers:
            customer_rows = [
                {"Customer ID": str(customer["id"]), "Name": customer["name"]}
                for customer in customers[:20]
            ]
            st.dataframe(customer_rows, hide_index=True, use_container_width=True)
            if len(customers) > 20:
                st.caption(f"Showing 20 of {len(customers)} customers.")
        else:
            st.caption("No customer records in this dataset.")

        st.markdown(f"**Orders:** {len(orders)}")
        if orders:
            order_rows = [
                {
                    "Order ID": str(order["id"]),
                    "Customer ID": str(order["customer_id"]),
                    "Product": order["product"],
                    "Status": order["status"],
                }
                for order in orders[:20]
            ]
            st.dataframe(order_rows, hide_index=True, use_container_width=True)
            if len(orders) > 20:
                st.caption(f"Showing 20 of {len(orders)} orders.")
        else:
            st.caption("No order records in this dataset.")

    st.divider()
    st.markdown("### What can I help with?")
    st.markdown(
        """
        - 📦 **Track an order**

          Check the available shipping events.

        - 🔎 **Look up an order**

          Review order details and status.

        - ↩️ **Check a refund**

          Review eligibility before requesting a refund.

        - 🛑 **Cancel an order**

          Confirmation is required before cancellation.
        """
    )

    st.divider()
    if st.button("🧹 Clear conversation", use_container_width=True):
        reset_conversation()
        st.rerun()


for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about a customer or order..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.session_state.api_messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Checking your request..."):
            try:
                reply = run_assistant(
                    st.session_state.api_messages,
                    st.session_state.support_db,
                )
                st.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")
