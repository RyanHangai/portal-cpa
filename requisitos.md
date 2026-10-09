# Requisitos Funcionais - Portal CPA

## 1. Controle de Acesso e Autenticação
* **RF01 - Sistema de Autenticação:** O sistema deve possuir uma funcionalidade de login que identifique e direcione o usuário de acordo com o seu perfil de acesso.
* **RF02 - Sistema de Recuperação de Senha:** Um usuário deve recuperar a senha, para isso o usuário precisa acionar quem estiver um acesso superior ao dele.
* **RF03 - Gestão de Perfis:** O sistema deve suportar os seguintes níveis de acesso: Aluno, Professor, Coordenador, Diretor, Administrativo e CPA Externo. Para criar um usuário de qualquer níve, precisa ser feito pelo usuário com nível de acesso de "Administrativo", "Diretor" ou "Coordenador".
* **RF04 - Gestão de Cursos e Aulas:** O sistema deve permitir a criação, atualização e exclusão de cursos, temas de aulas, carga horária e dias de aula. Quem pode gerir esta parte é apenas o Coordenador (restrito ao curso que ele coordena), Administrativo e Diretor. 

## 2. Visualização de Dashboards e Relatórios
* **RF05 - Exibição Personalizada de Dashboards:** O portal deve exibir na página inicial os dashboards (Google Data Studio) baseados estritamente no perfil do usuário logado:
  * **Aluno:** Acesso exclusivo aos relatórios e pesquisas de alunos.
  * **Professor:** Acesso aos relatórios referentes ao corpo administrativo, aos professores e aos alunos.
  * **Coordenador e Diretor:** Acesso a todos os relatórios (pesquisas da CPA, avaliação docente e egressos), sem acesso à base de dados.
  * **Administrativo:** Acesso definido conforme a regra de negócio da área (a definir, mas restrito em relação à diretoria).
  * **CPA Externo (Avaliadores):** Acesso total a todos os relatórios institucionais.
* **RF06 - Acesso Exclusivo à Base de Dados:** O sistema deve garantir que apenas usuários logados com o perfil "Diretor" e "Administrativo" consigam visualizar e acessar a base de dados bruta do projeto.
* **RF07 - Área de Planejamento e Sugestões:** Todas alterações de cursos, aulas, temas de aula e carga horário, vão vir para uma área especifica antes de ser implementado, nesta área ocorrerá o planejamento, permissão, sugestões, modificações e execução. Precisa ocorrer um voto unánime dos CPAs Fixos para que seja implementado e implandado as mudanças.

## 3. Funcionalidades Públicas e Institucionais
* **RF08 - Mural de Devolutivas:** O portal deve possuir uma página pública onde serão publicadas as resoluções e as respostas das áreas em relação às demandas identificadas nas pesquisas da CPA.
* **RF09 - Área de Relatórios e Boletins:** O sistema deve incluir um repositório de arquivos para o armazenamento e consulta de documentos institucionais, como relatórios de autoavaliação e boletins informativos.
* **RF10 - Página de Contato:** O portal deve conter uma seção de contato com links de redirecionamento para o Google Chats e Google Meet, visando facilitar a comunicação da comunidade com a CPA.

# Requisitos Não Funcionais - Portal CPA

Abaixo estão os requisitos não funcionais (RNFs) que definem as restrições, padrões de qualidade, tecnologias e premissas de arquitetura do sistema:

## 1. Tecnologias e Arquitetura

* **RNF01 - Stack de Desenvolvimento Web:** O front-end e o back-end do portal devem ser desenvolvidos utilizando a linguagem **Python** em conjunto com a biblioteca **Streamlit**.
* **RNF02 - Banco de Dados:** O sistema deve utilizar o **PostgreSQL** como Sistema de Gerenciamento de Banco de Dados (SGBD) para garantir o armazenamento persistente e seguro das informações institucionais e acessos.
* **RNF03 - Visualização de Dados (BI):** A renderização de gráficos, resultados de pesquisas e relatórios dinâmicos na interface deve ser feita através da integração com painéis do **Google Data Studio**.

## 2. Segurança, Privacidade e Restrição de Acesso

* **RNF04 - Bloqueio de Acesso aos Dados Brutos:** A arquitetura do sistema e as permissões de infraestrutura devem garantir rigorosamente que usuários logados com perfis de liderança acadêmica (Coordenadores e Diretores) não tenham qualquer rota de acesso ao banco de dados bruto.
* **RNF05 - Permissão Técnica Exclusiva:** O acesso direto e técnico ao banco de dados relacional deve ser configurado para permitir acesso apenas aos membros do CPA Fixo (equipe executora e administrativa técnica).

## 3. Integrações de Terceiros e Usabilidade

* **RNF06 - Integração de Comunicação Externa:** O front-end da aplicação deve suportar hiperlinks estáveis e seguros na página de contato, garantindo o redirecionamento adequado dos usuários para instâncias do **Google Chats**
