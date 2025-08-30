# 🤖 Personal Finance Chatbot

An intelligent financial advisory chatbot powered by OpenRouter AI services, providing personalized financial guidance, budget analysis, and spending insights.

![Personal Finance Chatbot](https://img.shields.io/badge/OpenRouter-API-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green) ![Streamlit](https://img.shields.io/badge/Streamlit-1.24.1-red) ![HuggingFace](https://img.shields.io/badge/HuggingFace-NLP-orange)

## ✨ Features

- **💬 AI-Powered Q&A**: Get personalized financial advice using OpenRouter LLM
- **📊 Budget Analysis**: Comprehensive budget summaries with actionable insights
- **🔍 Spending Insights**: Deep analysis of spending patterns and financial goals
- **📈 NLU Analysis**: Sentiment and entity analysis using Hugging Face models
- **🎯 Persona-Based Advice**: Tailored guidance for students and professionals
- **🎨 Modern UI**: Cyberpunk-inspired interface with responsive design

## 🏗️ Architecture

```
personal-finance-chatbot/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application
│   ├── routes.py           # API endpoints
│   ├── ibm_api.py          # IBM Watson integration
│   ├── prompts.py          # Prompt engineering templates
│   └── requirements.txt    # Python dependencies
├── frontend/               # Streamlit frontend
│   └── streamlit/
│       ├── app.py          # Main application
│       └── requirements.txt # Frontend dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- IBM Cloud account with Watson services
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd personal-finance-chatbot
```

### 2. Set Up IBM Watson Services

1. **Create IBM Cloud Account**: [Sign up here](https://cloud.ibm.com/registration)
2. **Enable Watson Services**:
   - IBM Watson Natural Language Understanding
   - IBM Watsonx.ai (Granite models)
3. **Get API Credentials**:
   - NLU API Key and URL
   - Watsonx API Key, URL, and Project ID

## 3. Environment Configuration

Copy the example environment file and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your OpenRouter credentials:

```env
# OpenRouter API Configuration (REQUIRED)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# OpenRouter Optional Configuration
OPENROUTER_MODEL=gpt-4o-mini
OPENROUTER_TIMEOUT=30

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

### 4. Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install backend dependencies
cd backend
pip install -r requirements.txt
```

### 5. Frontend Setup

```bash
# Install frontend dependencies
cd frontend/streamlit
pip install -r requirements.txt
```

### 6. Run the Application

**Start the Backend Server:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Start the Frontend:**
```bash
cd frontend/streamlit
streamlit run app.py
```

The application will be available at:
- Backend API: http://localhost:8000
- Frontend UI: http://localhost:8501
- API Documentation: http://localhost:8000/docs

## 📋 API Endpoints

### POST `/generate`
Generate financial advice based on user query and persona.

**Request:**
```json
{
  "question": "How can I save money as a student?",
  "persona": "student"
}
```

### POST `/budget-summary`
Generate comprehensive budget analysis.

**Request:**
```json
{
  "income": 3000.0,
  "expenses": {
    "Rent": 1200.0,
    "Food": 400.0,
    "Transport": 200.0
  },
  "savings_goal": 500.0,
  "persona": "student"
}
```

### POST `/spending-insights`
Generate deep spending behavior analysis.

**Request:**
```json
{
  "income": 3000.0,
  "expenses": {
    "Rent": 1200.0,
    "Food": 400.0
  },
  "goals": [
    {
      "name": "Emergency Fund",
      "amount": 1000.0,
      "timeline": "3 months"
    }
  ],
  "persona": "student"
}
```

### POST `/nlu`
Analyze text sentiment and entities.

**Request:**
```json
{
  "question": "I'm struggling to save money each month"
}
```

## 🎨 UI Features

### Home Page
- Overview of all features
- Quick navigation cards
- Modern cyberpunk design

### Ask Questions
- Persona selection (Student/Professional)
- Real-time conversation history
- Context-aware responses

### Budget Analysis
- Income and expense input
- Savings goal tracking
- Comprehensive financial summaries

### Spending Insights
- Multiple financial goals
- Expense categorization
- Deep behavioral analysis

### NLU Analysis
- Sentiment detection
- Keyword extraction
- Entity recognition

## 🔧 Configuration Options

### Environment Variables
- `DEBUG`: Enable debug mode (True/False)
- `LOG_LEVEL`: Logging level (INFO/DEBUG/ERROR)
- `HOST`: Server host address
- `PORT`: Server port number

### IBM Watson Configuration
- Model selection via `WATSONX_MODEL_ID`
- Custom timeout settings
- Retry mechanisms for API calls

## 🚀 Deployment

### Local Deployment
Follow the Quick Start instructions above for local development.

### Production Deployment

1. **Set up production environment variables:**
   ```env
   DEBUG=False
   LOG_LEVEL=INFO
   ALLOWED_ORIGINS=https://your-domain.com
   ```

2. **Use production server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **Set up reverse proxy (nginx example):**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t finance-chatbot .
docker run -p 8000:8000 --env-file .env finance-chatbot
```

## 🛠️ Development

### Project Structure
```
backend/
├── main.py              # FastAPI application setup
├── routes.py            # API route definitions
├── ibm_api.py          # IBM Watson service integration
├── prompts.py          # LLM prompt templates
└── requirements.txt    # Python dependencies

frontend/streamlit/
├── app.py              # Streamlit application
└── requirements.txt    # Frontend dependencies
```

### Adding New Features

1. **New API Endpoint**:
   - Add route in `backend/routes.py`
   - Create corresponding prompt template in `backend/prompts.py`
   - Update frontend in `frontend/streamlit/app.py`

2. **New UI Feature**:
   - Add navigation option in sidebar
   - Create corresponding container and form elements
   - Connect to backend API endpoints

### Testing
```bash
# Run backend tests
cd backend
python -m pytest

# Test API endpoints
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"question":"How to save money?","persona":"student"}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- IBM Watson for AI capabilities
- FastAPI for the robust backend framework
- Streamlit for the intuitive frontend framework
- Open source community for various libraries and tools

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `/docs` endpoint
- Review the IBM Watson documentation

---

**Note**: This application requires valid IBM Watson credentials. Ensure you have appropriate service instances provisioned on IBM Cloud before running the application.
