# main.py
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib import response
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

# Load environment variables from a .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# To run this code you need to install the following dependencies:
# pip install google-genai


client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

model = "gemini-2.0-flash"

def generate_summary(full_prompt):

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=full_prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    return response

# Change according to new library

# --- Gemini API Configuration ---
# try:
#     gemini_api_key = os.getenv("GEMINI_API_KEY")
#     if not gemini_api_key:
#         raise ValueError("GEMINI_API_KEY not found in environment variables.")
#     genai.configure(api_key=gemini_api_key)
#     model = genai.GenerativeModel('gemini-1.5-flash')
# except Exception as e:
#     print(f"Error configuring Gemini API: {e}")
#     model = None

# --- Gmail (SMTP) Configuration ---
# Your Gmail address from which you'll send emails
sender_email = os.getenv("GMAIL_EMAIL")
# The 16-digit "App Password" you generated from your Google Account
sender_password = os.getenv("GMAIL_APP_PASSWORD")


@app.route("/")
def index():
    """
    A simple route to check if the server is running.
    """
    return render_template("index.html")


@app.route("/api/summarize", methods=["POST"])
def summarize_transcript():
    """
    API endpoint to generate a summary from a transcript.
    Accepts a POST request with a JSON body containing 'transcript' and 'prompt'.
    """
    if not model:
        return jsonify({"error": "Generative model not initialized. Check API key."}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON in request body"}), 400

    transcript = data.get("transcript")
    custom_prompt = data.get("prompt")

    if not transcript:
        return jsonify({"error": "Missing 'transcript' in request body"}), 400

    try:
        full_prompt = f"""
        Based on the following transcript, please provide a summary.
        {custom_prompt if custom_prompt else "Provide a general summary of the key points and decisions."}

        Transcript:
        ---
        {transcript}
        ---
        """
        # response = model.generate_content(full_prompt)
        response = generate_summary(full_prompt)
        return jsonify({"summary": response.text})

    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return jsonify({"error": "Failed to generate summary."}), 500


@app.route("/api/send-email", methods=["POST"])
def send_summary_email():
    """
    API endpoint to send the summary via email using Gmail's SMTP server.
    Accepts a POST request with a JSON body containing 'recipientEmail' and 'summary'.
    """
    if not sender_email or not sender_password:
        return jsonify({"error": "Email service is not configured on the server. Check .env file."}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON in request body"}), 400

    recipient_email = data.get("recipientEmail")
    summary = data.get("summary")

    if not recipient_email or not summary:
        return jsonify({"error": "Missing 'recipientEmail' or 'summary' in request body"}), 400

    # --- Construct the Email ---
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Meeting Summary"
    message["From"] = sender_email
    message["To"] = recipient_email

    # Create the HTML version of the email
    html_content = f"""
    <html>
      <body>
        <h3>Here is your requested meeting summary:</h3>
        <p>{summary.replace('\n', '<br>')}</p>
      </body>
    </html>
    """
    # Attach the HTML part to the MIMEMultipart message
    message.attach(MIMEText(html_content, "html"))

    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            # Log in to your Gmail account
            server.login(sender_email, sender_password)
            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        print(f"An error occurred while sending email: {e}")
        return jsonify({"error": "An internal error occurred while sending the email."}), 500


# This allows the script to be run directly
if __name__ == "__main__":
    app.run(debug=True, port=5000)
