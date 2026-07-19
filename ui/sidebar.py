import streamlit as st

from services.memory import clear_messages
from services.document_service import (
    create_document,
    get_document_statistics,
)

from utils.helpers import chat_to_text
from utils.loading import loading

from utils.constants import (
    PDF_LOADING_MESSAGE,
    TEXT_ONLY,
    TEXT_AND_VOICE,
    VOICE_ONLY,
)


# ==========================================================
# Sidebar
# ==========================================================
def show_sidebar():

    with st.sidebar:

        # ==================================================
        # Header
        # ==================================================
        st.title("🤖 Nova")
        st.caption("Your Personal AI Assistant")

        st.divider()

        # ==================================================
        # Response Mode
        # ==================================================
        response_mode = st.radio(
            "🔊 Response Mode",
            [
                TEXT_ONLY,
                VOICE_ONLY,
                TEXT_AND_VOICE,
            ],
        )

        st.divider()

        # ==================================================
        # Initialize Document Library
        # ==================================================
        if "documents" not in st.session_state:

            st.session_state.documents = []

        # ==================================================
        # Multi PDF Upload
        # ==================================================
        uploaded_files = st.file_uploader(
            "📄 Upload PDFs",
            type=["pdf"],
            accept_multiple_files=True,
        )

        if uploaded_files:

            existing_files = {

                doc["filename"]

                for doc in st.session_state.documents

            }

            for file in uploaded_files:

                # Avoid duplicates
                if file.name in existing_files:

                    continue

                with loading(
                    f"{PDF_LOADING_MESSAGE} ({file.name})"
                ):

                    document = create_document(file)

                    st.session_state.documents.append(
                        document
                    )

        st.divider()

        # ==================================================
        # Uploaded Documents
        # ==================================================
        st.subheader("📂 Uploaded Documents")

        documents = st.session_state.documents

        if documents:

            for index, document in enumerate(documents):

                with st.expander(
                    f"📄 {document['filename']}",
                    expanded=False,
                ):

                    st.write(
                        f"Pages : {document['pages']}"
                    )

                    st.write(
                        f"Chunks : {document['chunk_count']}"
                    )

                    if st.button(
                        "🗑 Remove",
                        key=f"remove_doc_{index}",
                        use_container_width=True,
                    ):

                        st.session_state.documents.pop(index)

                        st.rerun()

        else:

            st.info("No PDF uploaded.")

        st.divider()

        # ==================================================
        # Document Statistics
        # ==================================================
        st.subheader("📊 Documents")

        stats = get_document_statistics(
            documents
        )

        st.write(f"Files : {stats['files']}")
        st.write(f"Pages : {stats['pages']}")
        st.write(f"Chunks : {stats['chunks']}")

        st.divider()

        # ==================================================
        # Session Statistics
        # ==================================================
        st.subheader("💬 Session")

        st.write(
            f"Messages : {len(st.session_state.get('messages', []))}"
        )

        st.write(
            f"Voice Mode : {response_mode}"
        )

        st.divider()

        # ==================================================
        # Export Chat
        # ==================================================
        chat_text = chat_to_text(
            st.session_state.get(
                "messages",
                [],
            )
        )

        st.download_button(
            "📥 Export Chat",
            chat_text,
            file_name="nova_chat.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.divider()

        # ==================================================
        # Clear Chat
        # ==================================================
        if st.button(
            "🗑 Clear Chat",
            use_container_width=True,
        ):

            clear_messages()

            st.rerun()

    return response_mode