with open("diff.txt", "r", encoding="utf-8") as f:
    diff_text = f.read()

if not diff_text.strip():
    review_text = "No changes found in pull request."
else:
    review_text = f"""Test review successful.

Summary:
- Diff file was read correctly.
- Diff size: {len(diff_text)} characters.
- This is the improved review script in test-branch.
"""

with open("review_output.md", "w", encoding="utf-8") as f:
    f.write(review_text)

print("Improved review script finished.")
