import fitz

doc = fitz.open("manual.pdf")

all_text = ""
for page in doc:
    all_text += page.get_text()

with open("manual_text.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("Done!")
print("First 300 characters:")
print(all_text[:300])