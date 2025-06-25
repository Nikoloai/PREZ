"""FastAPI service to generate PDF presentations from JSON data."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, validator
from typing import List, Optional
import io
import requests
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas

# Pydantic models for request validation
class Slide(BaseModel):
    slide_title: str
    slide_text: str
    image_url: Optional[str] = None

class PresentationRequest(BaseModel):
    title: str
    slides: List[Slide]

    @validator('slides')
    def check_slides(cls, v):
        if not v:
            raise ValueError('slides must not be empty')
        return v

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/', response_class=HTMLResponse)
def root():
    """Serve a simple HTML page for creating presentations."""
    with open('static/index.html', 'r', encoding='utf-8') as file:
        return file.read()


def generate_pdf(data: PresentationRequest) -> io.BytesIO:
    """Create a PDF in memory from the presentation data."""
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    for slide in data.slides:
        pdf.setFont('Helvetica-Bold', 24)
        pdf.drawString(40, height - 50, slide.slide_title)

        pdf.setFont('Helvetica', 14)
        text_object = pdf.beginText(40, height - 100)
        for line in slide.slide_text.split('\n'):
            text_object.textLine(line)
        pdf.drawText(text_object)

        if slide.image_url:
            try:
                response = requests.get(slide.image_url, timeout=5)
                response.raise_for_status()
                image_data = io.BytesIO(response.content)
                pdf.drawImage(
                    image_data,
                    width - 340,
                    50,
                    width=300,
                    preserveAspectRatio=True,
                    mask='auto'
                )
            except requests.RequestException:
                # Ignore image errors and continue without it
                pass
        pdf.showPage()

    pdf.save()
    buffer.seek(0)
    return buffer

@app.get('/health')
def health_check():
    """Simple health check endpoint."""
    return {'status': 'OK'}

@app.post('/create_presentation')
def create_presentation(data: PresentationRequest):
    """Generate a PDF presentation from the provided data."""
    try:
        buffer = generate_pdf(data)
        headers = {
            'Content-Disposition': f'attachment; filename="{data.title}.pdf"'
        }
        return StreamingResponse(
            buffer,
            media_type='application/pdf',
            headers=headers
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    # Allow the service to be run directly with `python app.py`
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
