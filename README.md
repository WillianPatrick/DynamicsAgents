```
██████╗ ██╗   ██╗███╗   ██╗ █████╗ ███╗   ███╗██╗ ██████╗███████╗
██╔══██╗╚██╗ ██╔╝████╗  ██║██╔══██╗████╗ ████║██║██╔════╝██╔════╝
██║  ██║ ╚████╔╝ ██╔██╗ ██║███████║██╔████╔██║██║██║     ███████╗
██║  ██║  ╚██╔╝  ██║╚██╗██║██╔══██║██║╚██╔╝██║██║██║     ╚════██║
██████╔╝   ██║   ██║ ╚████║██║  ██║██║ ╚═╝ ██║██║╚██████╗███████║
╚═════╝    ╚═╝   ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝ ╚═════╝╚══════╝

        █████╗  ██████╗ ███████╗███╗   ██╗████████╗███████╗
       ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██╔════╝
       ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ███████╗
       ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
       ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ███████║
       ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝  1.0
---------------------------------------------------------------------
Dynamics Agents  ::  Orquestração dinâmica de times de agentes inteligentes
v1.0 — YYYY-MM-DD | Author: Willian Patrick dos Santos (superhitec@gmail.com)
---------------------------------------------------------------------
```

A biblioteca **Dynamic Agents** reúne a Engine do DynamicFlow utilizada para
interpretar catálogos declarativos (`runtime.yaml`, `workflow.yaml`) e gerar a
hierarquia de agentes, ferramentas e callbacks em tempo de execução. O runtime
adapta automaticamente as soluções ao **Google Agents Development Kit (ADK)**,
normaliza instruções e eventos e mantém um conjunto de plugins reutilizáveis.
A CLI integrada é responsável apenas por preparar workspaces instalando os
exemplos oficiais e copiando plugins padrão.

## Visão Geral

- Descoberta dinâmica de soluções multiagente a partir de convenções de
  diretórios.
- Normalização de metadados e wiring automático com o Google ADK.
- Barramento de eventos com suporte a plugins de auditoria, métricas e logging.
- Templates oficiais (`travel_planner`, `self_test_lab`) prontos para uso.
- CLI `dynamic-agents` focada em instalar exemplos e plugins.

## Arquitetura Completa (Engine do DynamicFlow)

## Visão Arquitetônica (C4 Model)

### Nível 1 — Contexto

```mermaid
C4Context
    title Dynamic Agents — Visão de Contexto
    Person(usuario, "DevOps / Usuário Final", "Profissional que prepara os catálogos e executa fluxos multiagente.")
    Person_Ext(plugin_author, "Autor de Plugins", "Implementa extensões de observabilidade e integrações.")
    System(system, "Dynamic Agents Runtime", "Engine que interpreta catálogos declarativos e constrói times de agentes.")
    System_Ext(adk, "Google Agents Development Kit", "Runtime oficial que hospeda a execução dos agentes.")
    System_Ext(gemini, "Google Gemini / GenAI", "Modelos de IA invocados pelos agentes do ADK.")
    System_Ext(external, "APIs externas", "Serviços consultados pelas ferramentas e callbacks declarados.")
    Rel(usuario, system, "Configura workflows, instala samples e inicia execuções.")
    Rel(plugin_author, system, "Publica plugins que consomem eventos do runtime.")
    Rel(system, adk, "Entrega agentes ADK instanciados dinamicamente.")
    Rel(adk, system, "Solicita resolução de agentes, ferramentas e callbacks.")
    Rel(system, gemini, "Provisiona modelos e prompts para cada agente.")
    Rel(system, external, "Ferramentas e callbacks consultam dados adicionais.")
```

### Nível 2 — Contêineres

