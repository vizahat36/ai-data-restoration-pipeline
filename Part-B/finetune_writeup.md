# Finetuning Writeup

## Model Choice

For this assignment I selected **Qwen2.5-0.5B-Instruct**, a lightweight instruction-tuned language model with approximately 0.5 billion parameters.

This model was chosen because:
- It fits comfortably within the **16GB VRAM constraint of Google Colab T4 GPUs**
- It supports **instruction-style chat interactions**
- It provides a good balance between capability and training efficiency for small-scale finetuning tasks.

---

## LoRA Configuration

The model was finetuned using **LoRA (Low-Rank Adaptation)** via the HuggingFace PEFT library.

Configuration used:

- Rank (`r`) = 16  
- Alpha (`lora_alpha`) = 32  
- Dropout (`lora_dropout`) = 0.05  
- Target modules = `q_proj`, `v_proj`

These parameters were chosen because they provide a good trade-off between:
- adaptation capacity
- training stability
- low GPU memory usage.

Only a small fraction of the model parameters (~0.3%) were trained, allowing efficient finetuning on the Colab T4 GPU.

---

## Training Setup

The cleaned dataset generated in **Part A** was converted into instruction-style chat format and used as training data.

Training configuration:

- Training examples: ~55
- Epochs: 1
- Batch size: 2
- Gradient accumulation: 2
- Learning rate: 2e-4

Although the dataset is small, it is sufficient to demonstrate a working finetuning pipeline.

---

## What Went Well

The complete finetuning pipeline successfully ran end-to-end on Google Colab.

Key achievements include:
- successful loading of the base model
- correct formatting of conversational training data
- LoRA adapter training
- inference generation
- evaluation script producing a pass/fail scorecard.

---

## Limitations

The primary limitation of the current model is the **small dataset size** (~55 training samples).

Because of this:
- the model sometimes produces inconsistent Hinglish responses
- the behavior adaptation is relatively weak.

---

## Future Improvements

If more time and compute resources were available, the following improvements would be prioritized:

1. Expand the dataset to **several thousand real customer support conversations**.
2. Train for **multiple epochs** to allow stronger behavioral adaptation.
3. Improve Hinglish language consistency by filtering and normalizing training data.
4. Implement better evaluation metrics such as semantic similarity and intent detection.