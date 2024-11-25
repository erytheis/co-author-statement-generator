import zipfile
import os
from xml.etree import ElementTree as ET


def replace_placeholders_recursive(node, replacements):
    """
    Recursively replace placeholders in an XML node and its children.

    Args:
        node: The current XML node.
        replacements: Dictionary of replacements (e.g., {<TAG>: value}).
    """
    # Replace in node text
    if node.text:
        for tag, replacement in replacements.items():
            if tag in node.text:
                node.text = node.text.replace(tag, replacement)

    # Replace in node tail (text after the current tag)
    if node.tail:
        for tag, replacement in replacements.items():
            if tag in node.tail:
                node.tail = node.tail.replace(tag, replacement)

    # Recurse into child nodes
    for child in node:
        replace_placeholders_recursive(child, replacements)



def modify_odt_template(template_path, output_path, replacements):
    """
    Modifies an .odt template file by replacing tags with specified values.

    Args:
        template_path (str): Path to the input .odt template file.
        output_path (str): Path to save the modified .odt file.
        replacements (dict): Dictionary where keys are tags (e.g., <TAG>) and values are replacement strings.
    """
    # Temporary extraction folder
    temp_folder = "temp_odt"

    # Unzip the .odt file
    with zipfile.ZipFile(template_path, 'r') as odt_zip:
        odt_zip.extractall(temp_folder)

    # Path to the content XML inside the .odt file
    content_xml_path = os.path.join(temp_folder, "content.xml")

    # Parse the content.xml file
    tree = ET.parse(content_xml_path)
    root = tree.getroot()

    # Apply recursive replacement
    replace_placeholders_recursive(root, replacements)

    # Write back the modified content.xml
    tree.write(content_xml_path, encoding='UTF-8', xml_declaration=True)

    # Rezip the folder into a new .odt file
    with zipfile.ZipFile(output_path, 'w') as odt_zip:
        for foldername, subfolders, filenames in os.walk(temp_folder):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, temp_folder)
                odt_zip.write(file_path, arcname)

    # Cleanup the temporary folder
    for foldername, subfolders, filenames in os.walk(temp_folder, topdown=False):
        for filename in filenames:
            os.remove(os.path.join(foldername, filename))
        os.rmdir(foldername)

    print(f"Modified .odt file saved to {output_path}")


# Example Usage
template_path = "template.odt"  # Path to your template .odt file
output_path = "output.odt"  # Path to save the modified .odt file
replacements = {
    "AUTHOR_NAME": "Willy Wonka",
    "THESIS_NAME":'THESIS',
    "PAPER_NAME": '',
    "CONTRIBUTION": "conceptualization, methodology, experimentation, and the writing phase.",
    "CO_AUTHOR_NAME": "Joh n Doe"
}

modify_odt_template(template_path, output_path, replacements)
