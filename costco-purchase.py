import os
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv

load_dotenv()

model = "gpt-4o-mini"
llm_config = {
    "model": model,
    "api_key": os.environ.get("OPENAI_API_KEY"),
}



assistant = AssistantAgent(
    name="Assistant",
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="TERMINATE",  
    code_execution_config={
        "work_dir": "coding",
        "use_docker": True,  # make it True if you want to use docker
    },
)

user_proxy.initiate_chat(
    assistant, message="Plot a chart of META and TESLA stock price change. Install any necessary dependencies"
)

# start the agents
# response = user_proxy.generate_reply(
#     message="""
#     automate the following workflow for me:
# 1. go to https://www.costco.com/ and click the sign in button in the top right. The button contains a div element with the text “sign in / register”
# 2. Log into my Costco account using these creds - username from the env var “$COSTCO_USERNAME”, password from the env var “$COSTCO_PASS”
# 3. Navigate directly to the Uber gift card product page at this url: https://www.costco.com/uber---two-50-egift-cards.product.4000282374.html
# 4. Add the gift card to the cart with a default quantity.
# 5. Proceed to the checkout page and stop before completing the purchase.
# 6. capture screenshots at every step In the UI 
# Requirements:
# * Execute the script directly and ensure it works end-to-end.
# * Debug and fix any issues during execution.
# * Validate each step:
#     * Ensure login is successful.
#     * Confirm the product is added to the cart.
#     * Verify the script reaches the checkout page.
# * Log all actions and outcomes for transparency.
# * MUST HAVE: Capture screenshots at critical steps for manual review.
# Execution and Iteration:
# * If any step fails, debug the issue, update the script, and re-run it until all steps are completed successfully.
# Implementation Details:
# * Use Python and Playwright for automation.
# * Handle credentials securely.
# * Provide the final working script and a summary of fixes made to achieve success.
#     """,
# )

# print(response)
