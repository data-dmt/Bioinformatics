const $ = id => document.getElementById(id);

let simulationData = null;
let translationSteps = [];
let selectedCodon = 0;

const player = {
  activeStage: 'replication',
  playing: false,
  timer: null,
  speed: 1,
  progress: { replication: 0, transcription: 0, translation: 0 },
  options: { showLabels: true, showEnzymes: true, showBonds: true, narration: true }
};

function el(tag, text = '', className = '') {
  const node = document.createElement(tag);
  node.textContent = text;
  if (className) node.className = className;
  return node;
}

function setText(id, value) {
  const node = $(id);
  if (node) node.textContent = value;
}

function cleanSequence() {
  return $('sequence').value.replace(/\s/g, '').toUpperCase();
}

function updateCount() {
  const length = cleanSequence().length;
  setText('base-count', `${length} ${length === 1 ? 'base' : 'bases'}`);
}

$('sequence').addEventListener('input', updateCount);

for (const button of document.querySelectorAll('[data-sequence]')) {
  button.addEventListener('click', () => {
    $('sequence').value = button.dataset.sequence;
    updateCount();
    $('form').requestSubmit();
  });
}

function showError(message) {
  setText('error', message);
  $('error').hidden = false;
  setText('announcement', `Error: ${message}`);
}

function renderOverview(data) {
  const profile = data.dna.profile;
  const t = data.translation;
  const items = [
    [profile.length, 'bases de ADN'],
    [`${profile.gc_percent}%`, 'contenido GC'],
    [profile.hydrogen_bonds, 'puentes H estimados'],
    [data.replication.lagging_strand.okazaki_fragments.length, 'fragmentos Okazaki'],
    [t.protein_length, 'aminoácidos']
  ];

  $('overview').replaceChildren();
  for (const [value, label] of items) {
    const card = el('div', '', 'metric');
    card.append(el('strong', String(value)), el('span', label));
    $('overview').append(card);
  }
}

function renderTimeline(containerId, steps) {
  const container = $(containerId);
  container.replaceChildren();
  for (const step of steps ?? []) {
    const card = el('article', '', 'timeline-step');
    const number = el('div', String(step.number).padStart(2, '0'), 'timeline-number');
    const body = document.createElement('div');
    body.append(
      el('h4', step.title),
      el('p', step.actor, 'timeline-actor'),
      el('p', step.description),
      el('div', `Resultado: ${step.result}`, 'timeline-result')
    );
    card.append(number, body);
    container.append(card);
  }
}

function renderMachinery(containerId, machinery) {
  const container = $(containerId);
  container.replaceChildren();
  for (const item of machinery ?? []) {
    const card = el('article', '', 'machinery-card');
    const top = el('div', '', 'machinery-top');
    const title = document.createElement('div');
    title.append(el('h4', item.name), el('small', item.type));
    top.append(
      title,
      el('span', item.modeled ? 'REPRESENTADO' : 'CONTEXTO', `model-badge ${item.modeled ? 'modeled' : 'context'}`)
    );
    card.append(top, el('p', item.function));
    container.append(card);
  }
}

