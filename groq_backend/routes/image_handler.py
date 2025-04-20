from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.vision import describe_image
from utils.groq_llm import query_groq
from io import BytesIO

router = APIRouter()

@router.post("/image")
async def handle_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image_bytes = BytesIO(contents)

        print("Image received:", file.filename)

        description = describe_image(image_bytes)
        print("Image Description:", description)

        response = query_groq(
    f"This image was detected as: '{description}'. Based on this, describe what might be happening or its possible meaning."
)

        print("LLM Response:", response)

        return {
            "filename": file.filename,
            "description": description,
            "llm_response": response
        }

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
