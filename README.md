# Project Documentation

## Main Setup

To set up the project, follow these steps:

0. Environment Variables
   Make sure to set the `OPENAI_API_KEY` environment variable with your OpenAI API key to allow the application to function correctly.

1. Create a new conda environment:

   ```bash
   conda create -n agstudio python=3.11
   conda activate agstudio
   ```

2. Install the required package:

   ```bash
   pip install autogenstudio==0.4.0.dev41
   ```

3. Run Autogen Studio (The UI provided for autogen)
   ```bash
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
