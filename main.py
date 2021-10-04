import emailForwarder
import emailListener
import imaplib
import time
import yaml
import checkHash
with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


def startApplication():
    user = data["imapUsername"]
    pwd = data["imapPassword"]
    m = imaplib.IMAP4_SSL(data["imapServerUrl"])
    m.login(user, pwd)
    while True:
        results = emailListener.listen(m)
        if results is not None:
            print(results)
            emailForwarder.send_email(results["destination"], "Secure Email",
                                      "Document is not altered in any form \n Verified with blockchain",
                                      results["attachmentPath"])
            print("Hash of the attachment is : " + checkHash.hash_file(results["attachmentPath"]))
        time.sleep(10)


if __name__ == '__main__':
    startApplication()
