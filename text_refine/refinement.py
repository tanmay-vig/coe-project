import re

INPUT_FILE = "output/extracted_output.txt"
OUTPUT_FILE = "output/refined_output.txt"

def clean_text(text):
    # Remove unwanted characters
    text = re.sub(r"[^A-Za-z0-9\s.,:;!?()\-\+*/=<>%₹$°]", "", text)

    # Replace multiple spaces/newlines
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)

    # Remove repetitive junk
    text = re.sub(r"(.)\1{3,}", r"\1", text)

    # Strip lines and join
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def refine_text_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile:
        raw_text = infile.read()

    refined = clean_text(raw_text)

    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write(refined)

    print(f"✅ Refined text saved to: {output_path}")

if __name__ == "__main__":
    refine_text_file(INPUT_FILE, OUTPUT_FILE)
