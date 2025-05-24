from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pdf2image import convert_from_bytes
from io import BytesIO
from zipfile import ZipFile
import base64

app = FastAPI()

@app.post("/convert/")
async def convert(pdf: UploadFile = File(...)):
    if pdf.content_type != "application/pdf":
        raise HTTPException(400, "Sólo PDF permitido")
    data = await pdf.read()
    try:
        pages = convert_from_bytes(data, dpi=200)
    except Exception as e:
        raise HTTPException(500, f"Error conversión: {e}")

    # Empaqueta en ZIP
    buf = BytesIO()
    with ZipFile(buf, "w") as z:
        for i, img in enumerate(pages, start=1):
            name = f"{pdf.filename.rsplit('.',1)[0]} - Pag{i:03d}.jpeg"
            img_buf = BytesIO()
            img.save(img_buf, "JPEG")
            z.writestr(name, img_buf.getvalue())
    buf.seek(0)

    return StreamingResponse(buf, media_type="application/zip",
                             headers={"Content-Disposition":"attachment; filename=images.zip"})


@app.post("/convert_json/")
async def convert_json(pdf: UploadFile = File(...)):
    if pdf.content_type != "application/pdf":
        raise HTTPException(400, "Sólo PDF permitido")
    data = await pdf.read()
    try:
        pages = convert_from_bytes(data, dpi=200)
    except Exception as e:
        raise HTTPException(500, f"Error conversión: {e}")

    result = []
    for i, img in enumerate(pages, start=1):
        buf = BytesIO()
        img.save(buf, "JPEG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        name = f"{pdf.filename.rsplit('.',1)[0]} - Pag{i:03d}.jpeg"
        result.append({"name": name, "data": b64})
    return {"pages": result}
