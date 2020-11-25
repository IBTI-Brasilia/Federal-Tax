import textract
import re
import json
import csv
 
pdf_name = "./acordaos-18-11-2020/03.PDF"
text = textract.process(pdf_name, method='pdfminer').decode('utf-8')

def cleanner(text):
    '''
    Cleans some parts unwanteds and prepares the text for extration
    Add new words in the variable 'keywords' whenever necessary
    '''
    blocks = re.split('\n\n', text)
    keywords = ["assinado", "fl. 2", "df carf mf",]
    for block in blocks:
        comparative_paragraph = block.lower()
        for keyword in keywords:
            if keyword in comparative_paragraph:
                position_exc = comparative_paragraph.find(keyword)
                excludent = block[position_exc:]
                text = text.replace(excludent, " ")
    paragraphs = re.split('\n', text)
    return paragraphs
    

def get_orgao(paragraphs):
    '''
    Gets the organization of each judgment and treats them.
    Returns the organization.
    '''
    orgao = ''
    keyword = "conselho"
    for paragraph in paragraphs:
        comparative_paragraph = paragraph.lower()
        if keyword in comparative_paragraph:
            orgao = paragraph
            break
    return orgao


def find_processos(text):
    '''
    Finds the process number.
    Receives the text and returns the occurrences of process numbers.
    '''
    pattern = r"\d{5}\.\d{5}.?\d\/\d{4}[^\d]\d{2}|\d?\d?\d{3}\.?\d{3}.?\d{3}\/\d{2}(-| )\d{2}|\d?\.?\d{3}.\d{3}"
    return re.findall(pattern, text)


def get_processos(paragraphs):
    '''
    Treates and gets the first occurrence of the process number.
    '''
    for paragraph in paragraphs:
        comparative_paragraph = paragraph.lower()
        if find_processos(paragraph):
            out = paragraph
            break
    try:
        return out
    except:
        print("Process number not found")


def get_named_ementa(paragraphs):
    '''
    Extracts the ementas that have a start word.
    Receives the clear text and returns the ementa.
    '''
    texts = []
    starts = ["assunto:", "ementa"]
    ends = ["vistos", "acordam", "acórdão"]
    mark = 0
    
    for paragraph in paragraphs:
        comparative_paragraph = paragraph.lower()
        if mark == 0:
            for start in starts:
                if start in comparative_paragraph:
                    mark = 1
                    break    
        if mark == 1:
            texts.append(paragraph)
            for end in ends: 
                if end in comparative_paragraph:
                    ementa = '\n'.join(texts)
                    return ementa


def get_unnamed_ementa(text):
    '''
    Extracts the ementas that do not have a start word.
    Receives the pure text and returns the ementa.
    '''
    paragraphs = re.split('\n\n', text)
    texts = []
    rest = []
    ends = ["vistos", "acordam"]
    mark = 0
    
    for paragraph in paragraphs:
        comparative_paragraph = paragraph.lower()
        for end in ends: 
            if end in comparative_paragraph:
                ementa = '\n'.join(texts[-5:])
                rest.append(ementa)
                mark = 1
                break
        if mark == 1:
            rest.append(paragraph)
        texts.append(paragraph)
    text = '\n'.join(rest)
    return ementa, text


def get_text(paragraphs):
    texts = []
    starts = ["assunto:", "ementa"]
    mark = 0
    
    for paragraph in paragraphs:
        comparative_paragraph = paragraph.lower()
        if mark == 0:
            for start in starts:
                if start in comparative_paragraph:
                    mark = 1
                    break          
        if mark == 1:
            texts.append(paragraph)
    text = '\n'.join(texts)
    return text

################################

paragraphs = cleanner(text)

if get_orgao(paragraphs):
    orgao = get_orgao(paragraphs)
else:
    orgao = "Superior Tribunal de Justiça"

processo = get_processos(paragraphs)

# Se a ementa tiver indicada com "assunto"
# ementa = get_named_ementa(paragraphs)

# Se a ementa não tiver indicada
ementa, texto = get_unnamed_ementa(text)

# texto = get_text(paragraphs)

print(orgao)
print("--------------------")
print(processo)
print("--------------------")
print(ementa)
# print("--------------------")
# print(texto)
# with open('dados_acordaos.csv', mode='a', newline='') as csv_file:
    
#     fieldnames = ["nomePdf", "orgao", "processo", "ementa", "texto"]
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
#     writer.writerow({"nomePdf": pdf_name, "orgao": orgao, "processo": processo, "ementa": ementa, "texto": texto})
     








# Se a ementa não tiver indicada
# dados['ementa'], dados['texto'] = get_unnamed_ementa(text)


# with open('./jsons/26.json', 'w') as fp:
#             fp.write(json.dumps(dados, ensure_ascii=True, indent=4))