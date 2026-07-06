from app.database import vector_store
from pypdf import PdfReader
from pathlib import Path

data_dir = Path(__file__).resolve().parent.parent / "data"
pdf_files = [f for f in data_dir.iterdir() if f.suffix.lower() == ".pdf"]

for pdf_path in pdf_files:
    book_title = pdf_path.stem
    print(f"Ingesting: {book_title}")

    reader = PdfReader(str(pdf_path))

    # Extract paragraphs with their source page
    paragraphs_with_pages = []
    for page_num, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        paras = [p.strip() for p in text.split("\n\n") if p.strip()]
        paragraphs_with_pages.extend([(para, page_num) for para in paras])

    # chunking by paragraphs, each chunk ~200 tokens
    chunks = []
    current = []
    current_words = 0
    current_pages = []  # track pages of paragraphs in the current chunk

    for para, page_num in paragraphs_with_pages:
        n_words = len(para.split())
        # if this single paragraph is huge, split it forcibly
        if n_words > 200:
            words = para.split()
            for i in range(0, len(words), 200):
                chunk = " ".join(words[i : i + 200])
                chunks.append({"text": chunk, "page": page_num})
            continue

        # if accumulating exceeds ~200 tokens, close the current chunk
        if current_words + n_words > 150:
            if current:
                # use the page of the first paragraph in the chunk
                chunk_text = " ".join(current)
                chunk_page = current_pages[0]
                chunks.append({"text": chunk_text, "page": chunk_page})
            current = []
            current_words = 0
            current_pages = []

        current.append(para)
        current_words += n_words
        current_pages.append(page_num)

    if current:
        chunk_text = " ".join(current)
        chunk_page = current_pages[0]
        chunks.append({"text": chunk_text, "page": chunk_page})

    print(f"  {len(chunks)} chunks generated")
    vector_store.store.add_documents(book_title, chunks)

print("Ingestion complete.")
