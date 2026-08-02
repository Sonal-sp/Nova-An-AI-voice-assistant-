import io
import logging
from typing import List, Dict, Any, Optional
from PIL import Image
import fitz  # PyMuPDF

from services.gemini_service import ask_gemini_vision

logger = logging.getLogger(__name__)


# ==========================================================
# Optical Character Recognition (OCR)
# ==========================================================
def extract_text_ocr(image: Image.Image) -> Dict[str, Any]:
    """
    Extracts text from image using PyTesseract with automatic fallback to Gemini Vision OCR.

    Parameters
    ----------
    image : Image.Image
        Input PIL Image.

    Returns
    -------
    Dict[str, Any]
        Dictionary with 'text', 'engine', and 'success'.
    """
    if image is None:
        return {"text": "", "engine": "None", "success": False}

    # 1. Attempt PyTesseract OCR if installed locally
    try:
        import pytesseract

        ocr_text = pytesseract.image_to_string(image)
        if ocr_text and ocr_text.strip():
            logger.info("Tesseract OCR extracted text successfully.")
            return {
                "text": ocr_text.strip(),
                "engine": "Tesseract OCR",
                "success": True,
            }
    except Exception as e:
        logger.warning(f"PyTesseract unavailable or error ({e}). Using Gemini Vision OCR fallback.")

    # 2. Fallback to Gemini Multimodal Vision OCR
    try:
        prompt = (
            "Perform verbatim Optical Character Recognition (OCR) on this image. "
            "Extract and format all visible text accurately without summary or paraphrase."
        )
        gemini_ocr_text = ask_gemini_vision(image, prompt)
        return {
            "text": gemini_ocr_text.strip(),
            "engine": "Gemini Vision OCR",
            "success": bool(gemini_ocr_text and not gemini_ocr_text.startswith("⚠️")),
        }
    except Exception as e:
        logger.error(f"Gemini Vision OCR failed: {e}")
        return {"text": f"⚠️ OCR Extraction Error: {e}", "engine": "Failed", "success": False}


# ==========================================================
# Multimodal Image Analysis & Explanation
# ==========================================================
def analyze_image_with_vision(
    image: Image.Image,
    prompt: Optional[str] = None,
    analysis_type: str = "general",
) -> str:
    """
    Analyzes an image using Gemini Multimodal Vision API according to analysis mode.

    Parameters
    ----------
    image : Image.Image
        Input PIL Image.
    prompt : Optional[str]
        User specific prompt or question.
    analysis_type : str
        'general' | 'screenshot' | 'diagram' | 'ocr'

    Returns
    -------
    str
        Text analysis response.
    """
    if image is None:
        return "⚠️ No image provided for analysis."

    user_query = prompt.strip() if prompt else ""

    if analysis_type == "screenshot":
        system_instructions = (
            "Examine this application screenshot in detail. Identify the application, "
            "UI components, visible text, active controls, layout structure, and any visible errors or notices."
        )
        final_prompt = f"{system_instructions}\n\nUser Question: {user_query}" if user_query else system_instructions

    elif analysis_type == "diagram":
        system_instructions = (
            "Examine this diagram, chart, or architecture flow in detail. Identify all components, "
            "nodes, direction arrows, data paths, labels, and explain the overall process step-by-step."
        )
        final_prompt = f"{system_instructions}\n\nUser Question: {user_query}" if user_query else system_instructions

    elif analysis_type == "ocr":
        ocr_result = extract_text_ocr(image)
        return f"### 🔤 Extracted Text ({ocr_result['engine']}):\n\n{ocr_result['text']}"

    else:
        final_prompt = user_query if user_query else "Analyze this image in detail and describe key features, objects, and text."

    return ask_gemini_vision(image, final_prompt)


# ==========================================================
# PDF Image Extraction (PyMuPDF)
# ==========================================================
def extract_images_from_pdf(pdf_file) -> List[Dict[str, Any]]:
    """
    Extracts embedded raster images from PDF file using PyMuPDF (fitz).

    Parameters
    ----------
    pdf_file : BytesIO or Streamlit UploadedFile
        PDF file stream.

    Returns
    -------
    List[Dict[str, Any]]
        List of extracted image records containing:
        - page: int
        - index: int
        - image: PIL.Image
        - width: int
        - height: int
        - ext: str
    """
    extracted_images: List[Dict[str, Any]] = []

    try:
        pdf_bytes = pdf_file.read()
        pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        for page_index in range(len(pdf_doc)):
            page = pdf_doc[page_index]
            image_list = page.get_images(full=True)

            for img_idx, img_info in enumerate(image_list):
                xref = img_info[0]
                base_image = pdf_doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                try:
                    pil_image = Image.open(io.BytesIO(image_bytes))
                    width, height = pil_image.size

                    # Filter out tiny icon images (e.g. logos < 50x50)
                    if width >= 50 and height >= 50:
                        extracted_images.append(
                            {
                                "page": page_index + 1,
                                "index": img_idx + 1,
                                "image": pil_image,
                                "width": width,
                                "height": height,
                                "ext": image_ext,
                            }
                        )
                except Exception as img_err:
                    logger.warning(f"Could not parse extracted image xref {xref}: {img_err}")

        pdf_doc.close()
        logger.info(f"Successfully extracted {len(extracted_images)} images from PDF.")
        return extracted_images

    except Exception as e:
        logger.error(f"Error extracting images from PDF: {e}")
        return []
