from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_path = r"C:\Users\ORIGINAL SHOP\Desktop\implimen_bot\omarBot\omarBot\dialogpt_finetuning"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def chat_with_model(prompt, model, tokenizer, max_length=100):
    # Encode the prompt properly (adds batch dim)
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Generate response
    outputs = model.generate(
        inputs.input_ids,
        max_length=max_length,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        eos_token_id=tokenizer.eos_token_id,
        # early_stopping=True,  # optional
    )

    # Remove the prompt tokens from the output
    generated_tokens = outputs[0][inputs.input_ids.shape[-1]:]

    # Decode generated tokens
    response = tokenizer.decode(generated_tokens, skip_special_tokens=True)
    return response


def generative_answer(prompt):
    # Add speaker tags as your model was probably trained with these
    prompt = f"user: {prompt}"
    response = chat_with_model(prompt, model, tokenizer)
    
    # Clean up the output (adjust based on your training data special tokens)
    for token in ["<end>", "bot:", "user:", "<", ">"]:
        response = response.replace(token, "")
    response = response.strip()
    return response


'''questions = [
    "How are you doing today?",
    "Do you have any hobbies or interests?",
    "What’s your favorite kind of music?",
    "Are you married or in a relationship?",
    "How do you usually spend your weekends?",
    "What is the capital city of Japan?",
    "When was the first moon landing?",
    "Who invented the telephone?",
    "What’s the speed of light in km/s?",
    "How many countries are there in Africa?"
]

for q in questions:
    answer = generative_answer(q)
    print(f"Question: {q}")
    print(f"Answer: {answer}")
    print("-" * 50)
'''