const SVG_NS = 'http://www.w3.org/2000/svg';

function svgNode(tag, attrs = {}, text = null) {
  const node = document.createElementNS(SVG_NS, tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, String(value));
  if (text !== null) node.textContent = text;
  return node;
}

function addText(svg, x, y, text, className = 'svg-label', anchor = 'start') {
  const node = svgNode('text', { x, y, class: className, 'text-anchor': anchor }, text);
  svg.append(node);
  return node;
}

function addMarker(svg, id, color) {
  let defs = svg.querySelector('defs');
  if (!defs) {
    defs = svgNode('defs');
    svg.prepend(defs);
  }
  const marker = svgNode('marker', {
    id, viewBox: '0 0 10 10', refX: 9, refY: 5,
    markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse'
  });
  marker.append(svgNode('path', { d: 'M 0 0 L 10 5 L 0 10 z', fill: color }));
  defs.append(marker);
}

function enzymeBox(svg, x, y, width, title, subtitle, color = '#2e7188') {
  svg.append(svgNode('rect', { x, y, width, height: 44, rx: 10, fill: color }));
  addText(svg, x + width / 2, y + 17, title, 'svg-enzyme', 'middle');
  addText(svg, x + width / 2, y + 31, subtitle, 'svg-enzyme-sub', 'middle');
}

function baseColor(base) {
  return {
    A: '#55c7e8',
    T: '#f5b85b',
    C: '#7fd18c',
    G: '#dd83b1',
    U: '#f08b68'
  }[base] || '#9fb4bd';
}

function drawBaseStrip(svg, sequence, activeIndex, y = 382, options = {}) {
  if (!sequence) return;
  const maxVisible = Math.min(sequence.length, 28);
  const start = Math.max(0, Math.min(sequence.length - maxVisible, activeIndex - Math.floor(maxVisible / 2)));
  const visible = sequence.slice(start, start + maxVisible);
  const cellWidth = 28;
  const totalWidth = visible.length * cellWidth;
  const x0 = (980 - totalWidth) / 2;

  visible.split('').forEach((base, i) => {
    const absoluteIndex = start + i;
    const active = absoluteIndex === activeIndex;
    svg.append(svgNode('rect', {
      x: x0 + i * cellWidth,
      y,
      width: 24,
      height: 25,
      rx: 6,
      fill: active ? baseColor(base) : '#183b47',
      stroke: active ? '#ffffff' : '#315765',
      'stroke-width': active ? 1.5 : 1
    }));
    addText(
      svg,
      x0 + i * cellWidth + 12,
      y + 17,
      base,
      active ? 'svg-enzyme' : 'svg-mono',
      'middle'
    );
  });

  if (options.showLabels !== false) {
    addText(svg, x0, y - 9, `bases ${start + 1}–${start + visible.length}`, 'svg-small');
  }
}

function clampProgress(progress) {
  return Math.max(0, Math.min(1, Number.isFinite(progress) ? progress : 0));
}

