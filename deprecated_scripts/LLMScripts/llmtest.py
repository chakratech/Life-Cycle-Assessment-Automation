import openai

client = openai.OpenAI(api_key="API_KEY_HERE")

table_text = """
Process Step        Electricity (kWh)    Steam (ton)    Water (ton)
---------------------------------------------------------------------
Fermentation        706.2                1.3            5.5
Extraction          508.1                2.7            42.5
Pelleting           1162.5               0.04           -
"""

prompt = f"""
You are an assistant for life cycle inventory modeling.

Given the following table, extract each energy or material input flow used in the production of 1 metric ton of PHA. 

Return your answer as a JSON list where each item has the following fields:
- "flow": the name of the input (e.g., Electricity, Steam, Water)
- "amount": the numerical value
- "unit": the unit (e.g., kWh, ton)
- "process_step": the step of the process it belongs to (e.g., Fermentation)
- "assumption": include "From Table S5, 1 metric ton of PHA" for each

Here is the table:

{table_text}
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": prompt}
    ],
)

print(response.choices[0].message.content)
