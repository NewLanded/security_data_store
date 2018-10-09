import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from source.conf import FROM_ADDR, TO_ADDR, SMTP_SERVER, PASSWORD
from source.util_base.db_util import store_failed_message, get_connection


def send_email(subject, text):
    try:
        mail_msg = MIMEMultipart()
        mail_msg['Subject'] = subject
        mail_msg['From'] = FROM_ADDR
        mail_msg['To'] = ','.join(TO_ADDR)
        mail_msg.attach(MIMEText(text, 'html', 'utf-8'))

        server = smtplib.SMTP_SSL()
        server.connect(SMTP_SERVER, 465)  # 连接smtp服务器
        server.login(FROM_ADDR, PASSWORD)  # 登录邮箱
        server.sendmail(FROM_ADDR, TO_ADDR, mail_msg.as_string())  # 发送邮件
        server.quit()
    except Exception as e:
        session = get_connection()
        store_failed_message(session, "", "100001", str(e), datetime.datetime.now())
        session.close()


if __name__ == "__main__":
    send_email("BS", "感谢您成为谷歌上网助手会员，你的本次支付的信息如下<br> code b_point s_point quantity tactics_code<br> 002463 0.0 0.0 0 fluctuation_tactics_1<br> 600856 0.0 0.0 0 fluctuation_tactics_1<br> 002526 0.0 0.0 0 fluctuation_tactics_1<br>")
