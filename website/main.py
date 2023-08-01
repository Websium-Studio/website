from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import smtplib
from email.message import EmailMessage
from pydantic import BaseModel

app = FastAPI()
app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")
templates = Jinja2Templates(directory="templates")


class ContactForm(BaseModel):
    name: str
    email: str
    country: str 
    message: str

@app.post("/", response_class=HTMLResponse)
async def contact_us(request: Request, form: ContactForm):
    # Extract form data
    name = form.name
    email = form.email
    country = form.country
    message = form.message

    # Email configuration
    smtp_server = "smtp.office365.com"
    smtp_port = 587  # Change to the appropriate port for your SMTP server
    sender_email = "websiumbot@outlook.com"
    sender_password = "DigvijayThakur@123"
    receiver_email = "websium@outlook.com"

    # Create an EmailMessage
    msg = EmailMessage()
    msg.set_content(f"Name: {name}\nEmail: {email}\nCountry: {country}\n\n{message}")
    msg["Subject"] = "Contact Us Form Submission"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        # Send the email using the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return JSONResponse(content={"message": "Message sent successfully"})
    except Exception as e:
        return JSONResponse(content={"message": "Error sending the message"}, status_code=500)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/toc", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("toc.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9000)