function renderReplicationDiagram(data, state = {}) {
  const container = document.getElementById('replication-visual');
  const showLabels = state.showLabels !== false;
  const showEnzymes = state.showEnzymes !== false;
  const showBonds = state.showBonds !== false;
  const progress = clampProgress(state.progress);
  const sequence = data.dna.coding_5_3;
  const activeIndex = Math.min(sequence.length - 1, Math.max(0, Math.floor(progress * sequence.length) - 1));

  container.replaceChildren();
  const svg = svgNode('svg', {
    viewBox: '0 0 980 430', role: 'img',
    'aria-label': 'Animación conceptual de una horquilla de replicación.'
  });
  addMarker(svg, 'rep-new', '#62d390');
  addMarker(svg, 'rep-parent', '#91a9b2');

  const forkX = 235 + progress * 410;
  const topY = 166;
  const bottomY = 244;

  if (showLabels) {
    addText(svg, 28, 28, 'REPLICACIÓN · horquilla en avance', 'svg-small');
    addText(svg, 885, 28, `${Math.round(progress * 100)} %`, 'svg-label', 'middle');
  }

  // ADN cerrado por delante de la horquilla.
  svg.append(
    svgNode('line', { x1: forkX, y1: topY, x2: 930, y2: topY, stroke: '#91a9b2', 'stroke-width': 4, 'stroke-linecap': 'round' }),
    svgNode('line', { x1: forkX, y1: bottomY, x2: 930, y2: bottomY, stroke: '#91a9b2', 'stroke-width': 4, 'stroke-linecap': 'round' })
  );
  if (showBonds) {
    for (let x = forkX + 20; x <= 915; x += 27) {
      svg.append(svgNode('line', { x1: x, y1: topY + 4, x2: x, y2: bottomY - 4, stroke: '#42606c', 'stroke-width': 1.5 }));
    }
  }

  // Hebras parentales separadas detrás de la horquilla.
  svg.append(
    svgNode('path', {
      d: `M ${forkX} ${topY} C ${forkX - 70} ${topY - 18} ${forkX - 105} 92 ${Math.max(65, forkX - 260)} 80 L 60 80`,
      fill: 'none', stroke: '#91a9b2', 'stroke-width': 4, 'stroke-linecap': 'round'
    }),
    svgNode('path', {
      d: `M ${forkX} ${bottomY} C ${forkX - 70} ${bottomY + 18} ${forkX - 105} 320 ${Math.max(65, forkX - 260)} 332 L 60 332`,
      fill: 'none', stroke: '#91a9b2', 'stroke-width': 4, 'stroke-linecap': 'round'
    })
  );

  // Hebra líder nueva.
  const leaderEnd = Math.max(105, forkX - 18);
  svg.append(svgNode('path', {
    d: `M 85 318 C 220 330 ${Math.max(280, forkX - 190)} 333 ${leaderEnd} ${bottomY + 4}`,
    fill: 'none', stroke: '#62d390', 'stroke-width': 5, 'stroke-linecap': 'round',
    'marker-end': 'url(#rep-new)'
  }));

  // Hebra rezagada: fragmentos visibles según el progreso.
  const fragments = data.replication.lagging_strand.okazaki_fragments;
  const maxPieces = Math.min(5, fragments.length);
  const visiblePieces = Math.max(0, Math.ceil(progress * maxPieces));
  for (let i = 0; i < visiblePieces; i++) {
    const right = forkX - 28 - i * 92;
    const left = Math.max(80, right - 68);
    const y = 111 - i * 5;
    svg.append(svgNode('line', {
      x1: right, y1: y, x2: left, y2: y - 12,
      stroke: '#62d390', 'stroke-width': 5, 'stroke-linecap': 'round',
      'marker-end': 'url(#rep-new)'
    }));
    svg.append(svgNode('line', {
      x1: right + 2, y1: y - 5, x2: right + 16, y2: y - 2,
      stroke: '#f5b85b', 'stroke-width': 6, 'stroke-linecap': 'round'
    }));
    if (showLabels) addText(svg, left + 15, y - 22, `Okazaki ${i + 1}`, 'svg-small');
  }

  if (showEnzymes) {
    enzymeBox(svg, forkX - 53, 184, 106, 'Helicasa', 'abre el ADN', '#2d758a');
    enzymeBox(svg, Math.max(85, forkX - 175), 36, 90, 'Primasa', 'cebadores', '#b47c2c');
    enzymeBox(svg, Math.max(90, forkX - 245), 132, 118, 'ADN polimerasa', 'hebra rezagada', '#43865f');
    enzymeBox(svg, Math.max(100, forkX - 210), 270, 118, 'ADN polimerasa', 'hebra líder', '#43865f');
    if (progress > .55) enzymeBox(svg, 105, 156, 88, 'Ligasa', 'une Okazaki', '#6d7f87');
  }

  if (showLabels) {
    addText(svg, 84, 61, '5′', 'svg-mono');
    addText(svg, 84, 354, '3′', 'svg-mono');
    addText(svg, 932, topY - 14, '3′', 'svg-mono', 'end');
    addText(svg, 932, bottomY + 24, '5′', 'svg-mono', 'end');
    addText(svg, 120, 295, 'hebra líder · síntesis continua 5′ → 3′', 'svg-label');
    addText(svg, 115, 136, 'hebra rezagada · síntesis discontinua', 'svg-label');
  }

  drawBaseStrip(svg, sequence, activeIndex, 389, { showLabels });
  container.append(svg);
}

