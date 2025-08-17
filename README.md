# Meeting Summarizer Agent

A full-stack web application that leverages a generative AI model to summarize meeting transcripts. Users can input a transcript, provide an optional custom prompt to guide the output, edit the resulting summary, and share it directly via email.

## Features

* **AI-Powered Summarization:** Quickly condense long meeting transcripts into concise summaries.
* **Customizable Prompts:** Guide the AI to focus on specific aspects of the meeting, such as action items, key decisions, or specific topics.
* **Editable Output:** The generated summary is presented in an editable text area, allowing for user verification and refinement before sharing.
* **Integrated Email Sharing:** Seamlessly send the final summary to any recipient directly from the application's interface.
* **Responsive UI:** A clean and modern user interface built to work on both desktop and mobile devices.

## Technology Stack

* **Frontend:** Vue.js (v3), Tailwind CSS
* **Backend:** Python, Flask
* **AI Model:** Google Gemini API
* **Email Service:** Gmail SMTP

## Setup and Installation

Follow these steps to get the application running locally.

### Prerequisites

* Python 3.7+
* A Google Gemini API Key
* A Gmail account with 2-Step Verification enabled and an App Password generated.

 1. Clone the Repository

```bash
git clone [https://github.com/yaaashhh725/Meeting_summarizer.git](https://github.com/yaaashhh725/Meeting_summarizer.git)
cd meeting-summarizer
```

 2. Configure Environment Variables
Create a file named .env in the root of the project directory. This file will store your secret keys and credentials. Add the following variables, replacing the placeholder values with your actual credentials.

.env
```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
GMAIL_EMAIL="your.email@gmail.com"
GMAIL_APP_PASSWORD="your-16-digit-app-password"
```
 3. Install Backend Dependencies
Install the required Python packages using the requirements.txt file.

```Bash
pip install -r requirements.txt
```

 4. Run the Backend Server
Start the Flask application.

```Bash
python main.py
```
The backend server will now be running on http://127.0.0.1:5000.

 5. Launch the Frontend
Go to the base url your app

### How to Use
1. Ensure the Flask backend server is running.

2. Paste the meeting transcript into the "Meeting Transcript" text area.

3. (Optional) Provide a custom prompt to direct the summarization (e.g., "List all action items and their owners").

4. Click the Generate Summary button.

5. Wait for the AI to process the transcript and generate the summary.

6. Review and edit the summary in the text area as needed.

7. To share, enter a recipient's email address and click the Send Email button.
