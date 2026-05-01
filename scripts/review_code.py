with open("diff.txt", "r", encoding="utf-8") as f:
    diff_text = f.read()

if not diff_text.strip():
    review_text = "No changes found in pull request."
else:
    review_text = "Basic review successful. Diff file was read."

with open("review_output.md", "w", encoding="utf-8") as f:
    f.write(review_text)

print("Basic review script finished.")
