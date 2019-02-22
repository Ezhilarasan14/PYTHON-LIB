from PIL import Image
import pytesseract

def imageTOText(filePath):
    im = Image.open(filePath)
    text = pytesseract.image_to_string(im,lang = 'eng')
    return (text)

textResult = imageTOText("macos.png")
print(textResult)