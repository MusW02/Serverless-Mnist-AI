# 1. Use the AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.9

# 2. Copy requirements and install them
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --default-timeout=1200 --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# 3. Copy your application code and the model
COPY app.py ${LAMBDA_TASK_ROOT}
COPY mnist-8.onnx ${LAMBDA_TASK_ROOT}

# 4. CRITICAL CHANGE: Set the CMD to your Mangum handler
# "app" is the filename (app.py), "handler" is the variable inside it
CMD [ "app.handler" ]
