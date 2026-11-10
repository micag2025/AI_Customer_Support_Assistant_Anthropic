
# Building an AI-Powered Customer Support Assistant with Anthropic Claude  

A practical customer-support chatbot built with **Anthropic Claude, Python, and Streamlit**. The application uses Claude's tool-calling capabilities to retrieve customer and order information and execute controlled support operations through a Python backend.

## Overview  

This repository contains the full implementation of the publication **Building an AI-Powered Customer Support Assistant with Anthropic Claude**, published on the **Ready Tensor platform**.  

Customer-support teams frequently handle recurring requests such as:

- Looking up an order.  
- Checking order and shipping status.  
- Retrieving shipment tracking information.  
- Checking refund eligibility.  
- Requesting an order cancellation.  

This project demonstrates how a large language model (LLM) can support these workflows through a conversational interface.

Instead of simply generating answers, the assistant can identify when it needs information from the application and invoke predefined Python tools to retrieve data or perform an operation.

The project uses Anthropic Claude for natural-language understanding and tool selection, Python for the backend logic, and Streamlit for the user interface.

> _Important: This is a demonstration application. Customer, order, and shipping information is simulated. Refund and cancellation operations affect only the demo backend; no real payments, shipments, or customer accounts are modified._

---    

## Who Is This Project For?

This project is intended for:

- Customer support agents
- E-commerce businesses
- Online retailers
- Small and medium-sized businesses (SMBs)
- Customer service managers
- AI developers and students
- Software developers interested in LLMs and tool calling

It provides both a practical example of AI-assisted customer support and a learning resource for developers exploring Anthropic Claude, Python, Streamlit, and API-based tool integration.  

---

## Main Features  

- **Conversational interface**: Interact with the assistant using natural language.  
- **Order lookup**: Retrieve information about demo customer orders.  
- **Shipping information**: Check shipment status and available tracking events.  
- **Refund eligibility**: Check whether an order meets the demo refund conditions.  
- **Order cancellation**: Request cancellation through a controlled backend operation.    
- **Tool calling**: Allow Claude to invoke predefined Python functions when a request requires application data or an action.
- **Confirmation safeguards**: Sensitive operations require explicit user confirmation.  
- **Demo database**: Work with a simulated collection of customers, orders, and shipping events.    

---  

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and backend logic |
| Anthropic Claude API | Language model and tool calling |
| Streamlit | Web-based conversational interface |
| python-dotenv | Loading environment variables |
| Simulated database | Demo customer, order, and shipping data |  

---  

## Project Structure (Repository structure) 

```text
AI_Customer_Support_Assistent_Anthropic/
│
├── Screenshots/          # UI output examples
│   ├── Screenshot_Interface.jpeg
│   ├── Screenshot_Customer_Lookup.jpeg
│   ├── Screenshot_Order_Information.jpeg
│   ├── Screenshot_Shipping_Tracking.jpeg
│   ├── Screenshot_Order_Cancellation.jpeg
│   ├── Screenshot_Refund_Eligibility.jpeg
│   ├── Screenshot_Unknown_customer.jpeg
│   └── Screenshot_Missing_required_information.jpeg
├── .env_example          # Example environment configuration
├── app.py                # Streamlit user interface
├── helper.py
├── requirements.txt      # Python dependencies
├── support_backend.py    # Demo database, tools, and backend logic
├── .gitignore            # Files excluded from Git
├── LICENSE               # Project license
├── README.md             # Project documentation

```

## Dataset Overview

The project uses a fictional, in-memory customer-support dataset embedded directly in the `support_backend.py` file. It consists of 10 customer records and 12 order records.

The dataset includes:

- **Customer information:** Customer IDs, names, email addresses, phone numbers, and usernames.
- **Order details:** Order IDs, product names, quantities, unit prices, and order statuses.
- **Shipping information:** Shipping status, carrier (UPS, USPS, and FedEx), tracking numbers, estimated delivery dates, and tracking events.
- **Refund information:** Refund status, eligibility, and simulated refund amounts in USD.

The data supports demonstrations of customer lookup, order management, shipment tracking, order cancellation, and refund workflows.

**Note:** All records are fictional and stored in memory. No separate dataset file is required, and no real shipping or payment services are connected.

---  

## Available Tools

Based on the actual `support_backend.py` file, there are seven tools defined and implemented. Thus, the customer-support assistant uses seven tools to interact with the simulated customer-support database. These tools allow Claude to retrieve customer and order information, check shipping details, and perform eligible order-management operations.

