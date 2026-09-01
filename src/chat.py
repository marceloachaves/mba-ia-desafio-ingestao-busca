from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from search import search_prompt

load_dotenv()


def get_llm_response(prompt):
    try:
        llm = ChatOpenAI(
            model="gpt-5-nano",
            temperature=0.5
        )

        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"❌ Erro ao chamar LLM: {str(e)}")
        return None


def main():
    print("=== RAG Chat ===")
    print("Digite 'sair' para encerrar o programa.\n")
    
    while True:
        question = input("Digite sua pergunta (considerando apenas os dados do banco): ").strip()

        if question.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o programa...")
            break

        if not question:
            print("Nenhuma pergunta fornecida. Tente novamente.\n")
            continue

        print("\n🔍 Buscando documentos similares...")
        out = search_prompt(question)

        if not out or not out.get("results"):
            print("❌ Não foi possível obter resultados. Verifique se o banco está populado.\n")
            continue

        results = out["results"]
        
        if not results:
            print("❌ Nenhum documento encontrado com similaridade.\n")
            continue

        print("💬 Enviando para o LLM...")
        prompt = out["prompt"]
        response = get_llm_response(prompt)

        if response:
            print("\n== 🤖 Resposta do LLM ==")
            print(response)
        else:
            print("❌ Não foi possível obter resposta do LLM.")
        
        print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    main()