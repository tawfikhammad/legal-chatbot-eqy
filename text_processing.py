import re 

def preprocess_text(text):
    lines = text.split('\n')
    
    filtered_lines = [line for line in lines if len(line.strip()) != 1]
    text = '\n'.join(filtered_lines)
    
    text = text.strip()
    text = text.replace('\n', ' ')

    text = re.sub(r'(:|\.)', r'\1\n', text)
    
    return text

def summarize_text(text):
    text = preprocess_text(text)

    # Implement a summerizer later
    # ...

    return text 