function renderReplication(data) {
  const r = data.replication;
  setText(
    'leading',
    `Molde: 3′ ${r.leading_strand.template_aligned_3_5} 5′\nNueva: 5′ ${r.leading_strand.new_strand_5_3} 3′`
  );
  setText(
    'lagging',
    `Molde: 5′ ${r.lagging_strand.template_5_3} 3′\nNueva: 3′ ${r.lagging_strand.new_strand_aligned_3_5} 5′`
  );

  $('fragments').replaceChildren();
  for (const fragment of r.lagging_strand.okazaki_fragments) {
    const card = el('article', '', 'fragment-card');
    card.append(
      el('strong', `Fragmento ${fragment.number}`),
      el('small', `molde ${fragment.template_start}–${fragment.template_end}`),
      el('code', `Molde: 5′ ${fragment.template_sequence_5_3} 3′`),
      el('code', `Nuevo: 5′ ${fragment.sequence_5_3} 3′`)
    );
    $('fragments').append(card);
  }

  $('daughters').replaceChildren();
  [r.molecule_1, r.molecule_2].forEach((molecule, index) => {
    const card = el('article', '', 'sequence-card');
    card.append(
      el('h4', `Molécula hija ${index + 1}`),
      el('pre', `5′ ${molecule.top_aligned_5_3} 3′ [${molecule.top_origin}]\n3′ ${molecule.bottom_aligned_3_5} 5′ [${molecule.bottom_origin}]`)
    );
    $('daughters').append(card);
  });

  renderTimeline('replication-steps', r.steps);
  renderMachinery('replication-machinery', r.machinery);

  $('replication-models').replaceChildren();
  for (const model of r.models) {
    const card = el('article', '', `model-card ${model.name === 'Semiconservativo' ? 'selected-model' : ''}`);
    card.append(el('h4', model.name), el('p', model.description));
    $('replication-models').append(card);
  }
  setText('replication-evidence', r.evidence);
}

function renderTranscription(data) {
  const t = data.transcription;
  setText(
    'rna',
    `ADN codificante: 5′ ${t.coding_5_3} 3′\n` +
    `ADN molde:       3′ ${t.template_aligned_3_5} 5′\n` +
    `Pre-ARNm:        5′ ${t.pre_mrna_5_3} 3′\n` +
    `ARNm utilizado:  5′ ${t.mrna_for_translation_5_3} 3′`
  );

  renderTimeline('transcription-steps', t.steps);
  renderMachinery('transcription-machinery', t.machinery);

  $('rna-processing').replaceChildren();
  for (const item of t.rna_processing) {
    const card = el('article');
    card.append(el('h4', item.name), el('p', item.description));
    $('rna-processing').append(card);
  }

  $('intron-exon').replaceChildren();
  for (const [title, text] of [
    ['Intrones', t.intron_exon_context.introns],
    ['Exones', t.intron_exon_context.exons]
  ]) {
    const block = document.createElement('div');
    block.append(el('h4', title), el('p', text));
    $('intron-exon').append(block);
  }

  $('rna-types').replaceChildren();
  for (const item of t.rna_types) {
    const card = el('article');
    card.append(el('h4', `${item.name} · ${item.full_name}`), el('p', item.description));
    $('rna-types').append(card);
  }
}

function renderReading(step) {
  $('reading').replaceChildren();
  if (!step) {
    $('reading').append(
      el('strong', 'No se encontró AUG.'),
      el('p', 'El modelo no inicia la traducción y no se sintetiza una cadena polipeptídica.')
    );
    return;
  }

  const stop = step.type === 'STOP';
  $('reading').append(el('strong', `${step.codon} → ${stop ? 'STOP' : step.amino_acid.name}`));
  const grid = el('div', '', 'reading-grid');
  const values = [
    ['Codón', `5′ ${step.codon} 3′`],
    ['Posición', `${step.mrna_start_1_based}–${step.mrna_end_1_based}`],
    [stop ? 'Reconocimiento' : 'Anticodón', stop ? 'Factor de terminación' : `3′ ${step.anticodon_3_5} 5′`],
    [stop ? 'Efecto' : 'Aminoácido', stop ? 'Finaliza la traducción' : `${step.amino_acid.name} (${step.amino_acid.abbreviation})`],
    ['Cadena acumulada', step.peptide_after_step || '—']
  ];
  for (const [label, value] of values) {
    const block = document.createElement('div');
    block.append(el('small', label), el('span', value));
    grid.append(block);
  }
  $('reading').append(grid);

  if (stop) {
    $('reading').append(el('p', 'Los codones STOP no incorporan aminoácidos; señalan la terminación de la síntesis.'));
  } else if (step.role === 'start') {
    $('reading').append(el('p', 'AUG establece el inicio del marco de lectura en este modelo y codifica metionina.'));
  } else {
    $('reading').append(el('p', 'El ARNt reconoce el codón mediante su anticodón y aporta el aminoácido correspondiente.'));
  }
}

