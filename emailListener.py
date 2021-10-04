import email
import mailparser
import os

detach_dir = 'attachments/'


def listen(m):
    att_path = ""
    m.select("Inbox")
    resp, items = m.search(None, 'UNSEEN', 'FROM', 'sajin.alex@outlook.com')
    # get mails id
    items = items[0].split()

    for emailid in items:
        resp, data = m.fetch(emailid, "(RFC822)")
        email_body = data[0][1]  # getting the mail content
        mail = email.message_from_bytes(email_body)  # parsing the mail content to get a mail object
        mailp = mailparser.parse_from_bytes(email_body)

        if mail.get_content_maintype() != 'multipart':
            continue

        print("[" + mail["From"] + "] :" + mail["Subject"])
        source = mail["Subject"]
        destination = mailp.body

        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue

            # is this part an attachment ?
            if part.get('Content-Disposition') is None:
                continue

            # filename = part.get_filename()
            filename = mailp.attachments[0]['filename']
            print("filename :: " + filename)

            counter = 1

            if not filename:
                filename = 'part-%03d%s' % (counter, 'bin')
                counter += 1

            att_path = os.path.join(detach_dir, filename)

            if not os.path.isfile(att_path):
                mailp.write_attachments(detach_dir)

        jsonVar = {"source": source, "destination": destination, "attachmentPath": att_path}
        return jsonVar
