# VisageAi


#AI Beauty Advisor

An intelligent beauty advisor application powered by Google's Gemini AI that provides personalized makeup and accessory recommendations based on facial analysis.

## Features

- **Facial Analysis**: Uses MediaPipe to analyze facial features including face shape, measurements, and skin tone
- **Personalized Recommendations**: Generates customized beauty recommendations using Gemini Pro
- **Multiple Input Methods**: Support for both camera capture and image upload
- **User Authentication**: Secure login system with user account management
- **Chat Interface**: Interactive beauty assistant chatbot for follow-up questions
- **Analysis History**: Keeps track of previous analyses and recommendations
- **Real-time Processing**: Instant feedback and recommendations

## Technologies Used

- Python 3.x
- Streamlit
- Google Generative AI (Gemini Pro & Gemini Pro Vision)
- MediaPipe
- OpenCV
- SQLite
- bcrypt

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Run the main application:
```bash
streamlit run main.py
```

2. Create an account or login with existing credentials
3. Upload a photo or take a picture using your camera
4. Get personalized beauty recommendations
5. Chat with the AI beauty assistant for additional advice

## Project Structure

- `main.py`: Primary application entry point
- `beauty_advisor.py`: Core facial analysis and recommendation logic
- `login.py`: User authentication system
- `chat.py`: Chat interface implementation
- `vision.py`: Image processing and Gemini Vision API integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Generative AI
- MediaPipe Face Mesh
- Streamlit Community
