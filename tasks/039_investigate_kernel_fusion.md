# Task: Find Kernel Fusion Opportunities

## Goal
Every time we cross a kernel boundary, we pay memory bandwidth costs reading and writing tensors. Fusing adjacent kernels into one can dramatically reduce this overhead.

## What to do
1. Map the exact sequence of kernel calls for one forward + backward pass through a single transformer layer in unsloth
2. Identify every pair of adjacent kernels where the output of one is immediately consumed by the next
3. For each pair: estimate the memory bandwidth wasted on the intermediate tensor
4. Identify which fusions are feasible with triton
5. Prioritize by estimated speedup

## Known fusion candidates to investigate
- **RMSNorm + QKV projection**: Can norm and the Q/K/V linear be fused?
- **LoRA matmul + residual add**: Can the LoRA output addition be fused into the main matmul?
- **Activation + gate** (SwiGLU): Is the current geglu/swiglu kernel fully fused?
- **Cross-entropy + backward**: Can the loss and its gradient be computed in one pass?
- **RoPE + attention**: Can RoPE application be fused into the attention kernel?

## Also investigate
- `torch.compile` with `mode='max-autotune'` — does it find fusions unsloth's manual kernels miss?
- Compare `torch.compile` throughput vs unsloth's manual triton kernels

## Output
- `workspace/039_fusion_opportunities.md` — complete fusion map with estimated impact per fusion
- Prototype implementation of the highest-value fusion in `workspace/kernels/`