| Tool | Description | Required Input |
|---|---|---|
| `get_user` | Finds a customer using their email address, phone number, or username. | `key`, `value` |
| `get_order_by_id` | Retrieves the details and current status of a specific order. | `order_id` |
| `get_customer_orders` | Lists all orders associated with a customer. | `customer_id` |
| `cancel_order` | Cancels an order if its status is Processing. | `order_id` |
| `get_shipping_status` | Retrieves the carrier, tracking number, estimated delivery date, shipping status, and tracking events. | `order_id` |
| `check_refund_eligibility` | Checks whether an order qualifies for a refund and calculates the potential refund amount. | `order_id` |
| `issue_refund` | Records a simulated refund after eligibility has been verified and the customer has explicitly confirmed the action. | `order_id` |


> _Note : All seven tools are defined in the tools list and connected to their corresponding Python functions through process_tool_call()_

Each tool is defined through Anthropic's tool-use interface and executed by the Python backend through a dedicated dispatcher. Claude determines when a tool is needed, while the backend validates and executes the requested operation. Sensitive actions, such as cancellations and refunds, are subject to eligibility checks and explicit customer confirmation. All operations use fictional, in-memory data; no real orders or payments are affected.

## How Tool Use Works

Tool use allows Claude to interact with external functions and systems through the Python application. In this project, Claude can request operations such as retrieving customer information, checking order details, tracking shipments, and processing eligible order-management actions.

The tools are defined in `support_backend.py` and passed to Claude through the Anthropic Messages API. Claude determines when a tool is needed and generates a structured request containing the tool name and its input arguments. The Python application receives the request, executes the corresponding function, and sends the result back to Claude.

**Claude does not execute Python functions directly.** The application is responsible for executing the requested operations and controlling access to the simulated database.

### Conceptual Flow

```text
User
  ↓
Streamlit application (app.py)
  ↓
Claude – Anthropic Messages API
  ↓
Structured tool request
  ↓
Python backend (support_backend.py)
  ↓
Tool execution
  ↓
Tool result
  ↓
Claude
  ↓
Final response
  ↓
Streamlit interface
```

### The Tool-Use Message Loop

The application implements an iterative message exchange through the `run_assistant()` function in `app.py`.

The process follows these steps:

1. **User request:** The user submits a message through the Streamlit chat interface.
2. **API request:** The application sends the conversation history, system prompt, and available tool definitions to Claude using `client.messages.create()`.
3. **Claude response:** Claude determines whether it can answer directly or needs to request one or more tools.
4. **Response handling:** The application checks `response.stop_reason` to determine what to do next.
5. **Tool execution:** If Claude requests tools, the application processes each `tool_use` block and calls `process_tool_call()` from `support_backend.py`.
6. **Tool results:** The application collects the results and sends them back to Claude in a new message.
7. **Final response:** Claude processes the returned results and either requests additional tools or produces its final response.

The application uses the following `stop_reason` values:

| `stop_reason` | Meaning |
|---|---|
| `tool_use` | Claude is requesting one or more tools. |
| `end_turn` | Claude has completed its response. |
| Other values | The application raises an error because the response is not handled by the current implementation. |

### Example: Processing a Tool Request

For example, when a customer asks to look up their account using an email address, Claude may request the `get_user` tool.

The request is represented by a `tool_use` content block. The application accesses its attributes directly:

```python
block.name   # "get_user"
block.input  # {"key": "email", "value": "john@gmail.com"}
block.id     # Identifier for this tool request
```

The application passes the tool name and input arguments to the backend dispatcher:

```python
result = process_tool_call(block.name, block.input)
```

In `support_backend.py`, the `process_tool_call()` function maps the requested tool name to the corresponding Python method:

```python
dispatch = {
    "get_user": db.get_user,
    "get_order_by_id": db.get_order_by_id,
    "get_customer_orders": db.get_customer_orders,
    "cancel_order": db.cancel_order,
    "get_shipping_status": db.get_shipping_status,
    "check_refund_eligibility": db.check_refund_eligibility,
    "issue_refund": db.issue_refund,
}

return dispatch[tool_name](**tool_input)
```

The backend executes the selected method against the simulated database and returns its result.

### Returning Tool Results to Claude

After executing the requested tools, the application converts each result into JSON and creates a `tool_result` content block:

```python
result_text = json.dumps(result, ensure_ascii=False, default=str)

tool_results.append({
    "type": "tool_result",
    "tool_use_id": block.id,
    "content": result_text,
})
```

The `tool_use_id` associates the result with the original tool request.

The application then appends all collected tool results to the conversation as a user message:

```python
messages.append({
    "role": "user",
    "content": tool_results
})
```

If a tool execution raises an exception, the application also returns an error result with `is_error=True`, allowing the tool failure to be reported to Claude.

