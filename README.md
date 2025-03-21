# Dr. Artificial

Dr. Artificial is an AI-powered virtual doctor designed for the **Dedalus Datathon Andalucia 2025**. It leverages state-of-the-art (SOTA) machine learning models to provide insightful and data-driven responses in a healthcare environment, aiming to improve patient data analysis and clinical decision support.

## Features

- **Conversational AI:** Capable of answering medical-related queries with high accuracy while minimizing hallucinations.
- **Contextual Memory:** Retains conversation history to support chained question-answering.
- **Data Visualization:** Generates graphical and non-textual responses (e.g., charts, diagrams).
- **Actionable Insights:** Recommends next steps based on knowledge base data.
- **Scalable and Modular Architecture:** Implements prompt engineering techniques and efficiently processes synthetic datasets.
- **Efficient LLM Usage:** Optimized for sustainable and cost-effective model inference.

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

## Dataset Information

The project utilizes synthetic datasets provided by Dedalus Datathon, including:
- **Patient summaries** (`resumen_pacientes.csv`)
- **Lab results** (`resumen_lab_iniciales.csv`)
- **Medical notes** (`resumen_notas.csv`)
- **Medications and procedures** (`resumen_medicacion.csv`, `resumen_procedimientos.csv`)

## Contributing

We welcome contributions! Please open an issue or submit a pull request for improvements.

## License

This project is developed for the **Dedalus Datathon Andalucia 2025** and is for educational and research purposes only.

## Acknowledgments

Special thanks to Dedalus and the Datathon organizers for providing the datasets and evaluation framework.

