from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_path = "./storage/omni_project"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

generator = pipeline(task="text-generation", model=model, tokenizer=tokenizer, framework="pt")
# gen_text = generator("Why is life?")
# print(gen_text)

def generate_quote(prompt):
    generated_text = generator(prompt)[0]["generated_text"]
    return generated_text