import requests
import json


def bubble_sort_por_repositorios(lista_usuarios):
    """
    Ordena uma lista de usuários do GitHub com base no número de repositórios públicos.
    Usa o algoritmo Bubble Sort.
    """
    n = len(lista_usuarios)

    # O primeiro laço (i) controla o número de passagens pela lista.
    # A cada passagem, o maior elemento já estará na sua posição final,
    # por isso o n-1.
    for i in range(n - 1):
        # O segundo laço (j) faz as comparações entre elementos adjacentes.
        # O n-i-1 é uma otimização: a cada passagem i, o i-ésimo maior elemento
        # já está no lugar certo, então não precisamos compará-lo de novo.
        trocou = False
        for j in range(0, n - i - 1):
            # Acessamos o dicionário de cada usuário e pegamos o valor da chave 'public_repos'
            repos_usuario_atual = lista_usuarios[j]['public_repos']
            repos_proximo_usuario = lista_usuarios[j + 1]['public_repos']

            # Comparamos se o atual tem mais repositórios que o próximo, trocamos eles de lugar.
            if repos_usuario_atual < repos_proximo_usuario:
                lista_usuarios[j], lista_usuarios[j + 1] = lista_usuarios[j + 1], lista_usuarios[j]
                trocou = True
                
        if not trocou:
            break
            
    return lista_usuarios


#Função Principal para Executar a Tarefa
def main():
    """
    Função principal que consome a API e apresenta os dados.
    """
    print("Consumindo a API do GitHub para buscar usuários...")
    api_url = "https://api.github.com/users"
    
    try:
        # Faz a requisição GET para a URL da API
        response = requests.get(api_url)
        
        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()

        # Converte a resposta (JSON) para uma lista de dicionários em Python
        usuarios = response.json()
        
        # Filtra para pegar apenas os campos que nos interessam para simplificar a visualização
        # A API retorna muitos dados, vamos pegar só login, id e o número de repositórios
        usuarios_simplificados = []
        for user in usuarios:
            # A API /users às vezes não retorna todos os detalhes.
            # Vamos pegar os detalhes de cada um para garantir que temos o 'public_repos'.
            detalhes_response = requests.get(user['url'])
            detalhes_response.raise_for_status()
            detalhes_usuario = detalhes_response.json()

            # Verificamos se a chave 'public_repos' existe no retorno
            if 'public_repos' in detalhes_usuario:
                usuarios_simplificados.append({
                    'login': detalhes_usuario['login'],
                    'id': detalhes_usuario['id'],
                    'public_repos': detalhes_usuario['public_repos']
                })
        
        print(f"\nEncontrados {len(usuarios_simplificados)} usuários. Ordenando por número de repositórios públicos (do maior para o menor)...")

        # Chama a nossa função de ordenação
        usuarios_ordenados = bubble_sort_por_repositorios(usuarios_simplificados)
        
        print("\n--- Resultado da Ordenação ---")
        # Apresenta o resultado de forma legível
        for usuario in usuarios_ordenados:
            print(f"Usuário: {usuario['login']:<20} | Repositórios Públicos: {usuario['public_repos']}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao acessar a API: {e}")

# Executa a função principal quando o script é rodado
if __name__ == "__main__":
    main()
