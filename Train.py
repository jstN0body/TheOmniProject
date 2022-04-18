from transformers import AutoTokenizer, LineByLineTextDataset, DataCollatorForLanguageModeling, AutoModelForCausalLM, \
    Trainer, TrainingArguments
import os
import numpy as np

model_name = "./storage/omni_project"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.special_tokens_map["eos_token"]

model = AutoModelForCausalLM.from_pretrained(model_name)

train_path = "./storage/omni_project/dataset.txt"
modified_path = "./storage/omni_project/dataset_fixed.txt"
modified_entries = []
with open(train_path, "r", encoding="utf8") as file:
    for line in file.readlines():
        if not line == "":
            modified_line = tokenizer.special_tokens_map["bos_token"] + line.rstrip() + tokenizer.special_tokens_map["eos_token"]
            modified_entries.append(modified_line)

with open(modified_path, "wb") as modified_dataset:
    modified_entries = np.random.choice(modified_entries, size=1000, replace=False)
    for line in modified_entries:
        modified_dataset.write((line + "\n").encode())

def load_dataset(train_path, tokenizer):
    train_dataset = LineByLineTextDataset(tokenizer=tokenizer, file_path=train_path, block_size=128)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    return train_dataset, data_collator

train_dataset, data_collator = load_dataset(modified_path, tokenizer)

training_args = TrainingArguments(
    output_dir="./storage/omni_project",
    overwrite_output_dir=True,
    num_train_epochs=5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=0,
    logging_steps=500,
    save_steps=500,
    warmup_steps=500
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=train_dataset
)

trainer.train()
trainer.save_model("./storage/omni_project")
tokenizer.save_pretrained("./storage/omni_project")
