import sys
import io
import tokenize
import re
import ast
import unicodedata
import random
import os

def debug_print(msg):
    print("[DEBUG]", msg)

SLANG_DICT = {
    "voce": "vc",
    "porque": "pq",
    "qualquer": "qlq",
    "programacao": "prog",
    "amigo": "parc",
    "legal": "massa",
    "obrigado": "valeu",
    "obrigada": "valeu",
    # Acrescente outros termos se necessário
}

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join(c for c in nfkd_form if not unicodedata.combining(c))

def normalize_word(word):
    word = word.lower()
    word = word.replace("ç", "c")
    word = word.replace("é", "eh")
    return remove_accents(word)

def abbreviate_normalized_word(word):
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
    def replace_word(match):
        word = match.group(0)
        norm = normalize_word(word)
        if norm in SLANG_DICT:
            return SLANG_DICT[norm]
        # Para teste, sempre transforma:
        return abbreviate_normalized_word(norm)
    result = re.sub(r'\b\w+\b', replace_word, text, flags=re.UNICODE)
    debug_print("auto_slangify: " + result)
    return result

def process_code(code):
    debug_print("Input code:\n" + code)
    if not code.endswith("\n"):
        code += "\n"
        debug_print("Adicionada nova linha final.")
    result_tokens = []
    # Converte a string para UTF-8 para tokenização (garante bytes válidos)
    code_bytes = code.encode('utf-8')
    try:
        tokens = tokenize.tokenize(io.BytesIO(code_bytes).readline)
        tokens_list = list(tokens)
        debug_print("Tokenização completa. Número de tokens: " + str(len(tokens_list)))
        tokens = tokens_list
    except Exception as e:
        debug_print("Erro ao tokenizar o código: " + str(e))
        return code
    for token in tokens:
        if token.type == tokenize.COMMENT:
            prefix = "#"
            comment_text = token.string[1:]
            new_comment_text = auto_slangify(comment_text)
            new_token_string = prefix + new_comment_text
            debug_print("Processando comentário: '" + token.string.strip() + "' -> '" + new_token_string.strip() + "'")
            new_token = tokenize.TokenInfo(token.type, new_token_string, token.start, token.end, token.line)
            result_tokens.append(new_token)
        elif token.type == tokenize.STRING:
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
                    debug_print("Processando string triple-quoted: " + token.string[:30] + "...")
                    new_token = tokenize.TokenInfo(token.type, new_token_string, token.start, token.end, token.line)
                    result_tokens.append(new_token)
                except Exception as e:
                    debug_print("Erro ao processar string triple-quoted: " + str(e))
                    result_tokens.append(token)
            else:
                result_tokens.append(token)
        else:
            result_tokens.append(token)
    try:
        new_code = tokenize.untokenize(result_tokens)
    except Exception as e:
        debug_print("Erro ao reconstruir código: " + str(e))
        new_code = code
    if isinstance(new_code, bytes):
        new_code = new_code.decode('utf-8')
    lines = new_code.splitlines()
    new_lines = []
    for line in lines:
        if line.strip() == "":
            if not new_lines or not (new_lines[-1].strip().startswith("#") and set(new_lines[-1].strip()) == {"#"}):
                num_hashes = random.randint(60, 100)
                divider = "#" * num_hashes
                debug_print("Inserindo divisor: " + divider)
                new_lines.append(divider)
        new_lines.append(line)
    final_code = "\n".join(new_lines)
    debug_print("Final code:\n" + final_code)
    return final_code

if __name__ == '__main__':
    print("Iniciando o processamento...")
    if len(sys.argv) < 3:
        print("Uso: process_code_ahk.py <arquivo_entrada.txt> <arquivo_saida.txt>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    try:
        # Lê o arquivo de entrada usando cp1252
        with open(input_file, 'r', encoding='cp1252') as f:
            code = f.read()
        processed_code = process_code(code)
        # Grave o arquivo de saída usando cp1252
        with open(output_file, 'w', encoding='cp1252') as f:
            f.write(processed_code)
        print("Processamento concluído. Saída gravada em:", output_file)
    except Exception as e:
        with open(output_file, 'w', encoding='cp1252') as f:
            f.write("Erro: " + str(e))
        print("Erro:", e)
