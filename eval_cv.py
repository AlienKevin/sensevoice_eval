import json
from evaluate import load

cer_metric = load("cer")

def calculate_cer(expected, transcription):
    """
    Calculate the Character Error Rate (CER) between two strings.
    """
    return cer_metric.compute(predictions=[transcription], references=[expected])

def convert_to_simplified(text):
    """
    Convert traditional Chinese text to simplified Chinese using opencc.
    """
    from opencc import OpenCC
    converter = OpenCC('t2s')
    return converter.convert(text)

def remove_emotion_and_event_tokens(text):
    """
    Remove emotion and event tokens from text.
    """
    emo_set = {"😊", "😔", "😡", "😰", "🤢", "😮"}
    event_set = {"🎼", "👏", "😀", "😭", "🤧", "😷",}
    return ''.join(char for char in text if char not in emo_set and char not in event_set)

def remove_punctuations(text):
    """
    Remove punctuations from text.
    """
    import regex
    return regex.sub(r'\p{P}+', '', text)

# Read the transcriptions.json file
with open('cv16_transcriptions.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Calculate CER for each entry after converting expected sentences to simplified Chinese
total_cer = 0
count = 0

for entry in data:
    expected_simplified = remove_punctuations(convert_to_simplified(entry['expected']))
    generated = remove_punctuations(convert_to_simplified(remove_emotion_and_event_tokens(entry['transcription'])))
    cer = calculate_cer(expected_simplified, generated)
    # print(f'Expected: {expected_simplified} | Transcription: {generated} | CER: {cer}')
    total_cer += cer
    count += 1

average_cer = total_cer / count if count > 0 else 0
print(f'Average CER: {average_cer * 100:.2f}%')