function renderTranscriptionDiagram(data, state = {}) {
  const container = document.getElementById('transcription-visual');
  const showLabels = state.showLabels !== false;
  const showEnzymes = state.showEnzymes !== false;
  const showBonds = state.showBonds !== false;
  const progress = clampProgress(state.progress);
  const dna = data.dna.coding_5_3;
  const mrna = data.transcription.pre_mrna_5_3;
  const activeIndex = Math.min(dna.length - 1, Math.max(0, Math.floor(progress * dna.length) - 1));

  container.replaceChildren();
  const svg = svgNode('svg', {
    viewBox: '0 0 980 430', role: 'img',
    'aria-label': 'Animación conceptual de la transcripción del ADN a ARN.'
  });
  addMarker(svg, 'tx-rna', '#f5b85b');

  const polymeraseX = 250 + progress * 470;
  if (showLabels) {
    addText(svg, 28, 28, 'TRANSCRIPCIÓN · ARN polimerasa en avance', 'svg-small');
    addText(svg, 885, 28, `${Math.round(progress * 100)} %`, 'svg-label', 'middle');
  }

  // Promotor conceptual al inicio.
  svg.append(svgNode('rect', { x: 72, y: 92, width: 102, height: 38, rx: 8, fill: '#183c48', stroke: '#416875' }));
  if (showLabels) addText(svg, 123, 116, 'Promotor', 'svg-label', 'middle');

  // ADN.
  svg.append(
    svgNode('line', { x1: 60, y1: 160, x2: 925, y2: 160, stroke: '#91a9b2', 'stroke-width': 4, 'stroke-linecap': 'round' }),
    svgNode('line', { x1: 60, y1: 226, x2: 925, y2: 226, stroke: '#91a9b2', 'stroke-width': 4, 'stroke-linecap': 'round' })
  );

  if (showBonds) {
    for (let x = 82; x <= 905; x += 27) {
      if (Math.abs(x - polymeraseX) > 70) {
        svg.append(svgNode('line', { x1: x, y1: 164, x2: x, y2: 222, stroke: '#42606c', 'stroke-width': 1.4 }));
      }
    }
  }

  // Burbuja local alrededor de la polimerasa.
  svg.append(
    svgNode('path', { d: `M ${polymeraseX - 80} 160 Q ${polymeraseX} 110 ${polymeraseX + 80} 160`, fill: 'none', stroke: '#91a9b2', 'stroke-width': 4 }),
    svgNode('path', { d: `M ${polymeraseX - 80} 226 Q ${polymeraseX} 276 ${polymeraseX + 80} 226`, fill: 'none', stroke: '#91a9b2', 'stroke-width': 4 })
  );

  if (showEnzymes) {
    svg.append(svgNode('ellipse', { cx: polymeraseX, cy: 194, rx: 92, ry: 66, fill: '#2d758a' }));
    addText(svg, polymeraseX, 188, 'ARN POLIMERASA', 'svg-enzyme', 'middle');
    addText(svg, polymeraseX, 203, 'lee 3′→5′ · sintetiza 5′→3′', 'svg-enzyme-sub', 'middle');
  }

  // ARN naciente con longitud dependiente del progreso.
  const transcriptLength = Math.max(0, Math.ceil(progress * mrna.length));
  const rnaEndX = Math.min(860, polymeraseX + 80 + transcriptLength * 4);
  svg.append(svgNode('path', {
    d: `M ${polymeraseX + 8} 238 C ${polymeraseX + 35} 270 ${polymeraseX + 55} 294 ${rnaEndX} 304`,
    fill: 'none', stroke: '#f5b85b', 'stroke-width': 5, 'stroke-linecap': 'round',
    'marker-end': 'url(#tx-rna)'
  }));

  if (showLabels) {
    addText(svg, 65, 145, '5′', 'svg-mono');
    addText(svg, 65, 250, '3′', 'svg-mono');
    addText(svg, 915, 145, '3′', 'svg-mono');
    addText(svg, 915, 250, '5′', 'svg-mono');
    addText(svg, 205, 144, 'hebra codificante', 'svg-small', 'middle');
    addText(svg, 205, 249, 'hebra molde · lectura 3′ → 5′', 'svg-small', 'middle');
    addText(svg, rnaEndX, 329, `ARN naciente · ${transcriptLength}/${mrna.length} bases`, 'svg-label', 'end');
  }

  // Procesamiento como contexto cuando la transcripción está avanzada.
  if (progress > .78 && showLabels) {
    const labels = [['Cap 5′', 650], ['Splicing', 746], ['Cola poli-A', 842]];
    labels.forEach(([label, x]) => {
      svg.append(svgNode('rect', { x, y: 74, width: 82, height: 34, rx: 7, fill: '#503b24', stroke: '#8d6d3c' }));
      addText(svg, x + 41, 95, label, 'svg-small', 'middle');
    });
    addText(svg, 782, 56, 'procesamiento eucariota posterior', 'svg-small', 'middle');
  }

  drawBaseStrip(svg, mrna, activeIndex, 389, { showLabels });
  container.append(svg);
}

