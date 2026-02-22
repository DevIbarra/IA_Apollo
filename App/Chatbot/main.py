import os
from dotenv import load_dotenv
from App.Chatbot.RAG_TEMPLATE import Rag_template
from App.Query.Querys import salvar_msg
from App.Chatbot.IA_LLM import chamar_agente_llm

load_dotenv()

history = [
    {"role": "system", "content": Rag_template.strip()}
]

def main():
    print("======= Apollo =======")
    print("Digite 'sair' para encerrar.\n")

    while True:
        try:
            texto = input("Você: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando Atendimento...")
            break

        if not texto:
            continue

        if texto.lower() in ("sair", "exit", "quit"):
            print("Apollo: Até a proxima meu rei!")
            break

        salvar_msg("usuario", texto)

        resposta = chamar_agente_llm(history, texto)
        history.append({"role": "assistant", "content": resposta})
        print(f"Apollo: {resposta}\n")

        salvar_msg("apollo", resposta)

if __name__ == "__main__":
    main()