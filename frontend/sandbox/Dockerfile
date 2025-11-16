FROM ubuntu:22.04

RUN apt update && apt install -y python3 g++ gcc build-essential

WORKDIR /sandbox

COPY run.sh /sandbox/run.sh
RUN chmod +x /sandbox/run.sh

RUN useradd runner
USER runner

CMD ["/sandbox/run.sh"]
