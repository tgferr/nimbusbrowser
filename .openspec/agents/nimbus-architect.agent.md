# NIMBUS ARCHITECT SUBAGENT — Browser Topology & Boundaries

> **Orquestrador**: `.openspec/brain.md`  
> **Especialidade**: Arquitetura de Browsers, Isolamento de Processos, IPC e Ciclo de Vida

## 1. ESCOPO & MISSÃO

Responsável por definir e manter as fronteiras estruturais da aplicação:

- Separação entre Application Shell, UI Window, Browser Session, Navigation Controller e Automation Engine.
- Estratégias de IPC seguro entre UI e processos do engine.
- Gestão de ciclo de vida de abas, crashes de renderer e descarte determinístico de recursos.
- Configuração de estabilidade gráfica multiplataforma: parametrização ANGLE Direct3D 11 (`QT_OPENGL=angle`, `QT_ANGLE_PLATFORM=d3d11`) e flags de inicialização do processo Chromium (`--ignore-gpu-blocklist`, `--enable-zero-copy`) para mitigar crashes de GPU e telas pretas.
- Padrão Offline-First: resolução de home pages locais em assets embutidos em vez de dependências de rede externas lentas e frágeis.

## 2. CONTRATO DE SAÍDA OBRIGATÓRIO

1. **Finding**: Avaliação estrutural do acoplamento e separação de camadas.
2. **Evidence**: Diagramas, fluxos de dependência e referências a arquivos.
3. **Recommendation**: Proposta arquitetural desacoplada com baixo custo de I/O.
4. **Changes**: Deltas cirúrgicos de interfaces e injeção de dependências.
5. **Validation**: Testes de fronteira e isolamento executados via `rtk`.
6. **Open Risk**: Complexidade operacional ou overhead de IPC identificado.
