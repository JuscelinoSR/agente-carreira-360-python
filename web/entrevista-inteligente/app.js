const questions = [
  {
    id: "identidade",
    text: "Para começar, qual é seu nome, cidade e objetivo profissional hoje?",
    field: "identidade",
  },
  {
    id: "experiencia_formal",
    text: "Conte sobre seus trabalhos registrados: cargos, empresas, atividades e resultados importantes.",
    field: "experienciasFormais",
    categories: ["trabalho registrado", "atendimento ao público", "organização de equipes", "resolução de problemas"],
  },
  {
    id: "experiencia_informal",
    text: "Agora me fale sobre experiências informais: projetos pessoais, trabalhos extras, freelas ou iniciativas próprias.",
    field: "experienciasInformais",
    categories: ["projetos pessoais", "liderança informal", "comunicação", "resolução de problemas"],
  },
  {
    id: "igreja_voluntariado",
    text: "Você participa de igreja, eventos ou voluntariado? Descreva funções como operação de som, organização, apoio a equipes ou liderança.",
    field: "igrejaVoluntariado",
    categories: ["igreja", "eventos", "voluntariado", "operação de som", "organização de equipes", "liderança informal"],
  },
  {
    id: "habilidades",
    text: "Quais habilidades você percebe que usa bem? Pode citar comunicação, atendimento, análise, liderança, tecnologia, som, vendas ou planejamento.",
    field: "habilidadesDeclaradas",
    categories: ["comunicação", "atendimento ao público", "liderança informal", "organização de equipes"],
  },
  {
    id: "resultados",
    text: "Quais resultados, conquistas ou melhorias você já gerou? Exemplos: redução de erros, aumento de produtividade, organização de processos ou satisfação do cliente.",
    field: "resultados",
    categories: ["resolução de problemas", "organização de equipes", "comunicação"],
  },
];

const skillDictionary = [
  { skill: "Atendimento ao público", terms: ["cliente", "clientes", "atendimento", "público", "suporte"] },
  { skill: "Comunicação", terms: ["comunicação", "explicar", "orientar", "apresentar", "script", "conversa"] },
  { skill: "Liderança informal", terms: ["lider", "liderança", "coordenei", "organizei", "equipe", "times"] },
  { skill: "Organização de equipes", terms: ["escala", "rota", "roteirização", "organização", "planejamento", "distribuição"] },
  { skill: "Resolução de problemas", terms: ["problema", "resolvi", "melhoria", "corrigir", "erro", "redução", "otimização"] },
  { skill: "Operação de som", terms: ["som", "mesa", "áudio", "microfone", "igreja", "evento", "mixagem"] },
  { skill: "Análise de dados", terms: ["dados", "indicadores", "kpi", "planilha", "análise", "relatório"] },
  { skill: "Vendas e negociação", terms: ["vendas", "comercial", "negociação", "cliente", "proposta"] },
  { skill: "Gestão operacional", terms: ["operação", "processo", "campo", "produtividade", "equipe"] },
  { skill: "Tecnologia e automação", terms: ["python", "github", "codex", "automação", "ia", "sistema"] },
];

const experienceTypes = [
  "trabalho registrado",
  "projetos pessoais",
  "igreja",
  "eventos",
  "voluntariado",
  "liderança informal",
  "atendimento ao público",
  "operação de som",
  "organização de equipes",
  "comunicação",
  "resolução de problemas",
];

const state = {
  currentQuestion: 0,
  answers: {},
  skills: new Set(),
  experiences: new Set(),
  manualSummary: "",
};

const chatMessages = document.querySelector("#chatMessages");
const chatForm = document.querySelector("#chatForm");
const userAnswer = document.querySelector("#userAnswer");
const skipButton = document.querySelector("#skipButton");
const progressValue = document.querySelector("#progressValue");
const progressBar = document.querySelector("#progressBar");
const answeredCount = document.querySelector("#answeredCount");
const skillsList = document.querySelector("#skillsList");
const experienceList = document.querySelector("#experienceList");
const profilePreview = document.querySelector("#profilePreview");
const generateResumeButton = document.querySelector("#generateResumeButton");
const manualEditButton = document.querySelector("#manualEditButton");
const manualEditor = document.querySelector("#manualEditor");
const manualSummary = document.querySelector("#manualSummary");
const saveManualButton = document.querySelector("#saveManualButton");

