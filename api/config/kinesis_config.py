# -*- coding: utf-8 -*-
"""This module contain the confuguration for the application."""
import json
import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from smtplib import SMTP_SSL, SMTPException

import boto3
from dotenv import load_dotenv

load_dotenv()


class KinesisFirehoseDeliveryStreamHandler(logging.StreamHandler):
    """This class sends our logs to Amazon Kinesis."""

    def __init__(self):
        """Initialize the firehose stream.."""
        # By default, logging.StreamHandler uses sys.stderr if stream parameter is not specified
        logging.StreamHandler.__init__(self)

        self.__firehose = None
        self.__stream_buffer = []
        self.__aws_key = os.environ['AWS_KEY']
        self.__aws_secret = os.environ['AWS_SECRET']
        self.__aws_region = os.environ['AWS_REGION']

        try:
            self.__firehose = boto3.client(
                'firehose',
                aws_access_key_id=self.__aws_key,
                aws_secret_access_key=self.__aws_secret,
                region_name=self.__aws_region
            )
        except Exception:
            print('Firehose client initialization failed.')

        self.__delivery_stream_name = os.environ['FIREHOSE_DELIVERY_STREAM']

    def emit(self, record):
        """Send the formatted log to AWS Firehose."""
        try:
            msg = self.format(record)

            if self.__firehose:
                self.__stream_buffer.append({
                    'Data': msg.encode(encoding="UTF-8", errors="strict")
                })
            else:
                stream = self.stream
                stream.write(msg)
                stream.write(self.terminator)

            self.flush()
        except Exception:
            self.handleError(record)

    def flush(self):
        """Flush the log buffer."""
        self.acquire()

        try:
            if self.__firehose and self.__stream_buffer:
                self.__firehose.put_record_batch(
                    DeliveryStreamName=self.__delivery_stream_name,
                    Records=self.__stream_buffer
                )

                self.__stream_buffer.clear()
        except Exception as e:
            print("An error occurred during flush operation.")
            print(f"Exception: {e}")
            print(f"Stream buffer: {self.__stream_buffer}")
        finally:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()

            self.release()


class CustomEmailLogger(logging.Handler):
    """Custom email logger."""

    def __init__(self) -> None:
        """Initialize the logger."""
        logging.Handler.__init__(self)
        self.mailport = 465
        self.mailhost = os.environ['MAIL_HOST']
        self.fromaddr = 'lyceokoth@gmail.com'
        self.toaddrs = 'lyceokoth@gmail.com'
        self.username = os.environ['MAIL_USERNAME']
        self.password = os.environ['MAIL_PASSWORD']
        self.sender_name = 'Lyle from Amazon'

    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            log_record = json.loads(self.format(record))

            # Try to send the message.
            if log_record['levelname'] in ['CRITICAL']:
                with SMTP_SSL(self.mailhost, self.mailport) as server:
                    SUBJECT = log_record['levelname']
                    BODY_HTML = f"""
                    <html>
                        <head>
                        </head>
                        <body>
                            <h1>
                                {log_record['name']}
                            </h1>
                            <p>
                                {log_record['message']}
                            </p>
                        </body>
                    </html>"""
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = SUBJECT
                    msg['From'] = formataddr((self.sender_name, self.fromaddr))
                    msg['To'] = self.toaddrs

                    part2 = MIMEText(BODY_HTML, 'html')

                    msg.attach(part2)
                    server.login(self.username, self.password)
                    server.sendmail(self.fromaddr, self.toaddrs, msg.as_string())
                    server.close()
                    print("Email sent!")

        except SMTPException as e:
            print("Error: ", e)
        except Exception as e:
            print(f"Exception: {e}")

    def close(self):
        """Terminate the handler."""
        logging.Handler.close(self)
