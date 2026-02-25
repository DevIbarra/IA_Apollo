import os
import json
from dotenv import load_dotenv
from mistralai import Mistral

from App.Utils.Ferramenta import *
from App.Utils.Tools import TOOLS

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
MODEL = os.getenv("MISTRAL_CHAT_MODEL") or os.getenv("MISTRAL_CHAT_MODEL_SMALL")



# 🔹 Registro das funções
NAMES_TO_FUNCTIONS = {
    "set_conta_tool": set_conta_tool,
    "get_valor_total_contas_tool": get_valor_total_contas_tool,
    "get_contas_detalhada_tool": get_contas_detalhada_tool,
    "remove_conta_tool": remove_conta_tool,
    "altera_conta_tool": altera_conta_tool
}


# 🔹 Roteador de tool call
def run_tool_call(tool_call):
    fn_name = tool_call.function.name
    args = tool_call.function.arguments

    if isinstance(args, str):
        args = json.loads(args)

    if fn_name not in NAMES_TO_FUNCTIONS:
        raise ValueError(f"Tool desconhecida: {fn_name}")

    return NAMES_TO_FUNCTIONS[fn_name](**args)


# 🔹 Função principal da IA
def chamar_agente_llm(history: list, texto_usuario: str) -> str:
    # 1) adiciona user
    history.append({"role": "user", "content": texto_usuario})

    # 2) primeira chamada (com tools)
    response = client.chat.complete(
        model=MODEL,
        messages=history,
        tools=TOOLS,
        tool_choice="auto",
    )

    msg = response.choices[0].message

    # 3) se vier tool_calls
    tool_calls = getattr(msg, "tool_calls", None)
    if tool_calls:
        # IMPORTANTE: guardar a mensagem do assistant que pediu as tools no history
        history.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments,
                    },
                }
                for call in tool_calls
            ],
        })

        # 4) executar tools e adicionar resultados com tool_call_id
        for call in tool_calls:
            result = run_tool_call(call)  # salva no banco aqui

            history.append({
                "role": "tool",
                "tool_call_id": call.id,          
                "name": call.function.name,
                "content": json.dumps({"ok": True, "result": result}, ensure_ascii=False),
            })

        # 5) segunda chamada: agora o modelo responde “normal”, seguindo seu RAG
        response2 = client.chat.complete(
            model=MODEL,
            messages=history,
        )

        final_msg = response2.choices[0].message
        history.append({"role": "assistant", "content": final_msg.content})
        return final_msg.content

    # sem tool call: resposta normal
    history.append({"role": "assistant", "content": msg.content})
    return msg.content