import datetime
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from source.conf import FROM_ADDR, TO_ADDR, SMTP_SERVER, PASSWORD
from source.util_base.db_util import store_failed_message, get_connection


def send_email(subject, text):
    try:
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = FROM_ADDR
        msg['To'] = TO_ADDR
        msg['Subject'] = Header(subject, 'utf-8').encode()

        server = smtplib.SMTP(SMTP_SERVER, 25)
        # server.set_debuglevel(1)
        server.login(FROM_ADDR, PASSWORD)
        server.sendmail(TO_ADDR, [TO_ADDR], msg.as_string())
        server.quit()
    except Exception as e:
        session = get_connection()
        store_failed_message(session, "", "100001", str(e), datetime.datetime.now())
        session.close()


if __name__ == "__main__":
    send_email("BS", "ssssssssssssssssssssssssssss\nffffffffffffffffffffff")
