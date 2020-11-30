from pdf2image import convert_from_path
import random
import pytesseract
import os
import rhyme
import pickle
from create_pdf import generate_pdf_from_list

if not os.path.exists('./text.txt'):
    print("creating text.txt ...")
    pages = convert_from_path('Emergence and How One Might Live.pdf', poppler_path="C:/Program Files/poppler-0.68.0/bin")

    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

    page_content = ""
    for page in pages:
        page_content += pytesseract.image_to_string(page)

    with open('text.txt', 'w', encoding='utf-8') as f:
        f.write(page_content)

text = ""
with open('text.txt', 'r', encoding='utf-8') as f:
    text += f.read()

text = text.split()

word_set = list(dict.fromkeys(text))

####################################################################################################################

def generate_sentence(length, idx):
    return ' '.join(text[idx-length: idx + 1])


def monorhyme(num_sentences, start_word):
    start_word = start_word.upper()

    # get rhyme words
    rhyme_words = []

    try:
        for word in rhyme.rhymes_with(start_word):
            rhyme_words.append(word.lower())
    except:
        pass

    words = []
    # check which rhyme words also appear in text
    for word in rhyme_words:
        if word in text:
            words.append(word)

    return words


def get_sentences(words, sentence_length):
    rhyme_sentences = []

    for word in words:
        # get all indexes where word appears
        indices = [i for i, term in enumerate(text) if term == word]
        index = random.choice(indices)
        sentence = text[index - sentence_length + 1: index + 1]

        rhyme_sentences.append(' '.join(sentence))

    return rhyme_sentences


def get_rhyme_sentences(num_sentences, sentence_length):
    found = False
    while not found:
        word = random.choice(word_set)
        rhyme_words = monorhyme(num_sentences, word)
        if len(rhyme_words) >= num_sentences:
            found = True
        sentences = get_sentences(rhyme_words, sentence_length)

    sentences = random.sample(sentences, num_sentences)

    return sentences

def generate_limerick():
    B = get_rhyme_sentences(2, 3)
    A = get_rhyme_sentences(3, 5)

    return [A[0], A[1], B[0], B[1], A[2]]

def generate_monorhyme():
    length = random.randint(3, 10)
    num_sentences = random.randint(2, 10)
    return get_rhyme_sentences(num_sentences, length), length*num_sentences # total number of words


#TODO turn creat_limerick_chapter into create_chapter() so we can use it for any rhyme scheme
def create_limerick_chapter():
    contents = []
    min_num_poems = 50000/2/21  # section should be at least 50000/3 words long, and each limerick contains 21 words
    num_poems = 0
    while num_poems < min_num_poems:
        print("**************LIMERICK****************")
        limerick = generate_limerick()
        print(limerick)
        contents.append(limerick)
        num_poems += 1;
    return contents

def create_monorhyme_chapter():
    contents = []
    min_num_words = 50000/2  # section should be at least 50000/3 words long, and each limerick contains 21 words
    tot_num_words = 0
    while tot_num_words < min_num_words:
        print("**************MONORHYME****************")
        monorhyme, num_words_poem = generate_monorhyme()
        print(monorhyme)
        contents.append(monorhyme)
        tot_num_words += num_words_poem;
    return contents

if not os.path.exists('./limericks.pkl'):
    contents_limerick = create_limerick_chapter()

    file = open('limericks.pkl', 'wb')
    pickle.dump(contents_limerick, file) # store in pkl

if not os.path.exists('./monorhyme.pkl'):
    contents_monorhyme = create_monorhyme_chapter()

    file = open('monorhyme.pkl', 'wb')
    pickle.dump(contents_monorhyme, file) # store in pkl


def main():
    thesis_title = "Emergence and How One Might Live"

    limericks = open('limericks.pkl', 'rb')
    monorhymes = open('monorhyme.pkl', 'rb')

    limericks = pickle.load(limericks)
    monorhymes = pickle.load(monorhymes)

    generate_pdf_from_list(thesis_title, limericks, monorhymes)


if __name__ == '__main__':
    main()