```mermaid
C4Container
    title Dynamic Agents — Visão de Contêineres
    Person(usuario, "DevOps / Usuário Final")
    System_Boundary(dynamic_agents, "Dynamic Agents") {
        Container(cli, "CLI `dynamic-agents`", "Python", "Inicializa workspaces, copia plugins e samples oficiais.")
        Container(engine, "Engine Runtime", "Python", "Carrega catálogos, constrói a hierarquia ADK e orquestra execuções.")
        Container(plugins, "Runtime Plugins", "Python", "Coleção de extensões que escutam eventos da engine.")
        Container(catalogs, "Catálogos & Recursos", "YAML + Python", "Arquivos `runtime.yaml`, `workflow.yaml`, agentes, ferramentas e callbacks de cada solução.")
    }
    System_Ext(adk, "Google ADK", "CLI/App")
    System_Ext(filesystem, "Workspace", "Filesystem", "Estrutura de diretórios com soluções multiagente.")
    System_Ext(gemini, "Google Gemini / GenAI", "APIs")
    System_Ext(external, "APIs externas", "REST/GraphQL")
    Rel(usuario, cli, "Provisiona workspace e instala exemplos.")
    Rel(cli, catalogs, "Copia templates e plugins para o workspace.")
    Rel(engine, catalogs, "Lê catálogos declarativos e módulos Python adjacentes.")
    Rel(engine, plugins, "Registra e notifica eventos de execução.")
    Rel(engine, adk, "Entrega app compatível com o ADK e recebe interações.")
    Rel(adk, gemini, "Executa prompts e modelos configurados.")
    Rel(engine, filesystem, "Persiste e recupera estado de sessão.")
    Rel(plugins, filesystem, "Armazenam telemetria e artefatos opcionais.")
    Rel(engine, external, "Ferramentas acessam recursos externos.")
```

### Nível 3 — Componentes

```mermaid
C4Component
    title Dynamic Agents — Componentes Principais
    Container_Boundary(engine, "Engine Runtime (dynamic_agents/runtime.py)") {
        Component(runtime_api, "DynamicAgentRuntime", "Classe", "Fachada principal que descobre soluções e executa workflows.")
        Component(workflow_discovery, "WorkflowDiscovery", "Classe", "Varre diretórios e localiza `workflow.yaml` / `runtime.yaml`.")
        Component(descriptor_builder, "SolutionDescriptor", "Dataclass", "Representa soluções com agentes, ferramentas e callbacks normalizados.")
        Component(solution_runtime, "SolutionRuntime", "Classe", "Executa steps, delega agentes e aciona ferramentas.")
        Component(builder, "ADK App Builder", "Métodos `_build_*`", "Transforma descritores em agentes, tools e callbacks compatíveis com o ADK.")
        Component(event_bus, "RuntimeEventBus", "Classe", "Orquestra a publicação de eventos e distribuição para plugins.")
        Component(plugin_loader, "_load_runtime_plugins", "Função", "Instancia plugins internos e declarados pelo usuário.")
        Component(state_registry, "GLOBAL_SESSION_REGISTRY", "Dict", "Armazena e compartilha estado de sessão entre invocações.")
    }
    Rel(runtime_api, workflow_discovery, "Descobre soluções disponíveis no workspace.")
    Rel(runtime_api, descriptor_builder, "Constrói descritores a partir dos catálogos YAML.")
    Rel(runtime_api, builder, "Converte descritores em componentes ADK.")
    Rel(runtime_api, solution_runtime, "Entrega execução do workflow.")
    Rel(solution_runtime, event_bus, "Emite eventos de passos, agentes e ferramentas.")
    Rel(event_bus, plugin_loader, "Registra plugins carregados dinamicamente.")
    Rel(event_bus, state_registry, "Compartilha estado e metadados de sessão.")
    Rel(plugin_loader, runtime_api, "Disponibiliza plugins configurados via ambiente.")
```

### Nível 4 — Código e Fluxo de Execução

