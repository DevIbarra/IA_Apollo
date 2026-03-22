import os
import json
from dotenv import load_dotenv
from mistralai import Mistral

from App.Utils.Ferramenta import *
from App.Utils.Tools import TOOLS

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
MODEL = os.getenv("MISTRAL_CHAT_MODEL") or os.getenv("MISTRAL_CHAT_MODEL_SMALL")


NAMES_TO_FUNCTIONS = {
    "set_conta_tool": set_conta_tool,
    "get_valor_total_contas_tool": get_valor_total_contas_tool,
    "get_contas_detalhada_tool": get_contas_detalhada_tool,
    "remove_conta_tool": remove_conta_tool,
    "altera_conta_tool": altera_conta_tool,
    "agenda_evento_tool": agenda_evento_tool,
    "data_atual_tool": data_atual_tool,
    "todo_compromissos_tool": todo_compromissos_tool,
}


def run_tool_call(tool_call):
    fn_name = tool_call.function.name
    args = tool_call.function.arguments

    if isinstance(args, str):
        args = json.loads(args)

    if fn_name not in NAMES_TO_FUNCTIONS:
        raise ValueError(f"Tool desconhecida: {fn_name}")

    return NAMES_TO_FUNCTIONS[fn_name](**args)


def chamar_agente_llm(history: list, texto_usuario: str) -> str:
    history.append({"role": "user", "content": texto_usuario})

    temperature = float(os.getenv("TEMPERATURE", "0.7"))

    max_iterations = 10

    for _ in range(max_iterations):
        response = client.chat.complete(
            model=MODEL,
            messages=history,
            tools=TOOLS,
            tool_choice="auto",
            temperature=temperature
        )

        msg = response.choices[0].message
        tool_calls = getattr(msg, "tool_calls", None)

        # Se não houver tool call, é resposta final
        if not tool_calls:
            content = msg.content or ""
            history.append({"role": "assistant", "content": content})
            return content

        # registra mensagem do assistant chamando tool
        history.append({
            "role": "assistant",
            "content": msg.content if msg.content is not None else None,
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

        # executa cada tool chamada
        for call in tool_calls:
            result = run_tool_call(call)

            tool_content = (
                result
                if isinstance(result, str)
                else json.dumps(result, ensure_ascii=False, default=str)
            )

            history.append({
                "role": "tool",
                "tool_call_id": call.id,
                "name": call.function.name,
                "content": tool_content,
            })

    # fallback caso entre em loop
    fallback = "Não consegui concluir sua solicitação agora."
    history.append({"role": "assistant", "content": fallback})
    return fallback