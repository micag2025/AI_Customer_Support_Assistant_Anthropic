"""Streamlit UI for the Acme Co customer-support tool-use demo."""

import json
import streamlit as st

from support_backend import client, MODEL_NAME, tools, process_tool_call

st.set_page_config(page_title="Acme Co Support", page_icon="💬", layout="centered")
st.title("Acme Co Customer Support")
st.caption("Demo chatbot for customer lookups, order tracking, cancellations, and refunds.")
st.info("This is a fictional in-memory demo. Tracking events are sample data; refunds do not move real money.")

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


def run_assistant(messages):
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
                result = process_tool_call(block.name, block.input)
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


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "api_messages" not in st.session_state:
    st.session_state.api_messages = []

with st.sidebar:
    st.markdown("## 💬 Acme Support")
    st.caption("AI-powered customer assistance")
    st.divider()

    st.markdown("### What can I help with?")
    st.markdown(
        """
        - 📦 **Track an order**

          Check the latest demo shipping events.

        - 🔎 **Look up an order**

          Review order details and status.

        - ↩️ **Check a refund**

          Review eligibility before requesting a refund.

        - 🛑 **Cancel an order**

          Confirmation is required before cancellation.
        """
    )

    with st.expander("View demo records", expanded=False):
        st.markdown("**Customers**")
        st.caption("John Doe · Priya Patel · Liam Nguyen · and others")
        st.markdown("**Example order IDs**")
        st.code("24601  ·  13579  ·  97531  ·  28164", language=None)

    st.divider()
    st.caption("🧪 Demo environment · Fictional records · No real payments")
    if st.button("🧹 Clear conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.api_messages = []
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
                reply = run_assistant(st.session_state.api_messages)
                st.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")
