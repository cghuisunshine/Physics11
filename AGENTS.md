# AGENTS.md — Physics11

## Purpose
Maintain the Physics11 website as an accurate, accessible, algebra-based BC Physics 11 course, with optional deeper tutorials and a separate Practice Studio. Read `README.md`, `course-outline.md`, and `course-outline.json` before changing curriculum content.

## Mandatory curriculum boundary: main notes stay strictly Physics 11
**This rule takes priority over requests to add depth to a notes page.**

1. **Keep core notes within Physics 11.** Main notes pages must cover only the concepts, equations, derivations, examples, diagrams, and skills required by the BC Physics 11 curriculum and this project's Physics 11 course outline. Do not import university physics, calculus, statistical mechanics, or other advanced material into the main notes merely because it relates to the topic.
2. **Put additional explanations on separate pages.** Any deeper derivation, extended proof, optional conceptual explanation, advanced application, cross-course connection, or further reading that exceeds the Physics 11 scope belongs in its own standalone, clearly labelled HTML page—not in the core notes. This includes detailed follow-ups requested by a user when the follow-up exceeds Grade 11.
3. **Link, don't duplicate.** If a separate explanation is relevant, add a short contextual link such as “Further reading: Why does this equation work?” in the corresponding notes section. Do not embed the advanced content, long preview, or substantial summary in the notes. Add links only after the destination exists and works.
4. **Keep the learning path independent.** A student must be able to learn and complete the entire Physics 11 topic without following an extension link. Advanced pages must state that they are optional, identify prerequisites, and link back to the corresponding notes.
5. **Apply the boundary to every notes format.** The rule covers Study, Simple, Slides, printable notes, source Markdown, generated HTML, embedded examples, and review pages. Do not hide advanced material in a collapsed panel or alternate notes mode as a workaround.
6. **When in doubt, separate it.** If a proposed explanation's curriculum status is uncertain, keep the concise Grade 11 explanation in the notes and move the additional depth to an optional page. Do not silently broaden the course outline.

### Content placement examples
- **Core notes:** definitions, physical intuition, free-body diagrams, algebraic constant-acceleration derivations, Newton's laws, energy and momentum methods, circuit calculations, and curriculum-aligned worked examples.
- **Separate optional pages:** calculus-based derivations, microscopic statistical mechanics, entropy and the equipartition theorem, general rigid-body rotational dynamics beyond the course outline, advanced field theory, and university-level extensions.
- **Notes-page link:** one short “Further reading” link placed at the relevant concept, without expanding the notes.

## Teaching and mathematical accuracy
- Answer all parts of a question; explain which principle applies and why before substituting numbers.
- Define symbols and units; state assumptions, coordinate axes, sign conventions, system boundaries, and vector directions.
- Show meaningful algebraic steps, not just the final formula. Use diagrams where they clarify the Physics 11 objective.
- Check results using dimensions, conservation laws, limiting cases, or reasonable magnitudes.
- Respect the original source question, graphs, tables, and conditions; do not invent missing data. Flag ambiguous or incorrect source wording.
- Keep core examples algebra-based. A deeper proof may be offered through a separate optional tutorial.
- Clearly distinguish AI-authored worked answers and practice questions from publisher-verified materials.

## Repository editing and builds
- Edit the **source** files, not only generated HTML. Consult `README.md` for the authoritative source/template and build command for each page.
- Course notes generally live under `content/`; shared notes layout is in `tools/vectors-page.html`. Individual builders generate the published notes. Use the page-specific build command documented in `README.md`.
- The course tutorial builder is `python3 tools/build_tutorials.py`. Do not use `--seed-content` casually: it overwrites Markdown edits.
- Physics 11 Practice Studio sources include `tools/physics-practice-template.html` and `tools/physics-*.js`; rebuild with `python3 tools/build_physics_practice.py`.
- Keep existing chapter/question IDs and storage keys stable to preserve saved student progress. Preserve offline functionality, accessibility, printing, diagrams, and navigation.
- For optional extension pages, use the repository's existing styling and navigation conventions where practical. Keep extension files separate from notes source files; link them from the relevant notes and provide a return link.
- Avoid unrelated refactors or modifying generated assets without corresponding source changes.

## Practice Studio and assessment integrity
- Keep textbook questions, AI-generated practice, exam attempts, and follow-up practice distinguishable.
- Preserve exam timing, saved drafts, answer-locking, marking states, exposure records, student profiles, backups, and optional sync.
- Never present AI marking as authenticated teacher marking or readiness as a guaranteed exam prediction.
- Follow the current Exam Mode and Readiness rules documented in `README.md`; update tests if behavior intentionally changes.

## Verification before committing
1. Confirm that every changed core notes section remains within the Physics 11 outline.
2. Confirm that extra derivations and further reading live on **separate pages**, with only short, working links in notes.
3. Rebuild affected generated pages using the documented builders.
4. Run relevant tests (for example `node tools/test_notes_menu.cjs`, `node tools/test_notes_navigation.cjs`, `node tools/test_physics_practice.cjs`, or page-specific tests); report tests not run.
5. Check that Study/Simple/Slides, print mode, links, equations, figures, offline behavior, and student progress still work where applicable.
6. Summarize what changed, which files were touched, and any validation limitations.

**Default decision:** Physics 11 material stays in notes; everything beyond Physics 11 goes on a separate optional page, linked from the notes only when useful.
