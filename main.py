# Importa a biblioteca para fazer requisições HTTP (para acessar a API)
import requests
import json # Para tratar melhor a visualização da resposta

# --- Algoritmo de Ordenação: Bubble Sort ---
#
# Como funciona?
# Ele percorre a lista várias vezes. Em cada passagem, ele compara pares de elementos
# adjacentes (o primeiro com o segundo, o segundo com o terceiro, etc.).
# Se um par estiver na ordem errada, ele os troca de lugar.
# Elementos "maiores" (ou "menores", dependendo da regra) "borbulham" para o final da lista.
# O processo se repete até que nenhuma troca seja necessária em uma passagem completa.
#
# Complexidade de Tempo:
# - Pior Caso e Caso Médio: O(n²) - "O de n ao quadrado".
#   Isso acontece porque, no pior caso, temos dois laços de repetição aninhados,
#   onde para cada elemento da lista (n), percorremos a lista quase inteira novamente (n).
# - Melhor Caso: O(n) - Se a lista já estiver ordenada, o algoritmo faz apenas uma
#   passagem para verificar e não realiza trocas.

def bubble_sort_por_repositorios(lista_usuarios):
    """
    Ordena uma lista de usuários do GitHub com base no número de repositórios públicos.
    Usa o algoritmo Bubble Sort.
    """
    # n é o número de usuários na lista
    n = len(lista_usuarios)

    # O primeiro laço (i) controla o número de passagens pela lista.
    # A cada passagem, o maior elemento já estará na sua posição final,
    # por isso o `n-1`.
    for i in range(n - 1):
        # O segundo laço (j) faz as comparações entre elementos adjacentes.
        # O `n-i-1` é uma otimização: a cada passagem `i`, o `i`-ésimo maior elemento
        # já está no lugar certo, então não precisamos compará-lo de novo.
        trocou = False
        for j in range(0, n - i - 1):
            # Acessamos o dicionário de cada usuário e pegamos o valor da chave 'public_repos'
            repos_usuario_atual = lista_usuarios[j]['public_repos']
            repos_proximo_usuario = lista_usuarios[j + 1]['public_repos']

            # Comparamos! Se o atual tem mais repositórios que o próximo, trocamos eles de lugar.
            # (Para ordenar de forma crescente, mude o sinal para >)
            if repos_usuario_atual < repos_proximo_usuario:
                # A troca de lugar em Python é muito simples
                lista_usuarios[j], lista_usuarios[j + 1] = lista_usuarios[j + 1], lista_usuarios[j]
                trocou = True
        
        # Otimização: se em uma passagem inteira nenhuma troca foi feita, a lista já está ordenada.
        if not trocou:
            break
            
    return lista_usuarios


# --- Função Principal para Executar a Tarefa ---
def main():
    """
    Função principal que consome a API e apresenta os dados.
    """
    print("Consumindo a API do GitHub para buscar usuários...")
    api_url = "https://api.github.com/users"
    
    try:
        # Faz a requisição GET para a URL da API
        response = requests.get(api_url)
        
        # Verifica se a requisição foi bem-sucedida (código 200 significa OK)
        response.raise_for_status()

        # Converte a resposta (que está em formato JSON) para uma lista de dicionários em Python
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