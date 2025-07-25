import fitz  # PyMuPDF
import openai
import argparse
import tiktoken
import time

# --- Config ---
CHUNK_TOKEN_LIMIT = 3000
PAUSE_SECONDS = 1  # wait between API calls to avoid rate limits

# --- Token counter ---
def num_tokens_from_string(string: str, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(string))

# --- Extract PDF text ---
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n\n".join([page.get_text() for page in doc])

# --- Chunk text safely ---
def chunk_text(text, token_limit):
    words = text.split()
    chunks = []
    chunk = []

    token_count = 0
    for word in words:
        token_count += num_tokens_from_string(word)
        chunk.append(word)
        if token_count >= token_limit:
            chunks.append(" ".join(chunk))
            chunk = []
            token_count = 0

    if chunk:
        chunks.append(" ".join(chunk))
    return chunks

# --- Build GPT prompt ---
def build_prompt(text_chunk):
    return f"""
You are an expert in life cycle inventory modeling.

Given the text below, extract any inventory flows related to the production of 1 metric ton of PHA.

For each, return:
- "flow": name of the input or output
- "amount": numeric value (if given)
- "unit": unit (e.g., kg, kWh, ton)
- "process_step": if a process phase is mentioned (e.g., Fermentation)
- "assumption": table number, scenario, or other note

Skip impact categories or general environmental indicators.

Text:
{text_chunk}
"""

# --- Main function ---
def main(pdf_path, api_key):
    openai.api_key = api_key

    full_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(full_text, CHUNK_TOKEN_LIMIT)

    all_results = []

    for i, chunk in enumerate(chunks):
        print(f"\n⏳ Processing chunk {i+1}/{len(chunks)}...\n")

        prompt = build_prompt(chunk)

        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            result = response.choices[0].message.content
            print(result)
            all_results.append(result)

            time.sleep(PAUSE_SECONDS)

        except Exception as e:
            print(f"❌ Error in chunk {i+1}: {e}")

    print("\n✅ All chunks processed.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract LCI flows from a scholarly PDF using GPT-4")
    parser.add_argument("--pdf", required=True, help="Path to the PDF file")
    parser.add_argument("--apikey", required=True, help="Your OpenAI API key")
    args = parser.parse_args()

    main(args.pdf, args.apikey)
