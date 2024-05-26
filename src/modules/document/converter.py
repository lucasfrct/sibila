# flake8: noqa: E501

import re
import pandas as pd
from src.modules.document import documentpdf

# Path to the PDF file
pdf_path = "./codigo_civil_brasileiro.pdf"

roman_numerals_pattern = r'\b[ivxlcdm]+\b'
title_pattern = r'T[ÍI]TuLo [IVXLC]+\n([^\n]+)'
chapter_pattern = r'Cap[íi]tulo [IVXLC]+\n([^\n]+)'
section_pattern = r'Seção [IVXLC]+\n([^\n]+)'
subsection_pattern = r'Subseção [IVXLC]+\n([^\n]+)'
article_pattern = r'Art\. [0-9]+[A-Za-z]?\s*–?\s*([^\n]*)'
paragraph_pattern = r'^(Parágrafo\s*(?!único)[^\n]*)|^(§\s*\d+o?[^\n]*)'
incise_pattern = r'^[IVXLCDM]+\s*[-–]?\s*([^\n]+)'
aline_pattern = r'^[a-z]\)\s*([^\n]+)'

start_article_pattern = re.compile(r'Art\. [0-9]+[A-Za-z]?\s*–?\s*([^\n]*)', re.IGNORECASE)
stop_article_pattern = re.compile(r'\b[I|V|X|L|C]+\b|Parágrafo|Art\. [0-9]|\.\.{10,}', re.IGNORECASE)


def convert_to_uppercase(match):
    return match.group(0).upper()

def roman_format(text):
    return re.sub(roman_numerals_pattern, convert_to_uppercase, text, flags=re.IGNORECASE)

# Function to extract text and structure it
def extract_and_structure_text(lines):
    
    data = []
    current_title = current_chapter = current_section = current_subsection = current_article = current_paragraph = current_incise = current_aline = None
    
    lastLines = []
    sizeContext = 2
    current_article_list = []
    current_paragraph_list = []
    for line in lines:
        
        line = line.strip()
        
        if(len(lastLines) < sizeContext):
            lastLines.append(line)
            
        if(len(lastLines) >= sizeContext):
            lastLines.pop(0)
            lastLines.append(line)
        
        context = " ".join(s+"\n" for s in lastLines)
                
        title_match = re.search(title_pattern, context, re.IGNORECASE)
        chapter_match = re.match(chapter_pattern, context, re.IGNORECASE)
        section_match = re.match(section_pattern, context, re.IGNORECASE)
        subsection_match = re.match(subsection_pattern, context, re.IGNORECASE)
        paragraph_match = re.match(paragraph_pattern, line, re.IGNORECASE)
        # incise_match = re.match(incise_pattern, context, re.IGNORECASE)
        # aline_match = re.match(aline_pattern, line)
        
        # article_match = re.match(article_pattern, current_article, re.IGNORECASE)
        
        if stop_article_pattern.search(line) and len(current_article_list) > 0:
            current_article = ' '.join(current_article_list)
            current_article_list = []
            
        if len(current_article_list) > 0:
            current_article = ""
            current_article_list.append(line)
            continue
        
        if start_article_pattern.search(line) and len(current_article_list) == 0:
            current_article_list.append(line)
            
        # paragrafos
        if stop_article_pattern.search(line) and len(current_paragraph_list) > 0:
            current_paragraph = ' '.join(current_paragraph_list)
            current_paragraph_list = []
            print("TERMINOU PRG", current_paragraph)
            
        if len(current_paragraph_list) > 0:
            current_paragraph = ""
            current_paragraph_list.append(line)
            continue
        
        if paragraph_match and len(current_paragraph_list) == 0:
            current_paragraph_list.append(line)
        
        print("-")      
                 
        if title_match:
            current_title = title_match.group(0).replace("\n", "").title()
            current_title = roman_format(current_title)
            line = context.replace("\n", "")
            
        if chapter_match:
            current_chapter = chapter_match.group(0).replace("\n", "").title()
            current_chapter = roman_format(current_chapter)
            
        if section_match:
            current_section = section_match.group(0).replace("\n", "").title()
            current_section = roman_format(current_section)
            
        if subsection_match:
            current_subsection = subsection_match.group(0).replace("\n", "").title() 
            
        if current_article:
            print("->", current_article[:20]) 
            
        if current_paragraph:
            print("----> PAR: ", current_paragraph)

        # elif incise_match:
        #     current_incise = incise_match.group(0)
        # elif aline_match:
        #     current_aline = aline_match.group(0)
        #     data.append(['alinea', line, current_title, current_chapter, current_section, current_subsection, current_article, current_paragraph, current_incise, current_aline])
        # elif line:
        #     # Handle non-matching lines
        
        klass = None
        if current_aline:
            klass = 'alinea'
        elif current_incise:
            klass = 'inciso'
        elif current_paragraph:
            klass = 'paragrafo'
        elif current_article:
            klass = 'artigo'
        elif current_subsection:
            klass = 'subseção'
        elif current_section:
            klass = 'seção'
        elif current_chapter:
            klass = 'capítulo'
        elif current_title:
            klass = 'título'  
                
        data.append([klass, line, current_title, current_chapter, current_section, current_subsection, current_article, current_paragraph, current_incise, current_aline])
        
    return data

# Extract and structure the text  the PDF


linesRaw = documentpdf.lines_with_details(pdf_path, 26, 26)
lines = [l['content'] for l in linesRaw]

data = extract_and_structure_text(lines)
# print(data)

# # Convert the data into a DataFrame
# df = pd.DataFrame(data, columns=['classe', 'texto', 'titulo', 'capitulo', 'secao', 'subsecao', 'artigo', 'paragrafo', 'inciso', 'alinea'])

# # Save DataFrame to CSV
# csv_path = 'codigo_civil_brasileiro.csv'
# df.to_csv(csv_path, index=False)

# print(f"CSV file saved at {csv_path}")
