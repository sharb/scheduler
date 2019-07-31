FROM alpine:3.9

# https://github.com/aws/aws-cli/releases
ARG AWS_CLI_VERSION=1.16.155
ARG AWS_CLI_VERSION=${AWS_CLI_VERSION}

# https://releases.hashicorp.com/terraform/
ARG TERRAFORM_CLI_VERSION=0.12.3
ENV TERRAFORM_CLI_VERSION=${TERRAFORM_CLI_VERSION}

RUN apk add -v --update python py-pip curl \
    && pip install awscli==${AWS_CLI_VERSION} \
    && apk del -v --purge py-pip \
    && rm /var/cache/apk/*

RUN curl https://releases.hashicorp.com/terraform/${TERRAFORM_CLI_VERSION}/terraform_${TERRAFORM_CLI_VERSION}_linux_amd64.zip > terraform_${TERRAFORM_CLI_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_CLI_VERSION}_linux_amd64.zip -d /bin && \
    rm -f terraform_${TERRAFORM_CLI_VERSION}_linux_amd64.zip