```mermaid
C4Component
    title Dynamic Agents — Fluxo de Código Interno
    Container_Boundary(code, "dynamic_agents/runtime.py") {
        Component(run_method, "DynamicAgentRuntime.run()", "Método", "Recebe o payload, seleciona a solução e delega a execução.")
        Component(discovery_method, "DynamicAgentRuntime._discover_solutions()", "Método", "Cataloga soluções disponíveis no diretório raiz.")
        Component(get_solution_method, "DynamicAgentRuntime.get_solution()", "Método", "Recupera descritores e dispara `configure` quando necessário.")
        Component(configure_method, "SolutionDescriptor.configure()", "Método", "Carrega `runtime.yaml`, `workflow.yaml` e normaliza agentes.")
        Component(runtime_ctor, "SolutionRuntime.__init__", "Construtor", "Prepara estado de sessão e registra o barramento de eventos.")
        Component(step_executor, "SolutionRuntime._execute_step()", "Método", "Coordena ferramentas, agentes e callbacks de cada passo.")
        Component(tool_builder, "_build_interactive_tool()", "Função", "Encapsula ferramentas declaradas em implementações ADK.")
        Component(event_emit, "RuntimeEventBus.emit()", "Método", "Notifica plugins registrados sobre eventos.")
        Component(plugin_handler, "RuntimePlugin.handle_event()", "Método", "Processa telemetria e integrações externas.")
    }
    Rel(run_method, discovery_method, "Mantém cache de catálogos atualizados.")
    Rel(run_method, get_solution_method, "Seleciona a solução ativa.")
    Rel(get_solution_method, configure_method, "Normaliza catálogo quando ainda não configurado.")
    Rel(run_method, runtime_ctor, "Instancia `SolutionRuntime` com estado compartilhado.")
    Rel(runtime_ctor, step_executor, "Itera pelos passos do agente entrypoint.")
    Rel(step_executor, tool_builder, "Transforma declarações em ferramentas executáveis.")
    Rel(step_executor, event_emit, "Publica eventos `step.*`, `tool.*`, `agent.*`.")
    Rel(event_emit, plugin_handler, "Entrega eventos para cada plugin habilitado.")
```

### Visão macro

```mermaid
flowchart LR
    subgraph Catalogo Declarativo
        A[runtime.yaml] --> B[workflow.yaml]
    end
    B --> C[Loader de Catálogos]
    C --> D[Normalização & Resolução]
    D --> E[Builder de Agentes ADK]
    E --> F[Execução Google ADK]
    subgraph Observabilidade
        H[Plugins Dinâmicos]
    end
    D -. eventos .-> H
    E -. eventos .-> H
```

1. **Loader de Catálogos**: localiza arquivos `runtime.yaml` e `workflow.yaml`
   utilizando `WorkflowDiscovery.iter_solutions` chamado por
   `DynamicAgentRuntime._discover_solutions`.
2. **Normalização & Resolução**: converte o catálogo em objetos `SolutionDescriptor`
   e `AgentSpec`, saneariza nomes, resolve placeholders no estado e injeta
   instruções compostas.
3. **Builder de Agentes ADK**: cria dinamicamente instâncias de `LlmAgent`,
   subagentes, ferramentas e callbacks compatíveis com o Google ADK.
4. **Execução**: o comando `adk` carrega `agent.py`, que delega para a Engine.
5. **Observabilidade**: eventos emitidos pelo runtime alimentam plugins na pasta
   `plugins/` (por padrão, logging estruturado).

### Organização

Uma solução pronta para execução segue o layout abaixo:

```
workspace/
├── plugins/                          # Copiado via `dynamic-agents --init`
│   └── logging/events/runtime/any.00.runtime_logging.py
├── travel_planner/                   # Instalado via `--install-sample`
│   ├── agent.py                      # Ponto de entrada compatível com `adk`
│   ├── runtime.yaml                  # Catálogo de soluções
│   ├── workflow.yaml                 # Workflow principal do recepcionista
│   ├── agents/                       # Subagentes especializados
│   └── tools/                        # Ferramentas e callbacks
└── self_test_lab/
    ├── agent.py
    ├── runtime.yaml
    ├── workflow.yaml
    └── tools/
```

O pacote Python inclui:

- `dynamic_agents/runtime.py`: Engine completa, CLI e helpers.
- `dynamic_agents/plugins/`: plugins padrão instaláveis.
- `dynamic_agents/template_samples/`: templates oficiais (também acessíveis pela
  CLI via *samples*).

