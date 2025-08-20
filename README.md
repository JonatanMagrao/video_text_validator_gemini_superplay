# Why Gemini (or any multimodal LLM) Alone Can Fail at Consistent OCR

## 1. Not a Dedicated OCR Engine
LLMs are general vision–language models. They are strong at holistic understanding, but **precise transcription** of text — especially stylized CJK fonts — is the domain of OCR engines. Without that specialized step, accuracy fluctuates.

## 2. Non-Determinism in Decoding
Even when prompts enforce JSON:
- Sampling (`temperature`, `top-p`, `top-k`) introduces randomness.  
- `temperature=0` reduces but doesn’t fully eliminate variability.  

## 3. Variable Frame Selection / Temporal Ambiguity
For video inputs:
- The backend may sample **different frames** each run.  
- Key phrases can appear in only a few frames.  
- Result: one run finds it, the next misses it.  

## 4. Preprocessing & Ingestion Differences
Cloud backends often:
- Resize, re-encode, or chunk media,  
- Choose different keyframes,  
which changes what the model “sees.”  

## 5. Text Rendering Challenges
Stylized UI text is especially fragile:  
- Outline, drop shadow, or glow,  
- Compression artifacts or motion blur,  
- Small kana differences (っ vs つ),  
- Punctuation variants (！ vs !).  

## 6. Hallucination / Over-Inference
LLMs sometimes **guess** text based on expectations, not pixels — e.g., inserting a common UI phrase that isn’t actually present.

## 7. Locale & Normalization Issues
Japanese text is prone to mismatches due to:  
- Full-width vs half-width characters,  
- Unicode normalization (NFKC vs NFC),  
- Kana variations,  
- Mixed punctuation.  

## 8. Output Format Fragility
Even with JSON-only prompts:  
- Fields can be omitted,  
- Status values inconsistent,  
- Minor prompt changes alter structure.  

## 9. Context / Length Limits
Long videos + large rule lists → internal summarization.  
Different pruning paths can drop key evidence.  

## 10. Backend Variability
Under load or rate limiting, the system may inspect fewer frames, leading to less reliable detections.  

---

## Bottom Line
Multimodal LLMs are excellent for **scene understanding**, but **reliable, repeatable OCR** requires:  
- Deterministic decoding (`temperature=0`, `top_p=0`, `top_k=1`),  
- Unicode normalization,  
- Rigid output schema (JSON Schema),  
- Ideally: a dedicated OCR step (e.g., Google Vision, PaddleOCR, MMOCR) feeding into the LLM for reasoning.  

Simply upgrading to a “stronger” LLM won’t eliminate these structural issues.

---

# Even with deterministic settings, there are two external factors that can still introduce variability:
- Video pre-processing by Gemini’s backend
- If the service selects different frames for analysis (e.g., slightly different keyframes), the extracted text may change.
- This usually doesn’t happen if you reuse the same already-processed file instead of re-uploading it each time.
- OCR performance on stylized fonts
- Since Gemini is not a pure OCR engine, heavily stylized fonts may still be misread or skipped.