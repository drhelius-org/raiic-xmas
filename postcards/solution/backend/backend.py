from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import openai
import requests
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import base64

load_dotenv()

app = FastAPI()

# Define the Postcard model
class Postcard(BaseModel):
    imageData: str  # Base64 encoded image data
    text: str

# Azure OpenAI and Dall-e-3 configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
dalle_api_url = os.getenv("DALLE_API_URL")
dalle_api_key = os.getenv("DALLE_API_KEY")

# Email configuration
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")

class EmailRequest(BaseModel):
    recipient_email: EmailStr
    postcard: Postcard

@app.post("/generate_postcard", response_model=Postcard)
async def generate_postcard(user_instructions: str):
    try:
        # Generate postcard text using GPT-4
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Generate a warm and friendly Christmas postcard text."},
                {"role": "user", "content": user_instructions}
            ],
            max_tokens=150
        )
        postcard_text = gpt_response.choices[0].message['content'].strip()

        # Generate postcard image using Dall-e-3
        dalle_response = requests.post(
            dalle_api_url,
            headers={"Authorization": f"Bearer {dalle_api_key}"},
            json={"prompt": "Christmas postcard image"}
        )
        dalle_response.raise_for_status()
        image_data = dalle_response.json()["data"]

        return Postcard(imageData=image_data, text=postcard_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send_postcard")
async def send_postcard(email_request: EmailRequest):
    try:
        # Decode the base64 image data
        image_data = base64.b64decode(email_request.postcard.imageData)

        # Create the email
        msg = MIMEMultipart("alternative")
        msg['From'] = smtp_user
        msg['To'] = email_request.recipient_email
        msg['Subject'] = "Your Christmas Postcard"

        # Create the HTML content
        html_content = f"""
        <html>
        <body>
            <img src="data:image/png;base64,{email_request.postcard.imageData}" alt="Postcard Image" />
            <p>{email_request.postcard.text}</p>
        </body>
        </html>
        """

        # Attach the HTML content
        msg.attach(MIMEText(html_content, "html"))

        # Send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, email_request.recipient_email, msg.as_string())
        server.quit()

        return {"message": "Postcard sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
