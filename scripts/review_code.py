with open("diff.txt", "r", encoding="utf-8") as f:
    diff_text = f.read()

if not diff_text.strip():
    review_text = "No changes found in pull request."
else:

    preview = diff_text[:500].replace("```", "'''")
    review_text = f"""Test review successful.

Summary:
- Diff file was read correctly.
- Diff size: {len(diff_text)} characters.
- Preview of diff (first 500 characters):

{preview}
"""

with open("review_output.md", "w", encoding="utf-8") as f:
    f.write(review_text)

print("Improved review script finished.")
    review_text = "Basic review successful. Diff file was read."

with open("review_output.md", "w", encoding="utf-8") as f:
    f.write(review_text)

print("Basic review script finished.")

