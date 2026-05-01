with open("diff.txt", "r", encoding="utf-8") as f:
    diff_text = f.read()

if not diff_text.strip():
    review_text = "No changes found in pull request."
else:
    review_text = "Test review successful. Diff file was read correctly."

with open("review_output.md", "w", encoding="utf-8") as f:
    f.write(review_text)

print("Review script finished.")
