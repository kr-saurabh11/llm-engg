from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

text = "Hi my name is Saurabh and I like video games"

# Tokenize the text
tokens = tokenizer.encode(text)

print(f"Text: {text}\n")
print(f"Tokens: {tokens}")
print(f"Number of tokens: {len(tokens)}\n")

print("Token breakdown:")
print("-" * 50)
for token_id in tokens:
    token_text = tokenizer.decode([token_id])
    print(f"ID: {token_id:5d} | Text: {repr(token_text)}")

# Reconstruct text from tokens to verify
print("\n" + "-" * 50)
reconstructed = tokenizer.decode(tokens)
print(f"Reconstructed text: {reconstructed}")