function highlightProtein(step) {
  for (const node of $('protein').querySelectorAll('.amino')) node.classList.remove('current');
  if (!step || step.type === 'STOP') return;
  const node = $('protein').querySelector(`[data-codon-number="${step.codon_number}"]`);
  if (node) node.classList.add('current');
}

function selectCodon(index, scroll = false, syncPlayer = true) {
  if (!translationSteps.length) {
    selectedCodon = 0;
    setText('step-label', 'SIN INICIO');
    $('previous').disabled = true;
    $('next').disabled = true;
    renderReading(null);
    highlightProtein(null);
    if (syncPlayer) player.progress.translation = 0;
    if (player.activeStage === 'translation') renderActiveStage();
    return;
  }

  index = Math.max(0, Math.min(index, translationSteps.length - 1));
  selectedCodon = index;
  const step = translationSteps[index];
  setText('step-label', `CODÓN ${index + 1} / ${translationSteps.length}`);
  $('previous').disabled = index === 0;
  $('next').disabled = index === translationSteps.length - 1;

  const buttons = $('codons').querySelectorAll('.codon');
  buttons.forEach((button, i) => button.setAttribute('aria-pressed', i === index ? 'true' : 'false'));
  if (scroll && buttons[index]) buttons[index].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });

  renderReading(step);
  highlightProtein(step);
  if (syncPlayer) {
    player.progress.translation = index + 1;
    if (player.activeStage === 'translation') renderActiveStage();
  }
}

$('previous').addEventListener('click', () => selectCodon(selectedCodon - 1, true));
$('next').addEventListener('click', () => selectCodon(selectedCodon + 1, true));

function renderTranslation(data) {
  const t = data.translation;
  translationSteps = t.translation_steps;
  selectedCodon = 0;
  $('codons').replaceChildren();
  $('translation-rows').replaceChildren();
  $('protein').replaceChildren();

  for (const [index, step] of translationSteps.entries()) {
    const button = el('button', step.codon, 'codon');
    button.type = 'button';
    button.setAttribute('aria-pressed', 'false');
    button.setAttribute('aria-label', `Codón ${index + 1}: ${step.codon}`);
    button.addEventListener('click', () => selectCodon(index));
    $('codons').append(button);

    const row = document.createElement('tr');
    const values = [
      step.codon_number,
      `${step.mrna_start_1_based}–${step.mrna_end_1_based}`,
      `5′ ${step.codon} 3′`,
      step.type === 'STOP' ? '—' : `3′ ${step.anticodon_3_5} 5′`,
      step.type === 'STOP' ? 'STOP' : `${step.amino_acid.name} (${step.amino_acid.abbreviation})`,
      step.peptide_after_step || '—'
    ];
    for (const value of values) row.append(el('td', String(value)));
    $('translation-rows').append(row);

    if (step.amino_acid) {
      if ($('protein').querySelector('.amino')) $('protein').append(el('span', '—', 'bond'));
      const amino = el('span', step.amino_acid.abbreviation, 'amino');
      amino.title = step.amino_acid.name;
      amino.dataset.codonNumber = String(step.codon_number);
      $('protein').append(amino);
    }
  }

  if (!t.protein_length) $('protein').append(el('span', 'No se ha sintetizado una cadena.'));

  if (t.completed) setText('protein-title', 'Cadena polipeptídica liberada');
  else if (t.status === 'no_start') setText('protein-title', 'Sin síntesis');
  else setText('protein-title', 'Cadena polipeptídica parcial');

  const lines = [];
  if (t.completed) {
    lines.push(`La traducción termina en ${t.stop_codon}, a partir de la base ${t.stop_position_1_based} del ARNm.`);
    lines.push(`Se incorporaron ${t.protein_length} ${t.protein_length === 1 ? 'aminoácido' : 'aminoácidos'}.`);
  } else if (t.status === 'no_start') {
    lines.push('No se encontró AUG. En este modelo no comienza la traducción.');
  } else {
    lines.push('El ARNm termina sin un STOP en el marco de lectura; la cadena se considera parcial.');
  }
  if (t.sequence_before_start && t.status !== 'no_start') lines.push(`Región anterior al primer AUG: ${t.sequence_before_start}.`);
  if (t.incomplete_codon) lines.push(`Bases finales que no forman un codón completo: ${t.incomplete_codon}.`);
  if (t.untranslated_after_stop) lines.push(`Región posterior al STOP no traducida: ${t.untranslated_after_stop}.`);
  setText('status', lines.join('\n'));

  renderTimeline('translation-steps', t.steps);
  renderMachinery('translation-machinery', t.machinery);

  if (translationSteps.length) selectCodon(0, false, false);
  else selectCodon(0, false, false);
}

