"""This module contains the main process of the robot."""

import re
from pathlib import Path

import pytesseract
from pypdf import PdfReader
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection


# Matches names like "7163bef7-2fe7-4efe-b35e-6a449ba92a61_pades.pdf"
FILE_NAME_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}_pades\.pdf$",
    re.IGNORECASE
)


def process(orchestrator_connection: OrchestratorConnection) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")

    folder = orchestrator_connection.process_arguments

    for path in Path(folder).iterdir():
        if not FILE_NAME_PATTERN.match(path.name):
            continue

        case_number = extract_case_number(path)

        if not case_number:
            orchestrator_connection.log_error(f"Could not read case number from {path.name}. Skipping.")
            continue

        new_path = get_available_path(path.parent, case_number, ".pdf")
        path.rename(new_path)
        orchestrator_connection.log_info(f"Renamed {path.name} to {new_path.name}")


def extract_case_number(path: Path) -> str:
    """Read the case number from the first page of the PDF using OCR.

    Returns:
        The case number with any characters not allowed in file names removed.
    """
    reader = PdfReader(path)
    image = reader.pages[0].images[0].image

    crop_box = (800, 205, 1000, 240)
    image = image.crop(crop_box)
    text = pytesseract.image_to_string(image, lang="eng", config="--psm 3")

    return re.sub(r'[<>:"/\\|?*]', "", text).strip()


def get_available_path(folder: Path, name: str, extension: str) -> Path:
    """Get a path in the folder that doesn't already exist.
    If the name is taken a number is appended, e.g. "name (2).pdf".
    """
    path = folder / f"{name}{extension}"
    i = 2
    while path.exists():
        path = folder / f"{name} ({i}){extension}"
        i += 1
    return path


if __name__ == '__main__':
    import os
    import uuid
    conn_string = os.getenv("OpenOrchestratorConnString")
    crypto_key = os.getenv("OpenOrchestratorKey")
    oc = OrchestratorConnection("Omdøber test", conn_string, crypto_key, '', "trigger_id", uuid.uuid4())
    process(oc)