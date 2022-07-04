FROM public.ecr.aws/lambda/python:3.8

# Install the function's dependencies using file requirements.txt
# from your project folder.
COPY /requirements.txt  ./

RUN  pip3 install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

RUN pip3 install uszipcode

# Copy function code
COPY app "${LAMBDA_TASK_ROOT}/app/"

# Install packages to fix vulnerabilities issued by aws
RUN yum update zlib -y && yum update glibc -y &&  yum update libgcrypt -y && yum update openldap -y

# Download the database file
RUN python -m app.download_db

# Give necessary permissions to access the database file
RUN chmod 755 ${LAMBDA_TASK_ROOT}/app/simple_db.sqlite

ADD aws-lambda-rie /usr/local/bin/aws-lambda-rie
RUN chmod 755 /usr/local/bin/aws-lambda-rie

COPY entry.sh "${LAMBDA_TASK_ROOT}/"
RUN chmod +x ./entry.sh

ENTRYPOINT [ "./entry.sh" ]

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app/app.handler" ]