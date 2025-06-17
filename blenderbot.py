# chatbot_pipeline.py

from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import nltk
import string

# Load name dataset
nltk.download('names')
from nltk.corpus import names
all_names = set(names.words())  # use set for faster lookup

# Load your fine-tuned BlenderBot model
model_path = r"C:\Users\ORIGINAL SHOP\Downloads\fine tuning blenderbot\valid"
tokenizer = BlenderbotTokenizer.from_pretrained(model_path)
model = BlenderbotForConditionalGeneration.from_pretrained(model_path)


def chat_with_bot(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    output_ids = model.generate(**inputs, max_length=100, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response


def personalize_response(user_input):
    import string

    
    prompt_tokens = user_input.split()
    name = None

    
    all_names_lower = {n.lower(): n for n in all_names}  # lowercase → original

    # Detect and replace the first recognized name with <name_person>
    for i, token in enumerate(prompt_tokens):
        token_clean = token.strip(string.punctuation).lower()
        if token_clean in all_names_lower:
            name = all_names_lower[token_clean]  # original-cased name
            prompt_tokens[i] = "<name_person>"
            break

    masked_input = " ".join(prompt_tokens)
    bot_output = chat_with_bot(masked_input)

    if "<name_person>" in bot_output:
        if name:
            bot_output = bot_output.replace("<name_person>", name)
        else:
            bot_output = bot_output.replace("<name_person>", "")

    return bot_output.strip()






