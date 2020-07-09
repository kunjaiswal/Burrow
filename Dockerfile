#this Dockerfile needs to be in folder where Burrow is present
#->Burrow
#->Dockerfile
FROM golang:1.14.4-alpine AS build
MAINTAINER vishwanath.kulkarni@sap.com
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q python-all python-pip
RUN apt-get install -y nano iputils-ping telnet curl vim jq
RUN apt-get update -y
RUN apt-get install -y curl software-properties-common
RUN curl -sL https://deb.nodesource.com/setup_10.x |   bash -
RUN apt-get install -y wget
RUN wget -q -O - https://packages.cloudfoundry.org/debian/cli.cloudfoundry.org.key |  apt-key add -
RUN echo "deb https://packages.cloudfoundry.org/debian stable main" | tee /etc/apt/sources.list.d/cloudfoundry-cli.list
RUN apt-get update -y
RUN apt-get install -y cf-cli
RUN apt-get install -y net-tools
#ADD ./Burrow /opt/Burrow/
#ADD ./setup.sh /go/src/setup.sh
#RUN chmod u+x /go/src/setup.sh
#ADD ./rootCA.crt /go/src/rootCA.crt
WORKDIR /go/src
EXPOSE 5000
RUN echo $PATH
RUN go get -u github.com/golang/dep/cmd/dep
RUN go get -u github.com/kunjaiswal/Burrow
RUN cd $GOPATH/src/github.com/kunjaiswal/Burrow && \
	dep ensure && \
	go build
RUN cd $GOPATH/src/github.com/kunjaiswal/Burrow && \
    mv Burrow $GOPATH/src/
RUN cd $GOPATH/src/github.com/kunjaiswal/Burrow && \
    mv kafka-config/burrow.toml $GOPATH/src/
RUN cd $GOPATH/src/github.com/kunjaiswal/Burrow && \
    mv kafka-config/setup.sh $GOPATH/src/
RUN chmod u+x /go/src/setup.sh
RUN echo "source /go/src/setup.sh" > /go/src/.bashrc

CMD ["Burrow","--config-dir","."]