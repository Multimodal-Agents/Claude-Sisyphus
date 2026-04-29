# Task: Map Memory Bottlenecks Across the Finetuning Stack

## Goal
Identify every unnecessary memory allocation, copy, and peak usage spike in the unsloth training pipeline. Memory efficiency directly enables larger batch sizes, which directly increases throughput.

## What to analyze

### In unsloth source
- `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/unsloth/models/llama.py` — attention implementation memory patterns
- `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/unsloth/kernels/fast_lora.py` — LoRA intermediate tensor allocations
- `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/unsloth/trainer.py` — gradient accumulation memory behavior
- `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth_zoo/` — gradient checkpointing implementation

### Specific questions to answer
1. Does unsloth's gradient checkpointing implementation recompute the optimal set of activations?
2. Are there intermediate tensors in the LoRA backward pass that could be eliminated?
3. Does the attention implementation avoid materializing the full NxN attention matrix?
4. Are optimizer states stored in the most memory-efficient format?
5. Is there redundant padding in batched inputs?
6. Are there any `.contiguous()` calls creating unnecessary copies?
7. What is the theoretical minimum memory footprint vs actual?

### Compare against
- How DeepSpeed ZeRO handles optimizer state partitioning
- How `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/accelerate/` implements gradient accumulation
- Flash attention's memory complexity vs current attention impl

## Output
Save to `workspace/012_memory_analysis.md`:
- Memory usage map of one full training step
- Every unnecessary allocation found with file:line reference
- Estimated memory savings per fix
- Priority order for implementation