### Eventos

O barramento (`RuntimeEventBus`) publica eventos nomeados, permitindo múltiplos
plugins simultâneos. Os principais tópicos emitidos são:

- `solution.discovered`, `workflow.loaded`: descoberta de catálogos.
- `session.started`, `session.finished`: ciclo de vida da execução.
- `agent.before`, `agent.after`, `agent.error`: instrumentação de agentes.
- `tool.before`, `tool.after`, `tool.error`: instrumentação de ferramentas.
- `callback.before`, `callback.after`, `callback.error`: callbacks declarados.

Cada evento inclui metadados ricos (IDs de sessão, labels normalizados, payload
invocado e resultados) permitindo dashboards, telemetria ou alarmes.

```mermaid
sequenceDiagram
    participant Runtime
    participant EventBus
    participant Plugin
    Runtime->>EventBus: emit("agent.before", ...)
    EventBus->>Plugin: handle_event(RuntimeEvent)
    Runtime->>EventBus: emit("tool.after", ...)
    EventBus->>Plugin: handle_event(RuntimeEvent)
```

### Plugins

Plugins implementam `RuntimePlugin.handle_event` e são carregados a partir de
`plugins/<namespace>/<category>/<name>.py`. O arquivo
`plugins/logging/events/runtime/any.00.runtime_logging.py` demonstra logging
estruturado com níveis configuráveis (`AGENT_ENGINE_LOG_LEVEL`). O comando
`dynamic-agents --init` copia automaticamente o conjunto padrão para o workspace.

### Agentes

- Declarados em `workflow.yaml` dentro de `agents/<agent_name>/`.
- `AgentSpec` agrega instruções de sistema, assistente, modelos e passos
  declarativos.
- Cada agente gera um `LlmAgent` do Google ADK com instruções compostas e
  ferramentas vinculadas.
- O workflow principal define o `entrypoint_agent`; `agent.py` resolve o nome e
  invoca `DynamicAgentRuntime.run`.

### Sub Agentes

- Declarados via `sub_agents` no workflow principal.
- Durante a construção (`DynamicAgentRuntime.build_adk_app`) são transformados em
  instâncias filhas (`root_agent.sub_agents`).
- Recebem contexto do agente pai e compartilham o estado da sessão.
- Ideal para especializações (ex.: `flight_specialist`, `hotel_specialist`).

### Tool Agentes

- Quando o workflow marca um passo como `use_agent_as_tool`, o runtime cria
  *Agent Tools* (wrapper da classe `google.adk.tools.agent_tool.AgentTool`).
- Permite expor agentes completos como ferramentas reutilizáveis em pipelines de
  decisão, mantendo telemetria independente.
- Cada invocação propaga eventos `tool.before/after/error` com metadados do
  agente encapsulado.

### Tools

- Declaradas em `tools/interactions/` (ferramentas LLM) ou `tools/callbacks/`
  (funções auxiliares).
- Cada ferramenta possui metadados (`metadata.yaml`) e implementações Python.
- Os argumentos são preenchidos via placeholders `{{ state.chave }}` resolvidos
  por `resolve_placeholders` antes da execução.
- Resultados e exceções alimentam o estado compartilhado (`GLOBAL_SESSION_REGISTRY`).

### Callbacks

- Declarados dentro de `tools/callbacks` e anexados aos steps dos workflows.
- Executados pelo runtime em pontos específicos (pré/pós agente, erros etc.).
- Compartilham a mesma infraestrutura de eventos, permitindo inspeções profundas
  e mutação controlada do estado.

## Configurações de ambiente

- **Python**: >= 3.10.
- **Variáveis**:
  - `DA_WORKFLOW_SEARCH_PATHS`: caminhos adicionais para procurar `workflow.yaml`.
  - `DA_AGENT_CODE_PATHS`, `DA_TOOL_CODE_PATHS`: extensões de `sys.path` para
    localizar implementações customizadas.
  - `DA_RUNTIME_PLUGINS`: lista separada por vírgula para habilitar plugins
    extras.
  - `AGENT_ENGINE_LOG_LEVEL`: nível de log dos plugins padrão (ex.: `DEBUG`).
