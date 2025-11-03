import os
import sys
import html
import argparse
from lxml import etree
#--------------------------------------------------------------------------------------------------
#  Les tags à traduire
#--------------------------------------------------------------------------------------------------
# les tags liées à toutes les questions
question_tags=["//name/text","//questiontext/text"]
# les tags de catégorie à traduire
category_tags=["//category/text"]
# d'autres tags à traduire
general_feedback = ["//generalfeedback/text"]
# les tags de feedbacks partiels 
partial_feedbacks=["//correctfeedback/text",
                   "//partiallycorrectfeedback/text",
                   "//incorrectfeedback/text"]
# les tags qui ont des CDATA
with_cdata=["//questiontext/text"]
# dictionnaire qui regroupe les tags par type
tags_a_traduire_par_type={ "coderunner"  : question_tags + general_feedback,
                           "matching"    : question_tags + general_feedback + partial_feedbacks,
                           "multichoice" : question_tags + general_feedback + partial_feedbacks,
                           "shortanswer" : question_tags + general_feedback + partial_feedbacks,
                           "numerical"   : question_tags + general_feedback,
                           "category"    : category_tags }
#--------------------------------------------------------------------------------------------------
def translate_text(target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate
    translate_client = translate.Client()
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    result = translate_client.translate(text, target_language=target)
    return html.unescape(result["translatedText"])

#--------------------------------------------------------------------------------------------------
def dir_path(path):
    return path if os.path.isdir(path) else argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
#--------------------------------------------------------------------------------------------------
def parsing_command_line():
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', nargs='+', type=argparse.FileType('r'),
                        default=sys.stdin,help='input files (on single or a set)',required=True)
    parser.add_argument('-o','--outpath', nargs='?', type=dir_path,
                        default='./', help='output path')
    args = parser.parse_args()

    outpath=args.outpath
    path=os.path.dirname(args.input[0].name)+'/'
    filespath=args.input
    return path,filespath,outpath,"en"

def translate_xml(file,target="en"):
    fileout=outpath+os.path.basename(file.name).replace(".xml","_en.xml")
    print(f"{file.name} -> {fileout}",file=sys.stderr)
    tree = etree.parse(file, parser)
    root = tree.getroot()
    # parcourir toutes les questions
    for question in root.findall(".//question"):
        qtype = question.get("type")
        # tag par type 
        for tag in tags_a_traduire_par_type[qtype] : 
            for t in root.xpath(tag):
                if t.text:
                    translated=translate_text(target,t.text)
                    t.text = etree.CDATA(translated) if tag in with_cdata else translated
    tree.write(fileout, encoding="UTF-8", xml_declaration=True, pretty_print=False)

#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    path,filespath,outpath,target = parsing_command_line()

    parser = etree.XMLParser(strip_cdata=False, remove_comments=False)

    for file in filespath :
        translate_xml(file,target=target)
