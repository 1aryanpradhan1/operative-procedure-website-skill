"""Extract supplied PDF text by page; does not crop figures or validate reading order."""
import argparse, json, shutil
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('workdir', type=Path)
    args = parser.parse_args()
    from pypdf import PdfReader
    reader = PdfReader(args.pdf)
    pages = [{'page': i + 1, 'text': page.extract_text() or ''}
             for i, page in enumerate(reader.pages)]
    if not pages:
        raise ValueError('PDF has no pages')
    args.workdir.mkdir(parents=True, exist_ok=True)
    (args.workdir / 'article.json').write_text(json.dumps(pages, ensure_ascii=False, indent=2))
    destination = args.workdir / 'source.pdf'
    if args.pdf.resolve() != destination.resolve():
        shutil.copyfile(args.pdf, destination)
    blank = [p['page'] for p in pages if not p['text'].strip()]
    print(f'Extracted {len(pages)} pages; visually verify reading order and source figures.')
    if blank:
        print(f'Pages without extracted text (may require OCR): {blank}')

if __name__ == '__main__':
    main()
