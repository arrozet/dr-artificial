# Dr. Artificial

Dr. Artificial is an AI-powered virtual doctor designed for the **Dedalus Datathon Andalucia 2025**. It leverages state-of-the-art (SOTA) machine learning models to provide insightful and data-driven responses in a healthcare environment, aiming to improve patient data analysis and clinical decision support.

## Features

- **Conversational AI:** Capable of answering medical-related queries with high accuracy while minimizing hallucinations.
- **Contextual Memory:** Retains conversation history to support chained question-answering.
- **Data Visualization:** Generates graphical and non-textual responses using **Mermaid.js**.
- **Actionable Insights:** Recommends next steps based on knowledge base data.
- **Scalable and Modular Architecture:** Implements **prompt engineering** techniques and efficiently processes synthetic datasets.
- **Efficient LLM Usage:** Optimized for sustainable and cost-effective model inference using **Amazon Bedrock via LiteLLM**.

## Project Structure

```
├── README.md  # Project documentation
├── requirements.txt  # Dependencies
├── datos/  # Synthetic patient datasets
│   ├── chats/  # Conversation history
│   ├── r_dataton/  # Data analysis scripts
│   └── users/  # User profiles
├── model/  # Core AI model
│   ├── api/  # API endpoints
│   ├── config/  # Model configurations
│   ├── data/  # Processed medical data
│   └── utils/  # Utility scripts
├── web/  # Web application interface
│   ├── app/  # Flask application
│   ├── static/  # CSS and JS files
│   ├── templates/  # HTML templates
│   └── run.py  # Web server entry point
└── logo/  # Branding assets
```
## Prerequisites

- **API Key:** A valid API key for **Amazon Bedrock** is required.
- **Model Connection:** Connection may need to be adjusted to match the used model.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/dr-artificial.git
   cd dr-artificial
   ```

2. **Set Up a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Web Application:**
   ```bash
   python web/run.py
   ```

## AI Model Details

- **LLM Model:** Claude 3.5 Sonnet via Amazon Bedrock (accessed through LiteLLM). Any model could be used.
- **Embeddings:** Amazon Titan Text Embeddings V2
- **RAG (Retrieval-Augmented Generation):** Utilized for efficient contextual retrieval and cost reduction.
- **Response Format:** Markdown-based with Mermaid.js for graphical representation.

## Future Improvements

- **Vector Database Storage:** Transition from file-based storage to a vector database.
- **AI-Powered Preprocessing:** Automate data extraction from databases via queries leveraging other AIs, as DeepSeek.
- **File & Image Attachments:** Support for handling diverse document types.
- **Automated Report Generation:** Beyond simple assistance, full document generation.

## Contributing

We welcome contributions! Please open an issue or submit a pull request for improvements.

## License

This project was developed as part of the **Dedalus Datathon Andalucia 2025** and is intended for educational and research purposes only. It is provided "as is" without warranty of any kind. Use at your own risk.