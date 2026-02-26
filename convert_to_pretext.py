import pathlib
import re

# Folder that contains the Markdown files
md_dir = pathlib.Path("md")

# Output file
out_path = pathlib.Path("statistics-done-wrong.ptx")

out_lines = []

# PreTeXt wrapper + book front matter (minimal, you can edit later)
out_lines.append('<pretext xml:lang="en">')
out_lines.append('  <book xml:id="statistics-done-wrong">')
out_lines.append('    <title>Statistics Done Wrong</title>')
out_lines.append('    <author>')
out_lines.append('      <personname>')
out_lines.append('        <firstname>Alex</firstname>')
out_lines.append('        <surname>Reinhart</surname>')
out_lines.append('      </personname>')
out_lines.append('    </author>')
out_lines.append('')
out_lines.append('    <chapter xml:id="ch-statistics-done-wrong">')
out_lines.append('      <title>Statistics Done Wrong (Online Edition)</title>')
out_lines.append('      <p>Adapted from the online version of <c>Statistics Done Wrong</c> by Alex Reinhart, licensed under CC-BY 4.0. Original available at <url href="https://www.statisticsdonewrong.com/">https://www.statisticsdonewrong.com/</url>.</p>')
out_lines.append('')

# Go through all md files in alphabetical order
for md_file in sorted(md_dir.glob("*.md")):
    text = md_file.read_text(encoding="utf-8")

    # Split into lines
    lines = text.splitlines()

    # Skip empty files
    if not lines:
        continue

    # Take first line as title if it's a Markdown H1 (# Title)
    first = lines[0].strip()
    if first.startswith("# "):
        title = first[2:].strip()
        body_lines = lines[1:]
    else:
        # Fallback: use filename as title
        title = md_file.stem
        body_lines = lines

    body = "\n".join(body_lines)

    # --- Very naive inline formatting conversions ---

    # Bold or italic: **text** or *text* -> <em>text</em>
    # (You can refine later for <em> vs <strong>)
    body = re.sub(r'\*\*(.+?)\*\*', r'<em>\1</em>', body)
    body = re.sub(r'\*(.+?)\*', r'<em>\1</em>', body)

    # Inline code `code` -> <c>code</c>
    body = re.sub(r'`(.+?)`', r'<c>\1</c>', body)

    # Convert Markdown H2 headings "## Heading" into a simple <p><em>Heading</em></p>
    # (You can later upgrade these to <subsection> etc.)
    body = re.sub(r'^## +(.+)$', r'<p><em>\1</em></p>', body, flags=re.MULTILINE)

    # Split on blank lines to make paragraphs
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]

    # Wrap each paragraph in <p>...</p> if it isn't already tagged
    xml_paras = []
    for p in paragraphs:
        if p.startswith("<p>") and p.endswith("</p>"):
            xml_paras.append(p)
        else:
            xml_paras.append(f"<p>{p}</p>")

    body_xml = "\n        ".join(xml_paras)

    section_id = f"sec-{md_file.stem}"

    out_lines.append(f'      <section xml:id="{section_id}">')
    out_lines.append(f'        <title>{title}</title>')
    out_lines.append(f'        {body_xml}')
    out_lines.append('      </section>')
    out_lines.append('')

# Close chapter and book and pretext
out_lines.append('    </chapter>')
out_lines.append('  </book>')
out_lines.append('</pretext>')

out_path.write_text("\n".join(out_lines), encoding="utf-8")
print(f"Wrote {out_path}")