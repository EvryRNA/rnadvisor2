from typing import Any

import streamlit as st

from src_st.utils.utils import viz_structure
import os

MAX_FILE_SIZE = 3 * 1024 * 1024


def get_upload(current_upload: Any, is_native: bool = True, session_number: int = 77):
    try:
        if os.path.exists(current_upload):
            return current_upload
    except TypeError:
        pass
    if current_upload is not None:
        if current_upload.size > MAX_FILE_SIZE:
            st.error(
                "The uploaded file is too large. Please upload a file smaller than 5MB."
            )
        else:
            current_path = viz_structure(
                upload=current_upload,
                is_native=is_native,
                session_number=session_number,
            )
        return current_path


def get_multiple_uploads(current_upload, session_number: int):
    if current_upload is not None:
        return [
            get_upload(upload, is_native=False, session_number=session_number)
            for upload in current_upload
        ]