function normalize(text) {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function addMessage(role, text) {
  const message = document.createElement("div");
  message.className = `message ${role}`;
  message.textContent = text;
  chatMessages.appendChild(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function askCurrentQuestion() {
  const question = questions[state.currentQuestion];

  if (!question) {
    addMessage("assistant", "Entrevista concluída. Você já pode revisar o resumo, editar manualmente ou gerar o currículo.");
    userAnswer.disabled = true;
    skipButton.disabled = true;
    chatForm.querySelector("button[type='submit']").disabled = true;
    updateSummary();
    return;
  }

  addMessage("assistant", question.text);
}

function extractSkills(answer) {
  const normalizedAnswer = normalize(answer);

  skillDictionary.forEach(({ skill, terms }) => {
    const found = terms.some((term) => normalizedAnswer.includes(normalize(term)));
    if (found) state.skills.add(skill);
  });
}

function extractExperiences(answer, question) {
  const normalizedAnswer = normalize(answer);

  experienceTypes.forEach((type) => {
    if (normalizedAnswer.includes(normalize(type))) {
      state.experiences.add(type);
    }
  });

  if (question.categories) {
    question.categories.forEach((category) => state.experiences.add(category));
  }
}

function buildProfileSummary() {
  if (state.manualSummary) return state.manualSummary;

  const identidade = state.answers.identidade || "Profissional em desenvolvimento";
  const formal = state.answers.experienciasFormais || "experiências formais ainda não detalhadas";
  const informal = state.answers.experienciasInformais || "experiências informais e projetos pessoais em construção";
  const igreja = state.answers.igrejaVoluntariado || "vivências comunitárias, eventos ou voluntariado ainda não detalhadas";
  const resultados = state.answers.resultados || "resultados e conquistas em processo de mapeamento";

  return `${identidade}\n\nResumo inicial: profissional com vivências formais e informais, incluindo ${formal}. Também apresenta experiências complementares em ${informal} e participação em ${igreja}. Demonstra potencial para comunicação, organização, atendimento, liderança informal e resolução de problemas. Resultados citados: ${resultados}.`;
}

function renderTags(container, values, emptyText) {
  container.innerHTML = "";
  const items = Array.from(values).filter(Boolean);

  if (!items.length) {
    const item = document.createElement("li");
    item.textContent = emptyText;
    container.appendChild(item);
    return;
  }

  items.forEach((value) => {
    const item = document.createElement("li");
    item.textContent = value;
    container.appendChild(item);
  });
}

function updateSummary() {
  const answered = Object.values(state.answers).filter(Boolean).length;
  const progress = Math.round((answered / questions.length) * 100);

  progressValue.textContent = `${progress}%`;
  progressBar.style.width = `${progress}%`;
  answeredCount.textContent = `${answered} resposta${answered === 1 ? "" : "s"}`;

  renderTags(experienceList, state.experiences, "Aguardando experiências");
  renderTags(skillsList, state.skills, "Aguardando habilidades");

  profilePreview.textContent = buildProfileSummary();
  localStorage.setItem("agenteCarreira360Entrevista", JSON.stringify({
    currentQuestion: state.currentQuestion,
    answers: state.answers,
    skills: Array.from(state.skills),
    experiences: Array.from(state.experiences),
    manualSummary: state.manualSummary,
  }));
}

function handleAnswer(answer) {
  const question = questions[state.currentQuestion];

  if (!question) return;

  const cleanAnswer = answer.trim();

  if (cleanAnswer) {
    state.answers[question.field] = cleanAnswer;
    addMessage("user", cleanAnswer);
    extractSkills(cleanAnswer);
    extractExperiences(cleanAnswer, question);
  } else {
    addMessage("user", "Pular esta pergunta por enquanto.");
  }

  state.currentQuestion += 1;
  updateSummary();
  askCurrentQuestion();
}

function generateResumeMarkdown() {
  const skills = Array.from(state.skills);
  const experiences = Array.from(state.experiences);

  return `# Currículo gerado pelo Agente Carreira 360\n\n## Resumo profissional\n\n${buildProfileSummary()}\n\n## Experiências mapeadas\n\n${experiences.length ? experiences.map((item) => `- ${item}`).join("\n") : "- [PREENCHER]"}\n\n## Habilidades extraídas\n\n${skills.length ? skills.map((item) => `- ${item}`).join("\n") : "- [PREENCHER]"}\n\n## Respostas da entrevista\n\n${questions.map((question) => `### ${question.text}\n\n${state.answers[question.field] || "[PREENCHER]"}`).join("\n\n")}\n`;
}

function downloadMarkdown(filename, content) {
  const blob = new Blob([content], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function restoreState() {
  const raw = localStorage.getItem("agenteCarreira360Entrevista");
  if (!raw) return;

  try {
    const saved = JSON.parse(raw);
    state.currentQuestion = Math.min(saved.currentQuestion || 0, questions.length);
    state.answers = saved.answers || {};
    state.skills = new Set(saved.skills || []);
    state.experiences = new Set(saved.experiences || []);
    state.manualSummary = saved.manualSummary || "";
  } catch {
    localStorage.removeItem("agenteCarreira360Entrevista");
  }
}

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  handleAnswer(userAnswer.value);
  userAnswer.value = "";
  userAnswer.focus();
});

skipButton.addEventListener("click", () => handleAnswer(""));

generateResumeButton.addEventListener("click", () => {
  const markdown = generateResumeMarkdown();
  downloadMarkdown("curriculo-entrevista-inteligente.md", markdown);
});

manualEditButton.addEventListener("click", () => {
  manualEditor.hidden = !manualEditor.hidden;
  manualSummary.value = buildProfileSummary();
  if (!manualEditor.hidden) manualSummary.focus();
});

saveManualButton.addEventListener("click", () => {
  state.manualSummary = manualSummary.value.trim();
  updateSummary();
  manualEditor.hidden = true;
});

restoreState();
updateSummary();
addMessage("assistant", "Olá! Eu sou o assistente da Entrevista Inteligente. Vou fazer perguntas guiadas para montar seu perfil profissional de forma simples e mobile-first.");
askCurrentQuestion();
