
# StackIt Hiring Assignment

#File to Google Sheet

This Django application allows users to upload a file and create a Google Sheet with the filtered and cleaned data. The sheet is then shared with the user's Gmail account.

#Working:

The user uploads a file.
The application filters out unwanted columns and cleans missing data.
A Google Sheet is created and the data is written to it using the Gspread API.
The user's Gmail address is obtained and the sheet URL is shared with them.
The sheet URL is displayed to the user.

#Stack:

Django
Gspread API

#Usage:

Clone the repository and install the dependencies:
git clone https://github.com/your-username/file-to-google-sheet.git
cd file-to-google-sheet
pip install -r requirements.txt
Create a .env file in the project root directory and add your Google API credentials:
GOOGLE_API_KEY=YOUR_API_KEY
Start the development server:
python manage.py runserver
Visit http://localhost:8000 in your web browser.

Click the "Upload File" button and select the file you want to upload.

Click the "Create Sheet" button.

Enter your Gmail address and click the "Share Sheet" button.

The sheet URL will be displayed.

You can then open the sheet in Google Sheets to view the data.

Limitations:

Encoding and feature scaling are not implemented due to time constraints.
The user's Gmail address is obtained using Django's built-in authentication system. This means that users must create an account and log in to use the application.