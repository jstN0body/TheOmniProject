from transformers import AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline

model_path = "./storage/omni_project"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

generator = TextGenerationPipeline(task="text-generation", tokenizer=tokenizer, model=model, framework="pt")

kwargs = {
    "repetition_penalty" : 1.15,
    "length_penalty" : 0.35,
    "max_length" : 25
}

def generate_quote():
    generated_text = generator("", kwargs=kwargs)[0]["generated_text"]
    for i in range(0, len(generated_text)):
        position = len(generated_text) - i -1
        char = generated_text[position]
        if char == "." or char == "?" or char == "!":
            generated_text = generated_text[0:position+1]
            break
    return generated_text

text = generate_quote()
print(text)
