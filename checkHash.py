import hashlib, base64, os

def hash_file(attach_path):
    # attach_path= os.path.join('attachments/',filename)
    print(attach_path)
    h = hashlib.sha512(open(attach_path, 'rb').read()).digest()
    encoded = base64.standard_b64encode(h)
    encodedStr= str(encoded,encoding='UTF-8')
    return encodedStr
