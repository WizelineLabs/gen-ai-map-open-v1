# Wizeline GEN AI MAP Auto-GPT

## Overview
This project leverages AWS CDK and AWS Lambda to process and analyze data changes in a Google Spreadsheet. It consists of two main Lambda functions: one that listens for changes in a spreadsheet and queues messages in AWS SQS (Listener Lambda), and another, known as the "agent" Lambda, which performs a series of operations including web scraping, document processing, and interaction with OpenAI's API.

## Features

This POC has the following features:

- CI/CD workflow using GitHub Actions and AWS CDK
- Automatic Google Spreadsheet reading and updating
- Google Search results scraping through Serper's API
- Document processing and resizing
- Vectorstore creation
- Interaction with OPEN AI's API using LangChain
- Prompt template repository for adding context 

## Prerequisites
- AWS CLI and an AWS account with the necessary permissions to deploy AWS Lambda, SQS, and other required services.
- Node.js and AWS CDK for infrastructure deployment.
- Python 3.8 or higher for Lambda functions.
- Access to the Google Sheets API and a service account with the necessary permissions.

## Architecture
### Listener Lambda
This function listens for changes in a specified Google Spreadsheet. Upon detecting a change, it sends a message to an AWS SQS queue with the details of the change.

### Agent Lambda
Triggered by messages in the SQS queue, this function performs several operations:
   - Scrapes web pages for content related to the detected changes.
   - Processes and resizes documents.
   - Interacts with OpenAI's API for content analysis.
   - Updates the Google Spreadsheet with the analysis results.

## Directory Structure
This section contains a description of key folders and files that will help you navigate this repository.

`/` 

The root folder contains the following key files:

- `app.py`: 
  
  This is the main application file and imports a class to create the AWS infrastructure using AWS CDK libraries.
- `cdk.json` 

   Contains AWS CDK configuration parameters in key-value pairs


`/gen_ai_map_agent`

This folder contains a Python script with the class `gen_ai_map_agent_stack` that creates the AWS infrastructure via AWS CDK. 

`/functions`

This folder contains the `Listener` and `Agent` Lambda functions. The Agent Lambda function is built as a Docker container and uploaded to the ECR repository as part of the CI/CD process.

`/functions/agent_lambda/config`

This folder contains the configuration file for the `Agent` Lambda function. Parameters include Open AI model name, max tokens, temperature, chunk size, and spreadsheet name.

`/tests`

This folder contains a unit test script for the `gen_ai_map_agent_stack` class.



## Environment Setup
1. **AWS Configuration:**
   - Configure your AWS credentials using the AWS CLI.

2. **Google Sheets API:**
   - Create a Google Cloud project and enable the Google Sheets API.
   - Create a service account in the Google Cloud Console and download the `drive_client_secret.json` file.

3. **Environment Variables:**
   - Set up the following environment variables in a `.env` file in the root of the Lambda function:
     ```
     OPENAI_API_KEY=<your_openai_api_key>
     SERPER_API_KEY=<your_serper_api_key>
     ```

4. **CDK Deployment:**
   - Install Node.js and AWS CDK.
   - Deploy your infrastructure using the command `cdk deploy`.

5. **Local Development:**
   - Navigate to the Lambda function directory: `cd functions/agent_lambda/`.
   - Ensure you have Python 3.8 or higher installed.
   - Create an isolated Python environment and activate it.
   - Install dependencies: `pip install -r requirements-dev.txt`.
   - To run the function locally, execute: `python3 lambda_function.py`.


## Deployment
To deploy the project:
1. Ensure all prerequisites are installed and configured.
2. From the project root, run `cdk deploy` to deploy the infrastructure to AWS.

## Usage
Once deployed, the system will automatically process changes in the configured Google Spreadsheet. For local development and testing:
1. Navigate to the Lambda function directory (`functions/agent_lambda/`).
2. Run the function locally with `python3 lambda_function.py`.


## Contributing
This section contains general guidelines to contribute to this repository.

### Branch naming conventions
Create a new branch for your contribution based on the following conventions:

|Contribution|Scenario|
|---|---|
|`feature/`|For adding new features to the Auto-GPT.|
|`fix/`|For fixing bugs or issues.|
|`enhancement/`|For enhancements or improvements to existing features or functionalities.|
|`test/`|For adding or improving test cases and test-related changes.|
|`docs/`|For changes related to updating the POC documentation.|

### Commits and Pull Requests

To ensure an efficient collaboration process, make sure to follow these guidelines:

- Create a new branch for each separate contribution.
- Maintain a clean and consistent coding style throughout your contributions.
- Test your changes thoroughly and ensure they don't introduce any regressions.
- Write clear and descriptive messages for each one of your commits.
- Write a clear title and description for your Pull Request when you want to merge your contributions to the `main` branch.
- Check the issue tracker or the project's discussion forum for existing discussions or known issues related to your contribution.




## Author
**Santiago Morillo Segovia**
- Email: [santiago.morillo@wizeline.com]


## License
MIT License
