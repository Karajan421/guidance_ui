import guidance
from collections import namedtuple
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import nest_asyncio

app = Flask(__name__)
CORS(app)

# Apply the nest_asyncio patch at the start of your script.
nest_asyncio.apply()

@app.route('/run_script', methods=['POST'])
@cross_origin()

def run_script():
    data = request.get_json()

    question = data.get('question')
    context = data.get('context')
        
        # set the default language model used to execute guidance programs
    guidance.llm = guidance.llms.TextGenerationWebUI()
    guidance.llm.caching = False


    # define a guidance program that adapts a proverb
    program = guidance("""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.### Instruction:
    You are a librarian AI who uses document information to answer questions. Documents as formatted as follows: [(Document(page_content="<important context>", metadata='source': '<source>'), <rating>)] where <important context> is the context, <source> is the source, and <rating> is the rating. 
    Strictly use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: what you should do to answer the question, should a search in Context
    Action Input: the input to the action, should be a question.
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    For examples:
    Question: How old is CEO of Microsoft wife?
    Thought: First, I need to find who is the CEO of Microsoft.
    Action: Searching through [(Document(page_content='Satya Nadella is the CEO of Microsoft Corporation. He took over as CEO in February 2014, succeeding Steve Ballmer.', metadata={'source': '/home/user/Documents/microsoft_info.txt'}), 0.95), (Document(page_content='Microsoft, the Redmond-based tech giant, is led by CEO Satya Nadella, who assumed the role in 2014.', metadata={'source': '/home/user/Documents/tech_leaders.txt'}), 0.91), (Document(page_content='The chief executive officer of Microsoft Corporation is Satya Nadella. Nadella took the helm in 2014 after Steve Ballmer stepped down.', metadata={'source': '/home/user/Documents/business_leaders.txt'}), 0.93)]
    Action Input: Who is the CEO of Microsoft?
    Observation: Satya Nadella is the CEO of Microsoft.
    Thought: Now, I should find out Satya Nadella's wife.
    Action: Searching through [(Document(page_content='Satya Nadella, the CEO of Microsoft, is married to Anu Nadella. They have been married since 1992.', metadata={'source': '/home/user/Documents/microsoft_info.txt'}), 0.96),(Document(page_content='Anu Nadella is the wife of Microsoft CEO, Satya Nadella. They have been together for many years.', metadata={'source': '/home/user/Documents/tech_leaders_families.txt'}), 0.94),(Document(page_content='The wife of Satya Nadella, chief executive officer of Microsoft Corporation, is Anu Nadella. They tied the knot in 1992.', metadata={'source': '/home/user/Documents/business_leaders_families.txt'}), 0.95)]
    Observation: Satya Nadella's wife's name is Anupama Nadella.
    Action Input: Who is Satya Nadella's wife?
    Thought: Then, I need to check Anupama Nadella's age.
    Action: Searching through [(Document(page_content='Anu Nadella, wife of Microsoft CEO Satya Nadella, is 38 years old.', metadata={'source': '/home/user/Documents/microsoft_info.txt'}), 0.96),(Document(page_content='38-year-old Anu Nadella is married to Satya Nadella, the CEO of Microsoft.', metadata={'source': '/home/user/Documents/tech_leaders_families.txt'}), 0.94), (Document(page_content='Anu Nadella, spouse of Satya Nadella, Microsoft Corporation's CEO, is currently 38 years old.', metadata={'source': '/home/user/Documents/business_leaders_families.txt'}), 0.95)]
    Action Input: How old is Anupama Nadella?
    Thought: I now know the final answer.
    Final Answer: Anupama Nadella is 38 years old.

    ### Input:
    {{question}}

    ### Response:
    Question: {{question}}
    Thought: {{gen 'thought' stop='\\n'}}
    Action: {{context}}
    Observation: {{gen 'thought2' stop='\\n'}}
    Action Input: {{gen 'actInput' stop='\\n'}}
    Thought: {{gen 'thought3' stop='\\n'}}
    Final Answer: {{gen 'final' stop='\\n'}}
    ,)""")

    executed_program = program(
    question="What is the office location?",
    context="[(Document(page_content='## 🔑\xa0Entrer\n\nPour ouvrir la première porte, appuyer sur le bouton rond. En dehors des horaires de travail, taper le code : **5A92**.\n\nOuvrir la seconde porte avec le badge ou **sonner à World Game**.\n\n**Troisième étage**.\n\n## 💬\xa0Message d’infos pour un extérieur\n\nLes bureaux se trouvent au 78 rue de Provence 75009 Paris.\n\nPour ouvrir la première porte, appuyer sur le bouton rond. Puis, sonner à World Game.\n\nNous sommes au 3e étage (les seuls sur le palier). Vous pouvez sonner.\n\n## 📡\xa0Wifi', metadata={'source': '/home/karajan/Documents/wg_notion.txt'}), 0.6865357160568237), (Document(page_content='à World Game**.\n\n**Troisième étage**.\n\n## 💬\xa0Message d’infos pour un extérieur\n\nLes bureaux se trouvent au 78 rue de Provence 75009 Paris.\n\nPour ouvrir la première porte, appuyer sur le bouton rond. Puis, sonner à World Game.\n\nNous sommes au 3e étage (les seuls sur le palier). Vous pouvez sonner.\n\n## 📡\xa0Wifi\n\nRéseau : Livebox-3B00\n\nCode : 9Dg34Xfthne3bnWhX6\n\n## 👩\u200d💻\xa0Les utiliser\n\nLes salariés du World Game habitant à Paris sont attendus au moins 3 jours par semaine au bureau (voir [Manuel du salarié World', metadata={'source': '/home/karajan/labzone/textgen/BrainChulo/data/uploads/wg_notion.txt'}), 0.6865357160568237), (Document(page_content='Bureaux Opéra\n\n**Sous-pages :**\n\n[Règles du jeu bureaux Opéra](Re%CC%80gles%20du%20jeu%20bureaux%20Ope%CC%81ra%209159ac0ccb9740f5b721faca8896832e.md)\n\n## 📍S’y rendre\n\nAdresse : **78 rue de Provence 75009 Paris**\n\nMétros : Trinité d’Estienne d’Orves ; Chaussée d’Antin Lafayette ; Opéra.\n\n## 🔑\xa0Entrer\n\nPour ouvrir la première porte, appuyer sur le bouton rond. En dehors des horaires de travail, taper le code : **5A92**.\n\nOuvrir la seconde porte avec le badge ou **sonner à World Game**.\n\n**Troisième', metadata={'source': '/home/karajan/labzone/textgen/BrainChulo/data/uploads/wg_notion.txt'}), 0.7134025692939758)]"
,   async_mode=False
)
    print(executed_program)
    # You can return the result as JSON
    return str({'result': executed_program})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


print("\n\nProgram Result:")
print(executed_program)