function renderAssumptions(data) {
  $('model-assumptions').replaceChildren();
  for (const assumption of data.model_assumptions ?? []) $('model-assumptions').append(el('li', assumption));
}

function stageMax(stage) {
  if (!simulationData) return 0;
  if (stage === 'replication') return simulationData.dna.coding_5_3.length;
  if (stage === 'transcription') return simulationData.transcription.pre_mrna_5_3.length;
  if (stage === 'translation') return Math.max(translationSteps.length, 1);
  return 0;
}

function stageFraction(stage) {
  const max = stageMax(stage);
  return max ? Math.min(1, player.progress[stage] / max) : 0;
}

function currentTheoryStep(stage) {
  if (!simulationData) return null;
  const steps = simulationData[stage].steps;
  const fraction = stageFraction(stage);
  if (!steps.length) return null;
  if (fraction <= 0) return null;
  const index = Math.min(steps.length - 1, Math.max(0, Math.ceil(fraction * steps.length) - 1));
  return steps[index];
}

function renderNarration(stage) {
  const card = $(`${stage}-narration`);
  if (!card) return;
  card.hidden = !player.options.narration;
  const workbench = card.closest('.workbench');
  if (workbench) workbench.classList.toggle('no-narration', !player.options.narration);
  if (!player.options.narration) return;

  card.replaceChildren();
  card.append(el('span', player.playing ? 'EN REPRODUCCIÓN' : 'EXPLICACIÓN', 'live-tag'));

  if (stage === 'translation') {
    if (!translationSteps.length) {
      card.append(el('span', 'TRADUCCIÓN', 'narration-step'), el('h4', 'No se encontró AUG'), el('p', 'La secuencia no contiene un codón de inicio que active este modelo de traducción.'));
      return;
    }
    const progress = player.progress.translation;
    if (progress <= 0) {
      card.append(el('span', 'ANTES DE EMPEZAR', 'narration-step'), el('h4', 'Ribosoma preparado'), el('p', 'Pulsa Reproducir o Paso para recorrer los codones desde el primer AUG.'));
      return;
    }
    const step = translationSteps[Math.min(progress - 1, translationSteps.length - 1)];
    card.append(el('span', `CODÓN ${step.codon_number}`, 'narration-step'));
    if (step.type === 'STOP') {
      card.append(
        el('h4', `${step.codon} · señal STOP`),
        el('p', 'No existe un ARNt que incorpore un aminoácido. Los factores de terminación finalizan la síntesis y permiten liberar el polipéptido.'),
        el('div', `Cadena final: ${step.peptide_after_step || '—'}`, 'narration-result')
      );
    } else {
      card.append(
        el('h4', `${step.codon} → ${step.amino_acid.name}`),
        el('p', `El ARNt con anticodón ${step.anticodon_3_5} reconoce el codón de forma complementaria y aporta ${step.amino_acid.name.toLowerCase()}.`),
        el('div', `Cadena acumulada: ${step.peptide_after_step}`, 'narration-result')
      );
    }
    return;
  }

  const theory = currentTheoryStep(stage);
  if (!theory) {
    const title = stage === 'replication' ? 'Horquilla preparada' : 'ADN preparado para transcribirse';
    const text = stage === 'replication'
      ? 'Pulsa Reproducir o Paso para ver cómo avanza la horquilla y se construyen las nuevas hebras.'
      : 'Pulsa Reproducir o Paso para seguir el avance de la ARN polimerasa y el crecimiento del transcrito.';
    card.append(el('span', 'ANTES DE EMPEZAR', 'narration-step'), el('h4', title), el('p', text));
    return;
  }

  card.append(
    el('span', `PASO ${theory.number}`, 'narration-step'),
    el('h4', theory.title),
    el('p', theory.description),
    el('div', theory.result, 'narration-result')
  );
}