The `while True` loop in `run_assistant()` then calls Claude again with the updated conversation. This process continues until Claude returns `end_turn`, at which point the application extracts the text response and displays it in Streamlit.

**Key principle:** Tool use is an iterative message exchange. Claude decides which tools to request, the Python backend executes them, and the results are returned to Claude so it can generate an informed response.  

## Streamlit application 

The `app.py` file is the main application entry point. It builds the user interface using Streamlit, manages the chat interaction between the user and Anthropic Claude, and handles the tool-calling workflow. It sends user messages and available tool definitions to Claude, processes Claude’s responses, and passes requested operations to the Python backend (support_backend.py). Finally, it displays the assistant’s responses in the chat interface, allowing users to interact with the customer-support assistant.

---
## Installation & Setup

This section shows how to install dependencies, configure authentication, and run the full pipeline.

### Prerequisites:

- Python 3.10+    
- Anthropic Clauude API key    

### Clone the repository

```bash
git clone https://github.com/micag2025/AI_Customer_Support_Assitent_Anthropic.git
cd AI_Customer_Support_Assitent_Anthropic
```

### Create a virtual environment

On Windows:

```bash
py -m venv .venv
.venv\Scripts\activate
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
python -m pip install streamlit anthropic python-dotenv
```

### Configure the Anthropic API key

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_actual_anthropic_api_key
```

Here the model 'claude-sonnet-5' has been selected and used. If the backend requires another configurable `model name`, also add the corresponding model setting used by `support_backend.py`. 

---  

## Running the Application

From the project directory, execute:

```bash
python -m streamlit run app.py
```

Streamlit will start the application and provide a local URL, normally:

```text
http://localhost:8501
```

Open that address in your browser to interact with the customer-support assistant.  

To stop the application, in the terminal where Streamlit is running, press:

```bash
Ctrl+C
```
---    

## How It Works

The application separates the conversational layer from the business logic.

1. The user enters a request through the Streamlit chat interface.
2. The application sends the conversation and available tool definitions to Anthropic Claude.
3. Claude interprets the request and determines whether one of the available tools is needed.
4. If a tool is requested, the Python backend executes the corresponding function.
5. The tool result is returned to Claude.
6. Claude uses the result to formulate a response for the user.
7. For sensitive operations, the application follows its confirmation and eligibility checks before executing the action.

---

## Example Queries for Testing the Application

The following examples can be used to test the Streamlit customer-support assistant and explore its main functionalities. They cover both successful interactions and scenarios involving errors, incomplete requests, and business-rule restrictions.

### 1. Customer Lookup
- "Find the customer with email address john@gmail.com."
- "Show me all orders associated with this customer."

### 2. Order Information
- "Retrieve the details of order 24601."
- "What is the current status of order 13579?"

### 3. Shipping and Tracking
- "Where is my order 24601, and when is it expected to arrive?"
- "Provide the latest tracking updates for order 54321."
- "Has order 86420 been delivered?"

### 4. Order Cancellation
- "I would like to cancel order 13579. Is that possible?"
- "Can order 97531 still be cancelled?"

The assistant should check the order status and request explicit customer confirmation before attempting cancellation. Only orders with a *Processing* status can be cancelled.

### 5. Refund Eligibility and Processing
- "Am I eligible for a refund for order 86420?"
- "Why is order 54321 not eligible for a refund?"
- "I would like to request a refund for order 86420. Can you check its eligibility?"

After the assistant confirms eligibility, reply:
- "Yes, I confirm that I want to proceed with the refund."

Refund processing requires an eligibility check and explicit customer confirmation. Refunds are recorded in the simulated database; no actual payment is processed.

### 6. Error Handling and Negative Test Cases

The following queries test how the assistant handles unsuccessful tool calls, invalid inputs, missing information, and business-rule restrictions.

- **Unknown customer:** "Find the customer with email address unknown@example.com."  
  Expected behaviour: The assistant reports that no matching customer was found.

- **Unknown order:** "Retrieve the details of order 99999."  
  Expected behaviour: The assistant explains that the order could not be found.

- **Invalid order ID:** "Check the shipping status of order ABC-XYZ."  
  Expected behaviour: The assistant reports that no matching order was found and asks the user to verify the order ID. The current backend does not implement a separate order-ID format validation.

- **Cancellation of an already shipped order:** "I would like to cancel order 24601. Can you do that?"  
  Expected behaviour: The backend rejects the cancellation because the order is already shipped. The assistant explains that only orders with a *Processing* status can be cancelled.

- **Missing required information:** "Where is my order?"  
  Expected behaviour: The assistant asks the user to provide an order ID before attempting to retrieve shipping information.

These examples demonstrate how the assistant interprets natural-language requests, selects and invokes the appropriate tools, retrieves or updates information, and handles unsuccessful operations. They also highlight the importance of backend validation, business-rule enforcement, and clear communication when a requested action cannot be completed.

---

## Example Use Cases (UI Walkthrough & Example Runs)  

### Web UI  

The application features a clean, dark-themed interface built with Streamlit. The sidebar provides an overview of the available `customer-support functions`, including `order tracking`, `order lookup`, `refund eligibility checks`, and `order cancellations`. It also includes access to fictional demo records and a button to clear the conversation. The main area displays the application title, a notice explaining the simulated environment, and a `chat input where users can submit questions or requests`. This simple layout makes the assistant easy to navigate and interact with while demonstrating its main customer-support capabilities.

![Web_UI](Screenshots/Screenshot_Interface.jpeg)

---  

Once the application is running, you can try requests such as:

### Order lookup

![Example1](Screenshots/Screenshot_Customer_Lookup.jpeg)    

---

### Order Information

![Example2](Screenshots/Screenshot_Order_Information.jpeg)    

---  

### Shipping and Tracking Information

![Example3](Screenshots/Screenshot_Shipping_Tracking.jpeg)    

---  

### Order Cancellation  

![Example4](Screenshots/Screenshot_Order_Cancellation.jpeg)    

---  

### Refund Eligibility and Processing

![Example5](Screenshots/Screenshot_Refund_Eligibility.jpeg)   

---  

### Error Handling and Negative Test Case : Missing Required Information  

![Example6](Screenshots/Screenshot_Missing_required_information.jpeg)    

---  

### Error Handling and Negative Test Case : Unknown Customer  

![Example7](Screenshots/Screenshot_Unknown_customer.jpeg)   


The actual outcome depends on the demo records and the business rules implemented in the backend.  

---

## Safety and Limitations

This repository is intended for learning and experimentation.

- The database contains fictional demonstration records.
- Order and shipping information is not retrieved from real external services.
- Refund and cancellation operations are simulated.
- No real payment processor or logistics provider is connected.
- The application should not be used to handle real customer information or transactions without additional security and operational controls.

A production implementation would require persistent data storage, user authentication, authorization, secure API integrations, audit logging, error handling, and appropriate privacy controls.  

---  

## Possible Future Improvements

The project provides a starting point for further development. Potential extensions include:

- Replacing the simulated database with a persistent database.
- Integrating real shipping and tracking APIs.
- Connecting to a payment provider in a controlled test environment.
- Adding authentication and role-based authorization.
- Introducing audit logs for sensitive operations.
- Adding automated tests for backend functions and tool execution.
- Improving observability, error handling, and conversation management.
- Exploring more advanced agent workflows.

---  

## Contributing  

Contributions are welcomed to improve the Anthropic Claude Customer Support Assistant. The suggested workflow is the following:    

- Fork the GitHub repository  
- Create a feature branch:
  
```bash  
git checkout -b feat/your-feature
```
- Commit and push your changes  
- Submit a Pull Request and describe your contribution.  

>_Note : Please follow the repository code style and add tests for major features._

---  

## References    

- [Claude Platform documentation](https://platform.claude.com/docs/en/home)    
- [Anthropic](https://www.anthropic.com/)
- [Streamlit documentation](https://docs.streamlit.io/)    
- [Technical Evaluation Rubric](https://app.readytensor.ai/publications/technical-excellence-in-aiml-and-data-science-publications-an-evaluation-rubric-WsaE5uxLBqnH)  
- [Engage and Inspire: Best Practices for Publishing on Ready Tensor](https://app.readytensor.ai/publications/engage-and-inspire-best-practices-for-publishing-on-ready-tensor-SBgkOyUsP8qQ)
- [The Open Source Repository Guide](https://app.readytensor.ai/publications/best-practices-for-ai-project-code-repositories-0llldKKtn8Xb)
- [Markdown for Machine Learning Projects: A Comprehensive Guide](https://app.readytensor.ai/publications/markdown-for-machine-learning-projects-a-comprehensive-guide-LX9cbIx7mQs9)  


---

## License
This project is licensed under the [MIT License](/LICENSE).  

---  

## Contact
If you encounter bugs, have questions, or want to request a new feature, please open an [issue](https://github.com/micag2025/AI_Customer_Support_Assitent_Anthropic/issues/) on this repository.

---  

## Acknowledgements  

An acknowledgement to Ready Tensor developer community for creating a vibrant ecosystem where AI professionals can share projects, insights, and innovations, playing a meaningful role in accelerating the advancement of AI technology and in shaping practical, real-world developer tools such as this project.

---


