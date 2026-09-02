import re

file_path = r"C:\zsh-Robllama-copilot-ai\vendor\deepseek-v3-inference\magnetic_field_engine.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Target the exact broken block
old_block = """        with open('C:\\zsh-Robllama-copilot-ai\\vendor\\deepseek-v3-inference\\magnetic_field_proof.json', 'w') as f:
            json.dump(complete_proof, f, indent=2, default=str)"""

new_block = """        import os
        out_path = r"C:\\zsh-Robllama-copilot-ai\\vendor\\deepseek-v3-inference\\magnetic_field_proof.json"
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(complete_proof, f, indent=2, default=str)
        print(f" Magnetic field proof saved: {out_path}\\n")"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[SUCCESS] Path fix patched successfully via Python script!")
else:
    print("[WARNING] Exact target block not found, let's check file contents.")
