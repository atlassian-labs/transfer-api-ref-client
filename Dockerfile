FROM ubuntu
RUN apt-get update && apt-get install -y git python3 pip
RUN git clone https://github.com/atlassian-labs/transfer-api-ref-client
RUN mv transfer-api-ref-client/* ./
RUN pip install -r requirements.txt