function renderActiveStage() {
  if (!simulationData) return;
  const stage = player.activeStage;
  const options = player.options;

  if (stage === 'replication') {
    renderReplicationDiagram(simulationData, { ...options, progress: stageFraction(stage) });
  } else if (stage === 'transcription') {
    renderTranscriptionDiagram(simulationData, { ...options, progress: stageFraction(stage) });
  } else {
    const p = player.progress.translation;
    const step = p > 0 && translationSteps.length
      ? translationSteps[Math.min(p - 1, translationSteps.length - 1)]
      : null;
    renderTranslationDiagram(step, options);
    if (step) {
      selectedCodon = Math.min(p - 1, translationSteps.length - 1);
      renderReading(step);
      highlightProtein(step);
      setText('step-label', `CODÓN ${selectedCodon + 1} / ${translationSteps.length}`);
      const buttons = $('codons').querySelectorAll('.codon');
      buttons.forEach((button, i) => button.setAttribute('aria-pressed', i === selectedCodon ? 'true' : 'false'));
      $('previous').disabled = selectedCodon === 0;
      $('next').disabled = selectedCodon === translationSteps.length - 1;
    } else if (!translationSteps.length) {
      renderReading(null);
    }
  }

  renderNarration(stage);
  const max = stageMax(stage);
  const value = Math.min(player.progress[stage], max);
  const percent = max ? (value / max) * 100 : 0;
  $('animation-progress').style.width = `${percent}%`;
  setText('animation-counter', `${value} / ${max}`);
}

function stopPlayback() {
  player.playing = false;
  if (player.timer) window.clearTimeout(player.timer);
  player.timer = null;
  $('play-toggle').innerHTML = '▶ <span>Reproducir</span>';
  $('play-toggle').setAttribute('aria-label', 'Reproducir');
}

function scheduleTick() {
  if (!player.playing) return;
  const delay = Math.round(900 / player.speed);
  player.timer = window.setTimeout(() => {
    const stage = player.activeStage;
    const max = stageMax(stage);
    if (player.progress[stage] >= max) {
      stopPlayback();
      return;
    }
    player.progress[stage] += 1;
    renderActiveStage();
    scheduleTick();
  }, delay);
}

function togglePlayback() {
  if (!simulationData) return;
  if (player.playing) {
    stopPlayback();
    renderNarration(player.activeStage);
    return;
  }

  const stage = player.activeStage;
  if (player.progress[stage] >= stageMax(stage)) player.progress[stage] = 0;
  player.playing = true;
  $('play-toggle').innerHTML = 'Ⅱ <span>Pausar</span>';
  $('play-toggle').setAttribute('aria-label', 'Pausar');
  renderActiveStage();
  scheduleTick();
}

