import os

def gerar_arvore():
    # Conjunto de pastas e arquivos a serem ignorados
    exclude = {'.git', 'node_modules', 'dist', 'build', '__pycache__', '.venv', '__init__.py'}

    for root, dirs, files in os.walk('.'):
        # 1. Filtra as pastas in-place para o os.walk não entrar nelas
        dirs[:] = [d for d in dirs if d not in exclude]
        
        # 2. Filtra a lista de arquivos
        files = [f for f in files if f not in exclude and not f.endswith('.pyc')]
        
        # Calcula o nível de indentação atual
        level = root.replace('.', '', 1).count(os.sep)
        indent = '│   ' * level
        
        # Exibe o nome da pasta atual (se não for a raiz '.')
        if root != '.':
            print(f'{indent}├── {os.path.basename(root)}/')
        
        # Subindentação para os arquivos dentro desta pasta
        subindent = '│   ' * (level + 1)
        num_arquivos = len(files)
        
        # 3. Exibe os arquivos com a formatação correta de ramificação
        for i, f in enumerate(files):
            # Se for o último arquivo da lista, usa └──, se não, usa ├──
            conector = '└── ' if i == num_arquivos - 1 else '├── '
            print(f'{subindent}{conector}{f}')

if __name__ == '__main__':
    # Avisa onde o script está rodando
    print(f"Estrutura de diretórios para: {os.path.abspath('.')}\n")
    gerar_arvore()