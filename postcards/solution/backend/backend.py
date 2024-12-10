from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from openai import AzureOpenAI
import requests
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import json
import traceback

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-10-21"
)

app = FastAPI()

# Define the Postcard model
class Postcard(BaseModel):
    imageData: str  # Base64 encoded image data
    text: str

# Email configuration
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")

class EmailRequest(BaseModel):
    recipient_email: EmailStr
    postcard: Postcard

class GeneratePostcardRequest(BaseModel):
    name: str
    email: EmailStr
    description: str

@app.post("/generate_postcard", response_model=Postcard)
async def generate_postcard(request: GeneratePostcardRequest):
    try:
        # Generate postcard text using GPT-4
        gpt_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are part of an automatic system that generates warm, inspiring and friendly Christmas postcard texts. You receive a description of the postcard content and generate a text in no more than 2 paragraphs. Use emojis and be creative!"},
                {"role": "user", "content": request.description}
            ],
            max_tokens=500
        )
        postcard_text = gpt_response.choices[0].message.content.strip()

        print("Postcard text:\n" + postcard_text)

        gpt_dalle_prompt_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are part of an automatic system that generates warm, inspiring and friendly Christmas postcards. You receive a description of the postcard content and generate a prompt that will be used later in Dall-e-3 model to generate the postcard image using AI. Answer only with a prompt that will be used in the next step."},
                {"role": "user", "content": request.description}
            ],
            max_tokens=500
        )

        gpt_dalle_prompt = gpt_dalle_prompt_response.choices[0].message.content.strip()

        print("Dalle prompt:\n" + gpt_dalle_prompt)

        # Generate postcard image using Dall-e-3
        dalle_response = client.images.generate(
            model="dall-e-3",
            prompt=gpt_dalle_prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )

        image_data = dalle_response.data[0].b64_json

        print("Image data:\n" + image_data[:50])

        return Postcard(imageData=image_data, text=postcard_text)
    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
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
        print("Exception occurred:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
