
class Mail():
    
    @classmethod
    def Send_Email(cls):
        import smtplib       
        gmail_user = "torrentnotifier2@gmail.com"
        gmail_pwd = "broke_ender9"
        FROM = "torrentnotifier2@gmail.com"
        TO = "sid.sharma0@gmail.com"
        SUBJECT = "Your filters have matched Torrent results"
        
        msg = "Torrents have been found matching your query!"
        BODY = '\r\n'.join(['To: {}'.format(TO),
                    'From: {}'.format(FROM),
                    'Subject: {}'.format(SUBJECT),
                    '', msg])

        
        
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.ehlo()
        s.starttls()
        s.login(gmail_user,gmail_pwd)
        
        try:
            s.sendmail(FROM, [TO], BODY)
            print ('email sent')
        except:
            print ('error sending mail')

        s.quit()
    