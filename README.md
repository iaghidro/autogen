# Project Documentation

# Prereqs

1. Environment Variables
   Make sure to set the `OPENAI_API_KEY` environment variable with your OpenAI API key to allow the application to function correctly. This needs to be added to a `.env` file at the root of the repo.

2. Install Conda
   Installation docs found [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

## Main Setup

To set up the project, follow these steps. For more info refrence the installation docs [here](https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/installation.html):

3. Create a new conda environment:

   ```shell
   conda create -n ag-mic python=3.12
   conda activate ag-mic
   ```

   delete if necessary by running:

   ```shell
   conda remove --name ag-mic --all
   ```

   to deactive later run:

   ```shell
   conda deactivate
   ```

4. Install autogen
   ```shell
   pip install -U "autogen-agentchat" "autogen-ext" "autogen-ext[openai]"
   ```

## Autogen Studio

1. Install the required package for Autogen Studio:

   ```shell
   pip install autogenstudio==0.4.0.dev41
   ```

2. Run Autogen Studio (The UI provided for autogen)
   ```shell
   autogenstudio ui --port 8081 --appdir /Users/iaghidro/repos/autogen/studio
   ```

## Overview

This repository contains a chat application that utilizes AI agents to perform tasks based on user input. The main components of the application include:

### 1. `group_chat_tool.py`

This file sets up an asynchronous chat environment using a coding agent. The agent interacts with users and can execute tasks such as generating charts based on stock price changes. The user can provide feedback or exit the chat.

### 2. `shared/executors.py`

The `CodingAgent` class in this file serves as an AI assistant capable of executing Python code and shell commands. It sets up a local environment for code execution and includes a detailed system message that guides the assistant's behavior.

### 3. `shared/model_client.py`

This file defines an enumeration for different OpenAI models and a function to create a model client using the OpenAI API. This client is essential for the coding agent to interact with the OpenAI models.

## Usage

To use the application, run the files like this `python group_chat_tool.py` file. The coding agent will prompt you for tasks, and you can provide feedback or exit the chat as needed.
