TOOLS = [
  {
    "type": "function",
    "function": {
      "name": "get_conta_tool",
      "description": "Salva um gasto/conta no banco de dados.",
      "parameters": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
          "valor": {"type": "number", "description": "Valor numérico do gasto. Ex: 125.50"},
          "descricao": {"type": "string", "description": "Descrição curta do gasto.", "minLength": 1}
        },
        "required": ["valor", "descricao"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "get_todas_contas_tool",
      "description": "Retorna o total gasto no mês atual.",
      "parameters": {
        "type": "object",
        "additionalProperties": False,
        "properties": {},
        "required": []
      }
    }
  }
]