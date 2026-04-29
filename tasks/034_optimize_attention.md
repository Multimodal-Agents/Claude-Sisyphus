# Task: Optimize Unsloth's Attention Implementation

## Goal
Find improvements to how unsloth handles attention computation — currently the most compute-intensive part of any transformer.

## What to analyze
1. Find where attention is implemented in `C:/Users/Blue/git_work/unsloth/unsloth/models/llama.py` — search for `scaled_dot_product_attention`, `flash_attn`, attention mask handling
2. Read `C:/Users/Blue/git_work/flash-attention/` — what does FA3 do that unsloth isn't using?
3. Check `C:/Users/Blue/git_work/xformers/xformers/ops/fmha/` — any ops unsloth could use?
4. Check `C:/Users/Blue/git_work/unsloth/unsloth/kernels/flex_attention.py` — is flex attention being used optimally?

## Specific opportunities to investigate
- **GQA optimization**: For models with Grouped Query Attention (Llama 3, Qwen), is KV cache handled optimally?
- **Sliding window attention**: Is there a fast path for models with local attention?
- **Variable sequence length**: Does unsloth handle variable-length sequences without padding waste?
- **Context length scaling**: How does performance degrade at 8K, 16K, 32K, 128K context?
- **Causal mask**: Is the causal mask applied efficiently or does it waste computation?
- **Multi-head vs MLA**: Could Multi-head Latent Attention (DeepSeek's approach) be implemented?

## Output
- `workspace/034_attention_analysis.md` — full analysis with specific improvement proposals
- `workspace/kernels/attention_improvements.py` — any prototype implementations
- Benchmarks comparing current vs proposed attention for various sequence lengths