function stepForward() {
  if (!simulationData) return;
  stopPlayback();
  const stage = player.activeStage;
  const max = stageMax(stage);
  if (player.progress[stage] < max) player.progress[stage] += 1;
  renderActiveStage();
}

function resetActiveStage() {
  stopPlayback();
  player.progress[player.activeStage] = 0;
  renderActiveStage();
}

function setActiveStage(stage) {
  stopPlayback();
  player.activeStage = stage;
  for (const button of document.querySelectorAll('.stage-tab')) {
    const active = button.dataset.stage === stage;
    button.classList.toggle('active', active);
    button.setAttribute('aria-selected', active ? 'true' : 'false');
  }
  for (const panel of document.querySelectorAll('[data-stage-panel]')) {
    const active = panel.dataset.stagePanel === stage;
    panel.hidden = !active;
    panel.classList.toggle('active', active);
  }
  renderActiveStage();
}

for (const tab of document.querySelectorAll('.stage-tab')) {
  tab.addEventListener('click', () => setActiveStage(tab.dataset.stage));
}

$('play-toggle').addEventListener('click', togglePlayback);
$('step-forward').addEventListener('click', stepForward);
$('reset-animation').addEventListener('click', resetActiveStage);
$('animation-speed').addEventListener('change', event => {
  player.speed = Number(event.target.value) || 1;
  if (player.playing) {
    if (player.timer) window.clearTimeout(player.timer);
    scheduleTick();
  }
});

for (const [id, key] of [
  ['toggle-labels', 'showLabels'],
  ['toggle-enzymes', 'showEnzymes'],
  ['toggle-bonds', 'showBonds'],
  ['toggle-narration', 'narration']
]) {
  $(id).addEventListener('change', event => {
    player.options[key] = event.target.checked;
    renderActiveStage();
  });
}

function render(data) {
  simulationData = data;
  renderOverview(data);
  renderReplication(data);
  renderTranscription(data);
  renderTranslation(data);
  renderAssumptions(data);

  player.progress = { replication: 0, transcription: 0, translation: 0 };
  $('results').hidden = false;
  setActiveStage('replication');
  setText('announcement', `Simulación completada para ${data.dna.coding_5_3.length} bases. Usa los controles del explorador para recorrer cada proceso.`);
}

function setBusy(busy) {
  $('simulate').disabled = busy;
  $('sequence').disabled = busy;
  $('fragment-size').disabled = busy;
  for (const button of document.querySelectorAll('[data-sequence]')) button.disabled = busy;
  setText('simulate', busy ? 'Preparando simulación…' : 'Iniciar explorador');
}

$('form').addEventListener('submit', async event => {
  event.preventDefault();
  stopPlayback();
  $('error').hidden = true;
  $('results').hidden = true;

  const sequence = cleanSequence();
  const fragmentSize = Number.parseInt($('fragment-size').value, 10);

  if (!sequence) return showError('Introduce una secuencia de ADN.');
  if (sequence.length > 600) return showError('Utiliza como máximo 600 bases.');
  if (/[^ATCG]/.test(sequence)) return showError('La secuencia solo puede contener A, T, C y G.');
  if (!Number.isInteger(fragmentSize) || fragmentSize <= 0) return showError('El tamaño de Okazaki debe ser un entero positivo.');

  setBusy(true);
  try {
    const response = await fetch('/api/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sequence: $('sequence').value, fragment_size: fragmentSize })
    });
    let data;
    try {
      data = await response.json();
    } catch {
      throw new Error('El servidor devolvió una respuesta no válida.');
    }
    if (!response.ok) throw new Error(data.error || 'No se pudo realizar la simulación.');
    render(data);
  } catch (error) {
    showError(
      error instanceof TypeError
        ? 'No se puede conectar con Python. Comprueba que web_app.py sigue ejecutándose.'
        : error.message
    );
  } finally {
    setBusy(false);
  }
});

updateCount();
