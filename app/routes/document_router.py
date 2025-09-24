from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.schemas.document import DocumentRequest, DocumentResponse, SenderRecipientPair, Address
from app.db_services.document import DocumentService
import os

document_router = APIRouter()


@document_router.post("/document/generate", tags=["Document Generation"], response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    """Generate a Word document with sender and recipient information."""
    try:
        filepath = DocumentService.create_sender_recipient_document(request.pairs)
        filename = os.path.basename(filepath)
        
        return DocumentResponse(
            message="Document generated successfully",
            filename=filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating document: {str(e)}")


@document_router.get("/document/download/{filename}", tags=["Document Generation"])
async def download_document(filename: str):
    """Download a generated Word document."""
    import tempfile
    filepath = os.path.join(tempfile.gettempdir(), filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Document not found")
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@document_router.post("/document/generate-from-text", tags=["Document Generation"], response_model=DocumentResponse)
async def generate_document_from_text():
    """Generate a Word document from the predefined text in the problem statement."""
    
    # Parse the predefined text into structured data
    pairs = [
        SenderRecipientPair(
            sender=Address(
                name="CAROLA MODA FEMININA",
                street="RUA ANGELA VARGAS",
                number="77",
                neighborhood="REALENGO",
                city="RIO DE JANEIRO",
                state="RJ",
                postal_code="21755-220"
            ),
            recipient=Address(
                name="Luana Lima Effgen",
                street="Rua : Barberina Girle Cunha",
                number="20",
                neighborhood="Campo Grande",
                city="Cariacica", 
                state="Espírito Santo – ES",
                postal_code="29146206"
            )
        ),
        SenderRecipientPair(
            sender=Address(
                name="CAROLA MODA FEMININA",
                street="RUA ANGELA VARGAS",
                number="77", 
                neighborhood="REALENGO",
                city="RIO DE JANEIRO",
                state="RJ",
                postal_code="21755-220"
            ),
            recipient=Address(
                name="Larissa Alvarenga Schultz",
                street="Rua : Francisco Guimarães",
                number="823",
                neighborhood="Alvorada",
                city="Vila Velha",
                state="Espírito Santo – ES", 
                postal_code="29117175"
            )
        )
    ]
    
    try:
        filepath = DocumentService.create_sender_recipient_document(pairs)
        filename = os.path.basename(filepath)
        
        return DocumentResponse(
            message="Document generated successfully from predefined text",
            filename=filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating document: {str(e)}")