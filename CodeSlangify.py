import tkinter as tk
from tkinter import scrolledtext
import io
import tokenize
import re
import ast
import unicodedata
import random

# Base de dados de gírias (as chaves devem estar normalizadas: minúsculas e sem acentos)
SLANG_DICT = {
    "voce": "vc",
    "porque": "pq",
    "qualquer": "qqr",
    "programacao": "prog",
    "amigo": "amg",
    "comigo": "cmg",
    "valeu": "vlw",
    "projeto": "proj",
    # Acrescente outros termos se necessário
}

def remove_accents(input_str):
    """
    Remove acentos usando normalização Unicode.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join(c for c in nfkd_form if not unicodedata.combining(c))

def normalize_word(word):
    """
    Converte para minúscula, substitui 'ç' por 'c' e 'é' por 'eh',
    removendo também os acentos.
    """
    word = word.lower()
    word = word.replace("ç", "c")
    word = word.replace("é", "eh")
    word = remove_accents(word)
    return word

def abbreviate_normalized_word(word):
    """
    Aplica uma heurística de abreviação em uma palavra já normalizada:
      - Se a palavra tiver 3 ou menos caracteres, retorna inalterada.
      - Para palavras de 4 a 7 caracteres: preserva os dois primeiros caracteres,
        remove as vogais do meio e mantém a última letra.
      - Para palavras com mais de 7 caracteres: preserva os dois primeiros caracteres,
        remove as vogais do restante (exceto a vogal imediatamente após o prefixo, se for vogal),
        trunca o resultado para um comprimento máximo e garante que termine com uma consoante.
    """
    vowels = "aeiou"
    n = len(word)
    if n <= 3:
        return word

    if 4 <= n <= 7:
        prefix = word[:2]
        mid = word[2:-1]
        new_mid = "".join(ch for ch in mid if ch not in vowels)
        if not new_mid and mid:
            for ch in mid:
                if ch in vowels:
                    new_mid = ch
                    break
        suffix = word[-1]
        return prefix + new_mid + suffix
    else:
        prefix = word[:2]
        remainder = word[2:]
        if remainder and remainder[0] in vowels:
            preserved = remainder[0]
            rest = remainder[1:]
            new_remainder = preserved + "".join(ch for ch in rest if ch not in vowels)
        else:
            new_remainder = "".join(ch for ch in remainder if ch not in vowels)
        abbr = prefix + new_remainder
        max_length = 6
        if len(abbr) > max_length:
            abbr = abbr[:max_length]
        while len(abbr) > 1 and abbr[-1] in vowels:
            abbr = abbr[:-1]
        return abbr

def auto_slangify(text):
    """
    Processa o texto recebido: cada palavra é normalizada e,
    se não estiver no dicionário de gírias, tem 50% de chance de ser abreviada.
    """
    def replace_word(match):
        word = match.group(0)
        norm = normalize_word(word)
        if norm in SLANG_DICT:
            return SLANG_DICT[norm]
        if random.random() < 0.5:
            return abbreviate_normalized_word(norm)
        else:
            return norm
    new_text = re.sub(r'\b\w+\b', replace_word, text, flags=re.UNICODE)
    return new_text

def process_code(code):
    """
    Processa o código Python recebido (como string) e transforma os comentários:
      - Tokens de comentário (linhas iniciadas por '#') têm seu conteúdo processado.
      - Tokens de string que começam e terminam com aspas triplas 
        terão seu conteúdo processado.
    """
    result_tokens = []
    code_bytes = code.encode('utf-8')
    try:
        tokens = tokenize.tokenize(io.BytesIO(code_bytes).readline)
    except Exception as e:
        print(f"Erro ao tokenizar o código: {e}")
        return code

    for token in tokens:
        if token.type == tokenize.COMMENT:
            prefix = "#"
            comment_text = token.string[1:]
            new_comment_text = auto_slangify(comment_text)
            new_token_string = prefix + new_comment_text
            new_token = tokenize.TokenInfo(token.type, new_token_string, token.start, token.end, token.line)
            result_tokens.append(new_token)
        elif token.type == tokenize.STRING:
            # Se for uma string delimitada por aspas triplas, processa seu conteúdo
            if ((token.string.startswith("'''") and token.string.endswith("'''")) or 
                (token.string.startswith('"""') and token.string.endswith('"""'))):
                try:
                    content = ast.literal_eval(token.string)
                    new_content = auto_slangify(content)
                    i = 0
                    while i < len(token.string) and token.string[i] in "rRuU":
                        i += 1
                    quote = token.string[i:i+3]
                    prefix_str = token.string[:i]
                    new_token_string = prefix_str + quote + new_content + quote
                    new_token = tokenize.TokenInfo(token.type, new_token_string, token.start, token.end, token.line)
                    result_tokens.append(new_token)
                except Exception as e:
                    result_tokens.append(token)
            else:
                result_tokens.append(token)
        else:
            result_tokens.append(token)

    new_code = tokenize.untokenize(result_tokens)
    if isinstance(new_code, bytes):
        new_code = new_code.decode('utf-8')

    # Percorre as linhas do código e insere uma linha divisória antes de linhas em branco,
    # mas somente se a linha imediatamente anterior não for já uma linha de divisão.
    lines = new_code.splitlines()
    new_lines = []
    for line in lines:
        if line.strip() == "":
            # Se a linha estiver em branco e a linha anterior (se houver) não for um divisor:
            if not new_lines or not new_lines[-1].strip().startswith("#") or set(new_lines[-1].strip()) != {"#"}:
                num_hashes = random.randint(0, 2)
                divider = "#" * num_hashes
                new_lines.append(divider)
        new_lines.append(line)
    new_code = "\n".join(new_lines)
    return new_code

def process_input():
    """
    Lê o código inserido, processa os comentários (e o conteúdo de strings entre aspas triplas)
    e exibe o resultado.
    """
    input_code = text_input.get("1.0", tk.END)
    output_code = process_code(input_code)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, output_code)

# Configuração da interface gráfica com Tkinter
root = tk.Tk()
root.title("Transformador de Comentários - Abreviação Automática")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

label_input = tk.Label(frame, text="Código Original:")
label_input.pack(anchor="w")
text_input = scrolledtext.ScrolledText(frame, height=15)
text_input.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

process_button = tk.Button(frame, text="Processar Código", command=process_input)
process_button.pack(pady=5)

label_output = tk.Label(frame, text="Código Transformado:")
label_output.pack(anchor="w")
text_output = scrolledtext.ScrolledText(frame, height=15)
text_output.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

root.mainloop()
