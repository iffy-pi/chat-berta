from datasets import load_dataset_builder, load_dataset
ds_builder = load_dataset_builder("samsum")

# Inspect dataset description
print(ds_builder.info.description)
dataset = load_dataset("samsum", split="train")
# Inspect dataset features

print(dataset[5])