"""
Script Principal de Auditoria
Executa todos os testes e gera relatório consolidado
"""
import subprocess
import sys
from datetime import datetime

def run_test(test_file, test_name):
    """Executa um teste e retorna o resultado"""
    print(f"\n{'='*80}")
    print(f"Executando: {test_name}")
    print(f"{'='*80}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        
        if result.stderr:
            print("ERROS:")
            print(result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"❌ TIMEOUT: O teste {test_name} demorou mais de 30 segundos")
        return False
    except Exception as e:
        print(f"❌ ERRO ao executar {test_name}: {e}")
        return False

def main():
    """Executa todos os testes de auditoria"""
    
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "AUDITORIA COMPLETA DO BI" + " "*35 + "║")
    print("║" + " "*15 + "Sistema de Vendas de Veículos" + " "*34 + "║")
    print("╚" + "="*78 + "╝")
    print(f"\n📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🖥️  Python: {sys.version.split()[0]}")
    print("\n" + "="*80)
    
    # Lista de testes
    testes = [
        ("audit/test_database_structure.py", "TESTE 1: Estrutura do Banco de Dados"),
        ("audit/test_queries.py", "TESTE 2: Queries e Cálculos"),
        ("audit/test_requirements.py", "TESTE 3: Conformidade com Requisitos"),
    ]
    
    resultados = {}
    
    # Executar cada teste
    for test_file, test_name in testes:
        sucesso = run_test(test_file, test_name)
        resultados[test_name] = sucesso
    
    # Relatório final
    print("\n\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*25 + "RELATÓRIO FINAL" + " "*38 + "║")
    print("╚" + "="*78 + "╝")
    print()
    
    total_testes = len(resultados)
    testes_passaram = sum(1 for passou in resultados.values() if passou)
    
    for test_name, passou in resultados.items():
        status = "✅ PASSOU" if passou else "❌ FALHOU"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*80)
    print(f"\n📊 RESUMO: {testes_passaram}/{total_testes} testes passaram")
    print(f"📈 Taxa de Sucesso: {(testes_passaram/total_testes*100):.1f}%")
    
    if testes_passaram == total_testes:
        print("\n🎉 PARABÉNS! Todos os testes passaram!")
        print("✅ O sistema BI está em conformidade com todos os requisitos.")
        print("\n📋 Próximos passos:")
        print("   1. Revisar o relatório em audit/AUDIT_REPORT.md")
        print("   2. Verificar exemplos em audit/examples.md")
        print("   3. Preparar DER (Diagrama Entidade-Relacionamento)")
        return_code = 0
    elif testes_passaram >= total_testes * 0.7:
        print("\n⚠️  ATENÇÃO: Maioria dos testes passaram, mas há pendências.")
        print("📝 Revisar os testes que falharam e corrigir os problemas.")
        return_code = 1
    else:
        print("\n❌ PROBLEMAS GRAVES DETECTADOS!")
        print("🔧 É necessário revisar e corrigir os erros antes de continuar.")
        return_code = 2
    
    print("\n" + "="*80)
    print(f"📁 Relatórios disponíveis em: ./audit/")
    print(f"📄 Relatório principal: audit/AUDIT_REPORT.md")
    print("="*80 + "\n")
    
    return return_code

if __name__ == "__main__":
    sys.exit(main())
