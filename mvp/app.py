from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def executar_script(nome_script, *argumentos, interativo=False):
    caminho = ROOT / "scripts" / nome_script
    if not caminho.exists():
        print(f"Script não encontrado: {caminho}")
        return 1

    if interativo:
        resultado = subprocess.run(
            [sys.executable, str(caminho), *argumentos],
            cwd=str(caminho.parent),
        )
        return resultado.returncode

    resultado = subprocess.run(
        [sys.executable, str(caminho), *argumentos],
        cwd=str(caminho.parent),
        capture_output=True,
        text=True
    )

    if resultado.stdout:
        print(resultado.stdout)

    if resultado.stderr:
        print("Erros:")
        print(resultado.stderr)

    return resultado.returncode


def menu():
    while True:
        print("\n=== Agente Carreira 360 — Python MVP ===")
        print("1. Gerar currículo")
        print("2. Gerar resumo para LinkedIn")
        print("3. Gerar posts da semana")
        print("4. Gerar mensagens de networking")
        print("5. Analisar vaga")
        print("6. Gerar tudo")
        print("7. Adicionar novo curso")
        print("8. Adicionar nova formação")
        print("9. Adicionar nova conquista")
        print("10. Adicionar nova experiência")
        print("11. Adicionar nova competência")
        print("12. Atualizar resumo do GitHub")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            executar_script("gerar_curriculo.py")
        elif opcao == "2":
            executar_script("gerar_linkedin.py")
        elif opcao == "3":
            executar_script("gerar_posts.py")
        elif opcao == "4":
            executar_script("gerar_networking.py")
        elif opcao == "5":
            executar_script("analisar_vaga.py")
        elif opcao == "6":
            executar_script("gerar_curriculo.py")
            executar_script("gerar_linkedin.py")
            executar_script("gerar_posts.py")
            executar_script("gerar_networking.py")
            executar_script("analisar_vaga.py")
        elif opcao == "7":
            executar_script("adicionar_dados.py", "curso", interativo=True)
        elif opcao == "8":
            executar_script("adicionar_dados.py", "formacao", interativo=True)
        elif opcao == "9":
            executar_script("adicionar_dados.py", "conquista", interativo=True)
        elif opcao == "10":
            executar_script("adicionar_dados.py", "experiencia", interativo=True)
        elif opcao == "11":
            executar_script("adicionar_dados.py", "competencia", interativo=True)
        elif opcao == "12":
            executar_script("analisar_github.py")
        elif opcao == "0":
            print("Encerrando o Agente Carreira 360.")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
