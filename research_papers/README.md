# Research Papers Drop Zone

Drop PDF or markdown files of papers here before running the queue.

Sisyphus will read everything in this folder during the analysis phase and extract techniques applicable to optimizing the unsloth finetuning stack.

## What to drop here

Good candidates:
- Attention mechanism improvements (Flash Attention, ring attention, etc.)
- Quantization research (FP8, INT4, mixed precision)
- Kernel fusion techniques
- Memory-efficient training methods
- LoRA / PEFT variations and improvements
- Gradient checkpointing innovations
- Optimizer improvements (Adam variants, GaLore, etc.)
- Triton / CUDA kernel optimization techniques
- Data loading and pipeline improvements

## Format

- PDFs from arxiv are fine
- Markdown summaries work too
- Name files descriptively: `flash_attention_3_arxiv2024.pdf`, `galore_optimizer.pdf`

Sisyphus will process all files here in task 020_read_research_papers.
