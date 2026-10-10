# Physics 11 tutorials

Open [index.html](index.html) in a browser. No installation, server, account, or internet connection is required for the tutorials. The original PDF must remain in this directory for textbook links to work. Online curriculum links require internet access.

The standalone [BC Science Chapter 2 Kinematics question collection](bc-kinematics-questions.html) contains 101 entries across 26 sets: warm-ups, quick checks, practice problems, section and chapter reviews, extra practice, sample-problem prompts, and investigation questions. Original equations, graphs, and tables are embedded as question crops. Every entry has an independently calculated worked answer behind its own **Show answer / Hide answer** button; investigation answers explain how to use measured data. Search, section/type filters, completion marks, and printing work offline. Printing includes answers currently revealed. This HTML file needs no companion files. Its extraction inventory is in `content/bc-kinematics-questions.json`, and editable answers are in `tools/bc_kinematics_answers.py`; rebuild it with `tools/build_bc_kinematics_questions.py` using Python with Pillow and Poppler on PATH.

The course contains eight unit pages with 49 lessons, 49 worked examples, 98 practice questions with solutions, 24 multiple-choice checkpoint items, eight adjustable diagrams, and eight mixed review problems. The course companion contains a formula sheet with model conditions and symbol definitions.

The home page also includes a searchable textbook problem bank: **1,631 numbered problems across 16 course-related chapters**, with **125 original problem pages**. Filter by course unit, search words or a chapter/problem identifier such as `4.23`, and select a number to view the original question. Equations, tables, figures, and continuation pages are preserved in local lossless images. Keep `assets/textbook-problems/` beside `index.html` for the inline viewer to work offline.

The bank includes the complete end-of-chapter problem sets for chapters 1–8, 12, 15–18, 24, 26, and 27. Module headings distinguish direct lesson references from extension topics; additional mixed sets can contain both. Some source exercises require calculus or physics beyond the main Grade 11 lessons. This bank contains textbook questions; the 98 tutorial practice questions and their solutions remain separate.

- **Study mode:** all lessons; practice solutions start collapsed.
- **Simple mode:** all lessons and answers, without the sidebar.
- **Slides mode:** one lesson at a time; use previous/next or the left/right arrow keys. Each lesson can scroll vertically.
- **Print / Save PDF:** opens browser printing and includes practice solutions.
- **Progress:** lesson completion is saved locally when browser storage is available. It does not sync across devices; file-URL storage behavior can vary by browser.

## Sources

The two URLs in `resource.txt` supply the course organization and curriculum scope. The supplied PDF is *Halliday & Resnick Fundamentals of Physics*, 10th edition, Extended, Jearl Walker. The pages adapt relevant textbook ideas for an algebra-based Grade 11 course, with newly authored examples. Each lesson provides a textbook section opening, PDF viewer page, and printed page. For the referenced body chapters, printed page = PDF page - 36.

The main sequence intentionally omits calculus requirements and unrelated advanced textbook chapters. Qualitative refraction/diffraction and simple-machine terminology are curriculum bridge material. The inquiry tasks include measurement, uncertainty, model evaluation, practical application, and respectful community research; these pages do not prescribe local cultural knowledge or replace teacher guidance.

## Edit and rebuild

The editable lesson notes are in `content/`. Course outline files are `course-outline.md` and `course-outline.json`.

Run `python3 tools/build_tutorials.py` to rebuild HTML while preserving edits to the Markdown notes. This uses the installed `chapter-tutorial-html` generator at the path recorded near the top of the build script. Update that path if you move this project to a different machine.

`tools/course_content.py` holds the original authored content and lesson metadata. `python3 tools/build_tutorials.py --seed-content` regenerates the Markdown from that content and **overwrites Markdown edits**. If adding, removing, or reordering lessons, update the metadata in this file before reseeding; the rendering and source links use that metadata. Styling and interactions live in `tools/page.css` and `tools/page.js` and are embedded in each generated HTML file.

`content/textbook-problems.json` records every problem number, module, original page, starting location, continuation pages, and search text. The source PDF's math font does not extract reliably, so this text is used for search while the page images supply the readable mathematical content. The normal tutorial build includes this problem bank automatically.

To regenerate the textbook index and missing page images, run `python3 tools/build_textbook_problems.py --extract --render` in an environment with pypdf, Pillow, and Poppler's `pdftotext` and `pdftoppm`, then rebuild the tutorials. Chapter page ranges live in that script. Page images load only when opened; the home page does not download the entire bank on startup.

For an optional local server: `python3 -m http.server 8000`, then visit `http://localhost:8000/`. Browser printing can produce a PDF copy; no pre-generated PDF output is included.
# Physics11
