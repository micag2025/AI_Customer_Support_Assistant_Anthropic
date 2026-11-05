




## Architecture structure   

The following diagram illustrates the main communication flow:  


        ┌──────────────────────────┐
        │       User               │
        │  Asks a support question │
        └────────────┬─────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │      Streamlit UI        │
        │  Receives user request   │
        └────────────┬─────────────┘
                     │
               Send request
                     │
                     ▼
        ┌──────────────────────────┐
        │     Anthropic Claude     │
        │ Understands the request  │
        │ Selects the required tool│
        └────────────┬─────────────┘
                     │
                Tool request
                     │
                     ▼
        ┌──────────────────────────┐
        │      Python Backend      │
        │   Executes the tool      │
        │   Applies business rules │
        └────────────┬─────────────┘
                     │
                Read / Update
                     │
                     ▼
        ┌──────────────────────────┐
        │    Simulated Database    │
        │   Customers              │
        │   Orders                 │
        │   Shipping Events        │
        └────────────┬─────────────┘
                     │
                Return data
                     │
                     ▼
        ┌──────────────────────────┐
        │      Python Backend      │
        │   Returns tool result    │
        └────────────┬─────────────┘
                     │
                Tool result
                     ▼
        ┌──────────────────────────┐
        │     Anthropic Claude     │
        │  Generates final answer  │
        └────────────┬─────────────┘
                     │
                Final response
                     ▼
        ┌──────────────────────────┐
        │       Streamlit UI       │
        │   Displays response      │
        └──────────────────────────┘


*Figure 1 — Simplified system architecture showing how a user request travels through Streamlit, Anthropic Claude, the Python backend, and the simulated database before the final response is returned to the user. (Logical architecture and communication flow of the customer-support assistant.)*


## Repository structure 

```bash
AI_Customer_Support_Assistent_Anthropic/
├── Screenshots/
│   ├── Screenshot_14-10-2026_183433_localhost.jpeg
│   ├── Screenshot_14-10-2026_183833_localhost.jpeg
│   ├── Screenshot_14-10-2026_184035_localhost.jpeg
│   ├── Screenshot_14-10-2026_18413_localhost.jpeg
│   └── Screenshot_14-10-2026_184155_localhost.jpeg
├── .env_example
├── app.py
├── helper.py
├── LICENSE
├── README.md
├── requirements.txt
├── support_backend.py
└── Tool_Use_Streamlit.ipynb
```


## References  




---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---  

## Contact
If you encounter bugs, have questions, or want to request a new feature, please open an issue on this repository.

---  

## Acknowledgements  

TO BE DRAFTED  

---


