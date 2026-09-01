PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""
from dotenv import load_dotenv
from langchain_postgres import PGVector
from ingest import generate_embeddings, CONNECTION

load_dotenv()


def search_prompt(question):
  if not question or not isinstance(question, str):
    print("Pergunta inválida.")
    return None

  try:
    embeddings = generate_embeddings()

    vector_store = PGVector(
      embeddings=embeddings,
      collection_name="documents",
      connection=CONNECTION,
      use_jsonb=True,
    )

    results = vector_store.similarity_search_with_score(question, k=10)

    if not results:
      print(f"⚠️  Nenhum documento encontrado para: '{question}'")
      return None

    print(f"✓ Encontrados {len(results)} documentos similares.")

    contexts = []
    for doc, score in results:
      text = getattr(doc, "page_content", str(doc))
      contexts.append(f"SCORE: {score}\n{text}")

    contexto = "\n\n---\n\n".join(contexts)

    prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)

    return {"prompt": prompt, "results": results}
  
  except Exception as e:
    print(f"❌ Erro ao buscar documentos: {str(e)}")
    return None