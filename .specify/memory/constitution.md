<!--
  Sync Impact Report
  Version change: (nenhuma - criação inicial) -> 1.0.0
  Modified principles: nenhuma (constituição criada do zero)
  Added sections: Core Principles, Regras de Estilo e Comunicação,
    Qualidade e Revisão, Governance
  Removed sections: nenhuma
  Follow-up TODOs: nenhum
-->

# Portal CPA Constitution

## Core Principles

### I. Legibilidade acima de concisão
O código é escrito para seres humanos. Funções e algoritmos devem priorizar a
clareza, mesmo que isso signifique mais linhas ou passos explícitos. Soluções
compactas ou "inteligentes" só são aceitas quando não reduzem a legibilidade.

### II. Nomes descritivos e autoexplicativos
Variáveis, funções, classes e módulos devem revelar a intenção pelo próprio nome.
Evitar abreviações, siglas obscuras e nomes genéricos como "data", "info" ou "tmp".

### III. Uma responsabilidade por função
Cada função e cada algoritmo deve executar uma única tarefa de forma clara.
Preferir funções menores e bem nomeadas a blocos longos e difíceis de acompanhar.

### IV. Fluxo de controle explícito e previsível
Preferir estruturas simples e explícitas. Evitar truques, aninhamento profundo,
efeitos colaterais escondidos e expressões que exijam esforço extra para entender.

### V. Consistência e padrões do projeto
Seguir as convenções já adotadas no projeto. Código consistente é mais previsível,
mais fácil de revisar e mais barato de manter.

## Regras de Estilo e Comunicação

- É proibido o uso de emojis em qualquer artefato do projeto: código, comentários,
  mensagens de commit, documentação, interface e logs.
- Comentários devem explicar o "porquê", não repetir o "o quê" que o código já mostra.
- Manter formatação consistente (indentação, espaçamento e quebra de linha) para
  facilitar a leitura.

## Qualidade e Revisão

- Toda alteração deve manter ou melhorar a legibilidade do código.
- Revisões de código devem priorizar clareza, nomes e estrutura antes de
  micro-otimizações.
- Complexidade desnecessária deve ser justificada; soluções simples e legíveis são
  preferidas.
- Em caso de conflito entre brevidade e legibilidade, a legibilidade prevalece.

## Governance

Esta Constituição tem precedência sobre preferências individuais. Alterações exigem
proposta documentada e aprovação, seguindo versionamento semântico (MAJOR.MINOR.PATCH).
Toda revisão deve verificar a conformidade com os princípios acima.

**Version**: 1.0.0 | **Ratified**: 2026-11-04 | **Last Amended**: 2026-11-04
