import os
from xml.etree import ElementTree as ET

import untangle
import zipfile

HEADING_DATA = {
    "Title": "Title",
    "Heading1": "h1",
    "Heading2": "h2",
    "Heading3": "h3",
    "Heading4": "h4",
    "Heading5": "h5",
    "Heading6": "h6",
}


class DocxParser:
    def __init__(self, docx_file, html_file):
        self._docx = docx_file
        self._html = html_file
        self._paragraph_elements = []

    @staticmethod
    def _paragraph_text(p):
        """Returns the joined text of the text elements under the given paragraph tag"""
        if hasattr(p.w_r, "w_t"):
            text_elements = p.w_r.w_t
            if text_elements is not None:
                return text_elements.__dict__.get("cdata")
        return ''

    @staticmethod
    def _heading_type(p):
        paragraph_info = p.w_pPr
        if hasattr(paragraph_info, "w_pStyle"):
            paragraph_style = paragraph_info.w_pStyle.__dict__ if hasattr(paragraph_info, "w_pStyle") else {}
            attributes = paragraph_style.get("_attributes")
            title = attributes.get("w:val") if attributes else None

            return HEADING_DATA.get(title) if title else 'p'
        else:
            return 'p'

    @staticmethod
    def _text_family_info(p):
        paragraph_styles = p.w_pPr.w_rPr
        font_color = f"#{paragraph_styles.w_color.__dict__.get('_attributes').get('w:val')}" if hasattr(
            paragraph_styles,
            'w_color') else "#000000"
        font_family = paragraph_styles.w_rFonts.__dict__.get('_attributes').get('w:ascii') if hasattr(paragraph_styles,
                                                                                                      "w_rFonts") else "Lora"
        font_attribute = paragraph_styles.__dict__.get("_attributes")
        font_size = f"{int(font_attribute.get('w:val')) // 2}" if font_attribute else "11"
        return font_family, font_size, font_color

    def _parse(self):
        with zipfile.ZipFile(self._docx) as docx:
            content = docx.read('word/document.xml').decode('utf-8')
            parsed_content = untangle.parse(content)
            w_document = parsed_content.w_document
            if not w_document:
                ValueError("Unable to parse document")
            self._paragraph_elements = w_document.w_body.w_p

    def parse(self):
        self._parse()

    def export_html(self):
        if not self._paragraph_elements:
            ValueError("Please run parse first")
        if not self._paragraph_elements:
            ValueError("Please run parse first")
        html = ET.Element('html')
        body = ET.Element('body')
        html.append(body)

        for paragraph in self._paragraph_elements:
            text = self._paragraph_text(paragraph)
            if text:
                paragraph_type = self._heading_type(paragraph)
                font_info = self._text_family_info(paragraph)
                font_family, font_size, font_color = font_info

                html_attributes = {
                    'style': f"color:{font_color}; font-family: {font_family}"} if paragraph_type else {
                    'style': f"color:{font_color}; font-family: {font_family}; font-size: {font_size}"}

                div = ET.Element(paragraph_type, attrib=html_attributes)
                div.text = text
                html.append(div)

            else:
                html.append(ET.Element("br"))

        tree = ET.ElementTree(html)
        with open(os.path.join(os.getcwd() + self._html), 'w') as f:
            tree.write(f, encoding='unicode')

        return os.path.join(os.getcwd() + self._html)