function renderTranslationDiagram(step, state = {}) {
  const container = document.getElementById('translation-visual');
  const showLabels = state.showLabels !== false;
  const showEnzymes = state.showEnzymes !== false;
  const showBonds = state.showBonds !== false;
  container.replaceChildren();

  const svg = svgNode('svg', {
    viewBox: '0 0 980 430', role: 'img',
    'aria-label': 'Ribosoma leyendo un codón de ARN mensajero con ARN de transferencia.'
  });
  addMarker(svg, 'tr-rna', '#f5b85b');
  if (showLabels) addText(svg, 28, 28, 'TRADUCCIÓN · lectura codón a codón', 'svg-small');

  // ARNm.
  svg.append(svgNode('line', {
    x1: 65, y1: 320, x2: 915, y2: 320, stroke: '#f5b85b', 'stroke-width': 6,
    'stroke-linecap': 'round', 'marker-end': 'url(#tr-rna)'
  }));
  if (showLabels) {
    addText(svg, 58, 346, '5′', 'svg-mono');
    addText(svg, 930, 346, '3′', 'svg-mono');
    addText(svg, 815, 299, 'ARNm · lectura 5′ → 3′', 'svg-small');
  }

  // Ribosoma.
  svg.append(
    svgNode('ellipse', { cx: 500, cy: 220, rx: 190, ry: 105, fill: '#173d49', stroke: '#4d7988', 'stroke-width': 2 }),
    svgNode('ellipse', { cx: 500, cy: 300, rx: 150, ry: 58, fill: '#1d4855', stroke: '#557e8c', 'stroke-width': 2 })
  );
  if (showLabels) addText(svg, 500, 155, 'ribosoma · ARNr + proteínas', 'svg-label', 'middle');

  if (!step) {
    addText(svg, 500, 80, 'No se encontró AUG: la traducción no comienza en este modelo.', 'svg-label', 'middle');
    container.append(svg);
    return;
  }

  // Codón actual.
  svg.append(svgNode('rect', { x: 461, y: 298, width: 78, height: 40, rx: 7, fill: '#5a4324', stroke: '#a87735' }));
  addText(svg, 500, 323, step.codon, 'svg-mono', 'middle');
  if (showLabels) addText(svg, 500, 370, `codón ${step.codon_number} · bases ${step.mrna_start_1_based}–${step.mrna_end_1_based}`, 'svg-small', 'middle');

  // Cadena acumulada.
  const peptide = step.peptide_after_step ? step.peptide_after_step.split('-') : [];
  if (showLabels) addText(svg, 92, 70, 'cadena polipeptídica naciente', 'svg-small');
  peptide.forEach((aa, index) => {
    const x = 110 + index * 58;
    if (index > 0) svg.append(svgNode('line', { x1: x - 39, y1: 108, x2: x - 19, y2: 108, stroke: '#bd8fab', 'stroke-width': 2 }));
    svg.append(svgNode('circle', { cx: x, cy: 108, r: 19, fill: '#6a4057', stroke: '#b7769b' }));
    addText(svg, x, 112, aa, 'svg-small', 'middle');
  });

  if (step.type === 'STOP') {
    if (showEnzymes) {
      svg.append(svgNode('rect', { x: 548, y: 82, width: 165, height: 74, rx: 13, fill: '#613b39', stroke: '#b9796e' }));
      addText(svg, 630, 111, 'FACTOR DE', 'svg-label', 'middle');
      addText(svg, 630, 130, 'TERMINACIÓN', 'svg-title', 'middle');
      addText(svg, 630, 146, 'reconoce la señal STOP', 'svg-small', 'middle');
    }
  } else {
    // ARNt esquemático.
    svg.append(svgNode('path', {
      d: 'M 545 84 C 520 98 520 128 540 145 C 518 160 522 188 545 203 L 560 235 C 568 251 590 251 598 235 L 614 203 C 638 188 640 158 618 145 C 638 128 634 98 607 86 C 589 78 570 93 579 111 C 568 94 554 80 545 84 Z',
      fill: '#36543e', stroke: '#79a783', 'stroke-width': 2
    }));
    svg.append(svgNode('circle', { cx: 579, cy: 64, r: 22, fill: '#b45c4f', stroke: '#dc8a78' }));
    addText(svg, 579, 68, step.amino_acid.abbreviation, 'svg-enzyme', 'middle');

    svg.append(svgNode('rect', { x: 536, y: 226, width: 86, height: 31, rx: 6, fill: '#17343f', stroke: '#5d818e' }));
    addText(svg, 579, 246, step.anticodon_3_5, 'svg-mono', 'middle');

    if (showBonds) {
      [552, 579, 606].forEach(x => svg.append(svgNode('line', {
        x1: x, y1: 258, x2: x, y2: 295, stroke: '#7f9da8', 'stroke-width': 1.4, 'stroke-dasharray': '3 3'
      })));
    }

    if (showLabels) {
      addText(svg, 665, 69, step.amino_acid.name, 'svg-small');
      addText(svg, 666, 244, 'anticodón', 'svg-small');
    }
  }

  container.append(svg);
}
