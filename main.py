import os
import smtplib
from email.message import EmailMessage
import metal_rate

if __name__ == "__main__":

    sender = os.environ.get('EMAIL_SENDER')
    receivers = os.environ.get('EMAIL_RECEIVERS')
    password = os.environ.get("EMAIL_PASSWORD")
    url = os.environ.get('URL')

    data = metal_rate.compute_rate(url)

    message = EmailMessage()

    message['Subject'] = f"Metal Rate {data['date']}"
    message['From'] = sender
    message['To'] = receivers

    message.set_content("Hi There!")


    message.add_alternative(f"""\
    <!DOCTYPE html>
    <html>
        <body>
            <p style="font-size: 0.9rem; color: #od1b2a;">Hi / வணக்கம் 👋 </p>
            <br>
            <h3 style="color:#0d1b2a;">சென்னை Metal Rates {data['date']}</h3>
            <h3 style="color:#393d3f">🪙 Gold</h3>
            <b>24K</b>
            <span style="font-size: 1.5rem; font-weight: bold; color:{data['gold']['24k']['color']};">  {data['gold']['24k']['symbol']}</span>
            <p style="font-size:1rem;">
                1g ⟶ ₹{data['gold']['24k']['1g']}
            </p>
            <p style="font-size:1rem;">
                8g ⟶ ₹{data['gold']['24k']['8g']}
            </p>
            <b>22K</b>
            <span style="font-size: 1.5rem; font-weight: bold; color:{data['gold']['22k']['color']};">  {data['gold']['22k']['symbol']}</span>
            <p style="font-size:1rem;">
                1g ⟶ ₹{data['gold']['22k']['1g']}
            </p>
            <p style="font-size:1rem;">
                8g ⟶ ₹{data['gold']['22k']['8g']}
            </p>
            <br>
            <h3 style="color:#393d3f">🔘 Silver <span style="font-size: 1.5rem; font-weight: bold; color:{data['silver']['color']};">  {data['silver']['symbol']}</span></h3>
            <p style="font-size:1rem;">
                1g ⟶ ₹{data['silver']['1g']}
            </p>
            <br>
            <p class="padding:3px 5px; background-color:#eeeeee; border-radius: 20px; font-size:0.4rem; font-weight:light; color:#777777;">Made by SudoCodeDev with ❤️ </p>
        </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(message)
