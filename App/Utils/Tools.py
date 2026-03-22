TOOLS = [
  {
    "type": "function",
    "function": {
      "name": "set_conta_tool",
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
      "name": "get_valor_total_contas_tool",
      "description": "Retorna o total gasto no mês atual.",
      "parameters": {
        "type": "object",
        "additionalProperties": False,
        "properties": {},
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "get_contas_detalhada_tool",
      "description": "Lista detalhada dos gastos do mês atual da tabela valor_gasto.",
      "parameters": {
        "type": "object",
        "properties": {
          "limite": {
            "type": "integer",
            "description": "Quantidade máxima de itens retornados.",
            "default": 200
          }
        },
        "required": []
      }
    }
  },
    {
      "type": "function",
      "function": {
          "name": "remove_conta_tool",
          "description": "Remove um registro da tabela valor_gasto pelo id.",
          "parameters": {
              "type": "object",
              "properties": {
                  "id": {
                      "type": "integer",
                      "description": "ID do registro em valor_gasto que será removido."
                  }
              },
              "required": ["id"]
          }
      }
  },
    {
    "type": "function",
    "function": {
      "name": "altera_conta_tool",
      "description": "Atualiza um gasto/conta existente no banco. Pode atualizar valor e/ou descricao. Só altera campos enviados.",
      "parameters": {
        "type": "object",
        "properties": {
          "id": {"type": "integer", "description": "ID do registro a ser atualizado"},
          "valor": {"type": "number", "description": "Novo valor (opcional)"},
          "descricao": {"type": "string", "description": "Nova descrição (opcional)"}
        },
        "required": ["id"]
      }
    }
  },
    {
    "type": "function",
    "function": {
      "name": "agenda_evento_tool",
      "description": "Cria um evento na tabela agenda (data, descrição e horário).",
      "parameters": {
        "type": "object",
        "properties": {
          "data": {
            "type": "string",
            "description": "Data no formato YYYY-MM-DD (ex: 2026-02-27)."
          },
          "descricao": {
            "type": "string",
            "description": "Descrição do evento."
          },
          "horario": {
            "type": "string",
            "description": "Horário no formato HH:MM ou HH:MM:SS (ex: 14:30)."
          }
        },
        "required": ["data", "descricao", "horario"]
      }
    }
  },
    {
    "type": "function",
    "function": {
      "name": "data_atual_tool",
      "description": "Retorna a data e hora atual no fuso America/Sao_Paulo.",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  },
    {
      "type": "function",
      "function": {
        "name": "todo_compromissos_tool",
        "description": "Retorna todos os compromissos da agenda a partir de uma data específica. Se nenhuma data for informada, usa a data atual.",
        "parameters": {
          "type": "object",
          "additionalProperties": False,
          "properties": {
            "data": {
              "type": "string",
              "format": "date",
              "description": "Data base no formato YYYY-MM-DD. Se não for enviada, usar a data atual."
            }
          },
          "required": []
        }
      }
    }
]