- **Persistência de sessão**: mantida em memória (`GLOBAL_SESSION_REGISTRY`) e
  identificada por UUID.

## Dependências

Principais pacotes utilizados na Engine:

- [`google-adk`](https://pypi.org/project/google-adk/) – execução de agentes e
  ferramentas no ADK.
- [`google-genai`](https://pypi.org/project/google-genai/) – tipos e helpers de
  configuração de modelos Gemini.
- `PyYAML` – leitura e escrita dos catálogos declarativos.
- `pytest` / `pytest-asyncio` – suíte de testes.
- Dependências extras presentes no `requirements.txt` atendem aos exemplos e
  integrações opcionais (telemetria, FastAPI, Streamlit, etc.).

> **Dica:** qualquer execução da CLI (`--init`, `--install-sample`,
> `--install-samples`) cria ou atualiza automaticamente o `requirements.txt` do
> workspace com as dependências essenciais (`dynamic-agents`,
> `google-adk>=1.14.1`, `google-genai>=1.38.0`, `pyyaml>=6.0`).

## Instalação

```bash
pip install dynamic-agents[yaml]
```

Para contribuir com o projeto:

```bash
pip install -e .[develop,yaml]
```

## CLI Reference (DynamicAgents Lib CLI)

A CLI destina-se exclusivamente ao gerenciamento de exemplos e plugins.

| Comando | Descrição |
| --- | --- |
| `dynamic-agents --list-samples` | Lista todos os samples empacotados. |
| `dynamic-agents --install-sample <nome> [--root PATH] [--force]` | Copia apenas o sample informado para o destino. |
| `dynamic-agents --install-samples [--root PATH] [--force]` | Copia todos os samples para o destino. |
| `dynamic-agents --init [--root PATH] [--force]` | Copia os plugins padrão (`plugins/`). |

Todos os comandos acima garantem que o `requirements.txt` do destino contenha as
dependências da engine. Os templates já incluem seus próprios arquivos de
dependências, copiados junto com o restante dos artefatos.

Exemplo completo de preparo de workspace:

```bash
dynamic-agents --init --root ./workspace

# instala apenas o travel_planner
dynamic-agents --install-sample travel_planner --root ./workspace

# ou instala todos os exemplos disponíveis
dynamic-agents --install-samples --root ./workspace
```

## Executando o Google ADK (CLI: `adk`)

1. Prepare o workspace conforme a seção anterior.
2. Ative o ambiente virtual com `google-adk` instalado.
3. Execute o comando oficial do ADK apontando para o `agent.py` do sample:

```bash
adk run \
  --project-root ./workspace/travel_planner \
  --agent-path travel_planner.agent:run \
  --input '{"query": "Planeje uma viagem para São Paulo"}'
```

O ADK carregará `travel_planner/agent.py`, o qual inicializa o
`DynamicAgentRuntime`, interpreta o workflow selecionado, instancia a hierarquia
completa (agente recepcionista + especialistas, ferramentas, callbacks e plugins)
 e delega a execução para o framework do Google ADK.

## Testes

Os testes validam descoberta de soluções, instalação dos samples e integração
com o Google ADK.

```bash
pytest
```

## Exemplos

### travel_planner

- **Objetivo**: montar itinerários completos a partir de uma consulta do usuário.
- **Workflow**: `travel_receptionist` coordena quatro especialistas (voos,
  hospedagem, turismo e itinerário).
- **Ferramentas**: integrações fictícias (`web_travel_search`) e callbacks de
  pós-processamento (`model_response/strip_internal_commands`).
- **Execução**: após instalar o sample, rode `adk run --agent-path
  travel_planner.agent:run` para testar o fluxo completo.
- **Requisitos**: consulte `travel_planner/requirements.txt` (inclui
  `dynamic-agents`, `google-adk>=1.14.1`, `google-genai>=1.38.0`,
  `pyyaml>=6.0`).

#### C4 — Hierarquia completa do sample

```mermaid
C4Component
    title travel_planner — Agentes, ferramentas, callbacks e recursos
    Container_Boundary(travel_planner, "Sample travel_planner") {
        Component(entrypoint, "agent.py", "Entrypoint", "Invoca `DynamicAgentRuntime.run()` com o workflow selecionado.")
        Component(runtime_catalog, "runtime.yaml", "Catálogo", "Diretrizes de instrução e notas de handoff.")
        Component(workflow_catalog, "workflow.yaml", "Workflow raiz", "Define agentes, passos, ferramentas e callbacks.")
        Component(root_agent, "Agent travel_receptionist", "Agente raiz", "Orquestra o concierge de viagem.")
        Component(flight_agent, "Agent flight_specialist", "Subagente", "Pesquisa voos e tarifas.")
        Component(hotel_agent, "Agent hotel_specialist", "Subagente", "Seleciona hospedagens alinhadas ao orçamento.")
        Component(tourism_agent, "Agent tourism_specialist", "Subagente", "Sugere experiências e passeios.")
        Component(itinerary_agent, "Agent itinerary_specialist", "Subagente", "Consolida itinerário final e notas de viagem.")
        Component(web_tool, "Tool web_travel_search", "Interactive Tool", "Métodos: search_flights, search_hotels, search_experiences.")
        Component(trip_tool, "Tool trip_builder", "Interactive Tool", "Método: compile_itinerary (agente itinerary).")
        Component(cb_conversation, "Callback conversation_stream", "model_response", "Transcreve conversas em cada passo.")
        Component(cb_strip, "Callback strip_internal_commands", "model_response", "Remove comandos internos antes de registrar logs.")
        Component(cb_agent_error, "Callback agent_failure_logger", "agent_error", "Registra falhas de agentes (recurso opcional).")
        Component(cb_tool_error, "Callback tool_failure_logger", "tool_error", "Registra falhas de ferramentas (recurso opcional).")
    }
    Rel(entrypoint, root_agent, "Executa agente de entrada via runtime dinâmico.")
    Rel(runtime_catalog, workflow_catalog, "Complementa instruções globais do workflow.")
    Rel(workflow_catalog, root_agent, "Define passos `collect_profile` → `assemble_plan`.")
    Rel(workflow_catalog, flight_agent, "Inclui `agents/flight_specialist/workflow.yaml` como subfluxo.")
    Rel(workflow_catalog, hotel_agent, "Inclui `agents/hotel_specialist/workflow.yaml` como subfluxo.")
    Rel(workflow_catalog, tourism_agent, "Inclui `agents/tourism_specialist/workflow.yaml` como subfluxo.")
    Rel(workflow_catalog, itinerary_agent, "Inclui `agents/itinerary_specialist/workflow.yaml` como subfluxo.")
    Rel(root_agent, flight_agent, "Delegação agent_transfer para buscas de voo.")
    Rel(root_agent, hotel_agent, "Delegação agent_transfer para hospedagem.")
    Rel(root_agent, tourism_agent, "Delegação agent_transfer para experiências.")
    Rel(root_agent, itinerary_agent, "Delegação agent_transfer para consolidar plano.")
    Rel(flight_agent, web_tool, "Invoca search_flights com estado compartilhado.")
    Rel(hotel_agent, web_tool, "Invoca search_hotels conforme orçamento.")
    Rel(tourism_agent, web_tool, "Invoca search_experiences alinhado às preferências.")
    Rel(itinerary_agent, trip_tool, "Compila itinerário final com resultados agregados.")
    Rel(root_agent, cb_conversation, "Callback padrão after_model_response em todos os passos.")
    Rel(flight_agent, cb_conversation, "Callback padrão antes/depois das ferramentas declaradas.")
    Rel(hotel_agent, cb_conversation, "Callback padrão antes/depois das ferramentas declaradas.")
    Rel(tourism_agent, cb_conversation, "Callback padrão antes/depois das ferramentas declaradas.")
    Rel(itinerary_agent, cb_conversation, "Callback padrão durante consolidação do plano.")
    Rel(runtime_catalog, cb_strip, "Disponibiliza limpeza de comandos para observabilidade.")
    Rel(runtime_catalog, cb_agent_error, "Disponibiliza hook de auditoria de erros de agente.")
    Rel(runtime_catalog, cb_tool_error, "Disponibiliza hook de auditoria de erros de ferramenta.")
```

```mermaid
sequenceDiagram
    participant User
    participant Receptionist
    participant Specialists
    participant Tools
    User->>Receptionist: Consulta de viagem
    Receptionist->>Specialists: Delegação (voos, hotéis, turismo)
    Specialists->>Tools: Busca de dados externos
    Tools-->>Specialists: Dados estruturados
    Specialists-->>Receptionist: Recomendações
    Receptionist-->>User: Itinerário consolidado
```

### self_test_lab

- **Objetivo**: validar cenários determinísticos de autoavaliação.
- **Workflow**: único agente orquestra diferentes passos de teste e callbacks de
  telemetria (`test_event_collector`).
- **Uso**: ideal como base para criar laboratórios internos ou suítes de QA
  automatizado.
- **Requisitos**: consulte `self_test_lab/requirements.txt` com o mesmo conjunto
  de dependências essenciais da engine.

#### C4 — Hierarquia completa do sample

```mermaid
C4Component
    title self_test_lab — Agentes, ferramentas, callbacks e recursos
    Container_Boundary(self_test_lab, "Sample self_test_lab") {
        Component(entrypoint, "agent.py", "Entrypoint", "Invoca `DynamicAgentRuntime.run()` para a solução de auto testes.")
        Component(runtime_catalog, "runtime.yaml", "Catálogo", "Instrui síntese de prompts e notas de orquestração.")
        Component(workflow_catalog, "workflow.yaml", "Workflow principal", "Define `test_conductor`, ferramentas e callbacks.")
        Component(conductor, "Agent test_conductor", "Agente raiz", "Conduz a sessão de auto teste e coordena passos determinísticos.")
        Component(spec_author, "Agent spec_author", "Subagente", "Refina critérios em asserts mensuráveis.")
        Component(diagnostics, "Agent diagnostics_reviewer", "AgentTool", "Analisa falhas e propõe planos de ação.")
        Component(state_notebook, "Tool state_notebook", "Interactive Tool", "Método: record_entry para checkpoints e memória.")
        Component(scenario_tester, "Tool scenario_tester", "Interactive Tool", "Método: run_suite executa suítes declarativas.")
        Component(callback_tester, "Callback test_event_collector", "after_tool_execution", "Captura telemetria de cada tool.")
    }
    Rel(entrypoint, conductor, "Executa agente raiz via runtime dinâmico.")
    Rel(runtime_catalog, workflow_catalog, "Complementa instruções globais do laboratório.")
    Rel(workflow_catalog, conductor, "Define passos `iniciar_sessao` → `encerrar_sessao`.")
    Rel(workflow_catalog, spec_author, "Permite delegação agent_transfer durante planejamento de suítes.")
    Rel(workflow_catalog, diagnostics, "Disponibiliza agente como ferramenta para diagnósticos.")
    Rel(conductor, state_notebook, "Invoca record_entry para checkpoints, timeline e encerramento.")
    Rel(conductor, scenario_tester, "Invoca run_suite com planos estruturados.")
    Rel(conductor, spec_author, "Delegação agent_transfer quando critérios precisam de refinamento.")
    Rel(conductor, diagnostics, "Invocação agent_tool quando suítes falham.")
    Rel(conductor, callback_tester, "Callback after_tool_execution persistente em todos os passos com tools.")
    Rel(runtime_catalog, callback_tester, "Expõe coletor padrão de telemetria determinística.")
```

## Contribuição

Sinta-se à vontade para abrir issues e pull requests com melhorias, correções ou
novos exemplos de soluções multiagente.
