"""
Generates a valid text-based sample PDF file for CampusSaathi AI using pure Python.
Requires NO third-party libraries (zero dependencies).
"""

import os


def create_minimal_pdf(filename: str, title: str, pages_content: list):
    """
    Creates a simple, standard-compliant PDF 1.4 file containing selectable text.
    """
    # PDF objects
    objects = []

    def add_object(content_bytes):
        obj_num = len(objects) + 1
        objects.append(content_bytes)
        return obj_num

    # Obj 1: Catalog
    # Obj 2: Pages root
    # Subsequent: Page objects & Content streams
    # Font object

    font_obj_num = 3

    page_obj_nums = []
    content_obj_nums = []

    # Calculate object numbers
    # 1: Catalog, 2: Pages, 3: Font
    next_num = 4
    for _ in pages_content:
        page_obj_nums.append(next_num)
        content_obj_nums.append(next_num + 1)
        next_num += 2

    # Object 1: Catalog
    catalog_bytes = f"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n".encode(
        "latin1"
    )

    # Object 2: Pages
    kids_str = " ".join([f"{num} 0 R" for num in page_obj_nums])
    pages_root_bytes = f"2 0 obj\n<< /Type /Pages /Kids [{kids_str}] /Count {len(pages_content)} >>\nendobj\n".encode(
        "latin1"
    )

    # Object 3: Font
    font_bytes = f"3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n".encode(
        "latin1"
    )

    objects_data = [catalog_bytes, pages_root_bytes, font_bytes]

    # Generate Page and Content Objects
    for i, content_lines in enumerate(pages_content):
        # Format text stream
        stream_parts = ["BT", "/F1 12 Tf", "50 750 Td", "16 TL"]

        # Title on first page
        if i == 0:
            stream_parts.extend(
                [
                    f"/F1 18 Tf",
                    f"({title}) Tj",
                    "T*",
                    "/F1 11 Tf",
                    "(Department of Computer Science & Engineering - Semester 4) Tj",
                    "T*",
                    "T*",
                ]
            )

        for line in content_lines:
            safe_line = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            stream_parts.append(f"({safe_line}) Tj")
            stream_parts.append("T*")

        stream_parts.append("ET")
        stream_content = "\n".join(stream_parts).encode("latin1")

        content_num = content_obj_nums[i]
        page_num = page_obj_nums[i]

        content_obj = (
            f"{content_num} 0 obj\n"
            f"<< /Length {len(stream_content)} >>\n"
            f"stream\n".encode("latin1")
            + stream_content
            + f"\nendstream\nendobj\n".encode("latin1")
        )

        page_obj = (
            f"{page_num} 0 obj\n"
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Contents {content_num} 0 R /Resources << /Font << /F1 3 0 R >> >> >>\n"
            f"endobj\n".encode("latin1")
        )

        objects_data.append(page_obj)
        objects_data.append(content_obj)

    # Build final PDF binary with xref table
    pdf_output = bytearray(b"%PDF-1.4\n")
    offsets = []

    for obj in objects_data:
        offsets.append(len(pdf_output))
        pdf_output.extend(obj)

    xref_offset = len(pdf_output)
    pdf_output.extend(b"xref\n")
    pdf_output.extend(f"0 {len(objects_data) + 1}\n".encode("latin1"))
    pdf_output.extend(b"0000000000 65535 f \n")

    for offset in offsets:
        pdf_output.extend(f"{offset:010d} 00000 n \n".encode("latin1"))

    pdf_output.extend(b"trailer\n")
    pdf_output.extend(
        f"<< /Size {len(objects_data) + 1} /Root 1 0 R >>\n".encode("latin1")
    )
    pdf_output.extend(b"startxref\n")
    pdf_output.extend(f"{xref_offset}\n%%EOF\n".encode("latin1"))

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        f.write(pdf_output)

    print(f"Sample PDF successfully created: {filename}")


if __name__ == "__main__":
    sample_pages = [
        [
            "UNIT 1: DATA STRUCTURES AND ALGORITHM ANALYSIS",
            "----------------------------------------------------------------------",
            "1. Asymptotic Notations:",
            "   - Big-O (O): Represents the upper bound of algorithm runtime (Worst Case).",
            "   - Omega: Represents the lower bound of runtime (Best Case).",
            "   - Theta: Represents the tight bound where upper and lower bounds meet.",
            "",
            "2. Binary Search Trees (BST):",
            "   - A binary tree where the left subtree contains keys smaller than the node.",
            "   - The right subtree contains keys strictly greater than the root node.",
            "   - Search, insertion, and deletion complexity: O(h) where h is tree height.",
            "   - In a balanced BST (AVL or Red-Black), h = O(log n).",
            "   - In a degenerate BST, worst-case complexity degrades to O(n).",
            "",
            "3. Common College Exam Questions:",
            "   - Question: Differentiate between Stack (LIFO) and Queue (FIFO).",
            "   - Question: Explain In-order, Pre-order, and Post-order tree traversals.",
        ],
        [
            "UNIT 2: DATABASE MANAGEMENT SYSTEMS (DBMS)",
            "----------------------------------------------------------------------",
            "1. ACID Properties in Transaction Processing:",
            "   - Atomicity: All operations succeed or none are applied (All-or-Nothing).",
            "   - Consistency: Database moves from one valid state to another valid state.",
            "   - Isolation: Concurrent transactions do not interfere with each other.",
            "   - Durability: Committed changes survive power loss or system crash.",
            "",
            "2. Database Normalization:",
            "   - 1NF: Eliminates repeating groups; ensures atomic/indivisible values.",
            "   - 2NF: In 1NF and removes partial functional dependencies on candidate keys.",
            "   - 3NF: In 2NF and removes transitive functional dependencies (X -> Y -> Z).",
            "   - BCNF: Stricter version of 3NF; for every X -> Y, X must be a super key.",
            "",
            "3. Important Exam Formula:",
            "   - Candidate Keys formula: Minimal super key with uniqueness property.",
        ],
    ]

    create_minimal_pdf(
        filename="sample_notes/Sample_College_Notes.pdf",
        title="CampusSaathi AI - Sample College Notes",
        pages_content=sample_pages,
    )
