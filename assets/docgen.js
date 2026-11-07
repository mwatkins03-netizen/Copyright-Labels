/* =====================================================================
   Campus Only Label · in-browser document generation
   Word (.docx) via docx 9.15.3 IIFE, PowerPoint (.pptx) via pptxgenjs 4.0.1, both loaded from
   jsDelivr on first use. PDF is a print-ready page (print.html). Runs entirely in the browser;
   fine on GitHub Pages. Depends on assets/label.js (window.COL).
   ===================================================================== */
(function (root) {
'use strict';
var C = root.COL;
var LIBS = {
  docx: 'https://cdn.jsdelivr.net/npm/docx@9.15.3/dist/index.iife.js',
  pptx: 'https://cdn.jsdelivr.net/npm/pptxgenjs@4.0.1/dist/pptxgen.bundle.js'
};
var loaded = {};
function loadLib (name) {
  if (loaded[name]) return loaded[name];
  loaded[name] = new Promise(function (res, rej) {
    var s = document.createElement('script'); s.src = LIBS[name]; s.async = true;
    s.onload = function () { res(); }; s.onerror = function () { delete loaded[name]; rej(new Error('Could not load ' + name + ' from the CDN')); };
    document.head.appendChild(s);
  });
  return loaded[name];
}
function badgeBytes (st) {
  return new Promise(function (res, rej) { C.badgePNG(st, 1320, function (blob) { if (!blob) return rej(new Error('badge')); blob.arrayBuffer().then(function (ab) { res(new Uint8Array(ab)); }); }); });
}
function badgeDataURL (st) {
  return new Promise(function (res, rej) { C.badgePNG(st, 1320, function (blob) { if (!blob) return rej(new Error('badge')); var r = new FileReader(); r.onload = function () { res(r.result); }; r.readAsDataURL(blob); }); });
}
function urlsFor (st) {
  var base = new URL('label.html', location.href); var code = C.encodeShort(st);
  var label = base.href + '#' + code; var p = new URL('label.html', location.href); p.search = '?prompt=1';
  return { label: label, prompt: p.href + '#' + code };
}
function placeholder (n) {
  var out = []; for (var i = 0; i < n; i++) out.push('Your own text goes here. The structure is what matters: where the label sits relative to what students read and the place they upload.');
  return out;
}

/* ---------------- Word ---------------- */
var DOCS = {
  syllabus: {
    file: 'syllabus-with-label.docx',
    title: function (st) { return 'Course syllabus'; },
    sub: function (st) { return (st.inst || '') + ' · ' + (st.holder || 'Instructor') + ' · ' + (st.year || ''); },
    box: ['Once, under your AI policy heading, with scope set to the whole course. Everything you hand out afterward inherits it.',
          'The one-line version is already in this document’s page footer. Students skim footers; AI tools read them.',
          'Keep the badge image and the small grey notice together: the image is for people, the grey text is what an AI reads.',
          'The “Ask your AI first” link is the most useful line for students. Say it out loud on day one.',
          'Make a separate No-AI label only for exams and student work.'],
    fill: 'FFF4C2', border: 'B8860B',
    body: function (st) { return [['Course description', placeholder(2)], ['Required texts', placeholder(1)], ['AI use and course materials', ['Each assignment carries its own AI-use rules that say what you may do. The materials for this course carry the label below, which says where they may go.'], 'LABEL'], ['Grading', placeholder(2)], ['Schedule', placeholder(2)]]; },
    scope: 'course'
  },
  assignment: {
    file: 'assignment-with-label.docx',
    title: function (st) { return st.title || 'Assignment'; },
    sub: function (st) { return (st.inst || '') + ' · ' + (st.holder || 'Instructor') + ' · Due date · Points'; },
    box: ['After the directions and before the submission instructions, so it is the last thing a student reads before uploading anything.',
          'If your syllabus already carries the whole-course label, this one is optional. Include it when the assignment travels on its own (a PDF, an email) or when its rule differs.',
          'The footer carries the one-line version so every printed or photographed page shows it.'],
    fill: 'FFF4C2', border: 'B8860B',
    body: function (st) { return [['The task', placeholder(1)], ['Requirements', placeholder(2)], ['Before you upload or paste this anywhere', [], 'LABEL'], ['Submission', ['Submit through the course site by the deadline.']]]; },
    scope: 'assignment'
  },
  exam: {
    file: 'exam-with-label.docx',
    title: function (st) { return st.title || 'Exam'; },
    sub: function (st) { return (st.inst || '') + ' · ' + (st.holder || 'Instructor') + ' · Due date'; },
    box: ['This is a separate No AI processing (L2) label. Do not reuse the course label here.',
          'Top of page one, before the first question, and in the footer of every page. A photographed page carries the footer in the frame.',
          'Use the same L2 label on peer-review packets and discussion exports: other students’ work is theirs.',
          'In testing, every Claude model and one of three GPT configurations declined to answer an L2-labeled exam; the rest did not. The label is a record and a request, not a lock.'],
    fill: 'FDE2E1', border: 'CC0605',
    body: function (st) { return [['', [], 'LABEL'], ['Instructions', ['Answer the questions below. Cite specific moves from the readings.']], ['Question 1', placeholder(1)], ['Question 2', placeholder(1)], ['Question 3', placeholder(1)]]; },
    scope: 'document'
  }
};

function wordFile (kind, stIn) {
  var spec = DOCS[kind]; if (!spec) return Promise.reject(new Error('unknown kind'));
  var st = Object.assign({}, stIn); if (kind === 'exam') { st.level = 2; st.scope = 'document'; st.note = ''; } else if (kind === 'syllabus') { st.scope = 'course'; } else if (st.scope === 'course') { st.scope = 'assignment'; }
  var urls = urlsFor(st); st.terms = st.terms || urls.label;
  return Promise.all([loadLib('docx'), badgeBytes(st)]).then(function (r) {
    var D = root.docx; var png = r[1];
    var INK = '18171c', GREY = '55555c';
    var W = 9360; // 6.5in
    function run (t, o) { return new D.TextRun(Object.assign({ text: t, font: 'Georgia', size: 22, color: INK }, o || {})); }
    function para (t, o, po) { return new D.Paragraph(Object.assign({ children: [run(t, o)], spacing: { after: 120 } }, po || {})); }
    function heading (t, size) { return new D.Paragraph({ children: [new D.TextRun({ text: t, bold: true, font: 'Arial', size: size || 32, color: INK })], spacing: { before: 280, after: 80 }, keepNext: true }); }
    function cellBorders (color, sz) { var b = { style: D.BorderStyle.SINGLE, size: sz, color: color }; return { top: b, bottom: b, left: b, right: b }; }
    function box (title, lines, fill, border) {
      var kids = [new D.Paragraph({ children: [new D.TextRun({ text: 'INSTRUCTIONS FOR FACULTY (delete this box before you share the document)', bold: true, font: 'Arial', size: 17, color: GREY })], spacing: { after: 60 } }),
                  new D.Paragraph({ children: [new D.TextRun({ text: title, bold: true, font: 'Arial', size: 24, color: INK })], spacing: { after: 80 } })];
      lines.forEach(function (ln) { kids.push(new D.Paragraph({ children: [new D.TextRun({ text: '• ' + ln, font: 'Arial', size: 20, color: INK })], spacing: { after: 40 } })); });
      return new D.Table({ width: { size: W, type: D.WidthType.DXA }, columnWidths: [W], rows: [new D.TableRow({ children: [new D.TableCell({ width: { size: W, type: D.WidthType.DXA }, shading: { fill: fill, type: D.ShadingType.CLEAR, color: 'auto' }, borders: cellBorders(border, 12), margins: { top: 120, bottom: 120, left: 160, right: 160 }, children: kids })] })] });
    }
    function labelBlock () {
      var u = C.universalText(st, urls).split('\n');
      var kids = [new D.Paragraph({ children: [new D.ImageRun({ type: 'png', data: png, transformation: { width: 400, height: 144 } })], spacing: { after: 100 } }),
                  new D.Paragraph({ children: [new D.TextRun({ text: u[0], bold: true, font: 'Arial', size: 22, color: INK })], spacing: { after: 80 } }),
                  para(u[1], { size: 21 }),
                  new D.Paragraph({ children: [new D.TextRun({ text: u[2].replace('  ·  ', '\n'), font: 'Georgia', size: 18, color: GREY })], spacing: { after: 120 } })];
      C.shortNotice(st).split('\n').forEach(function (ln) { kids.push(new D.Paragraph({ children: [new D.TextRun({ text: ln, font: 'Consolas', size: 15, color: GREY })], spacing: { after: 0 } })); });
      return new D.Table({ width: { size: W, type: D.WidthType.DXA }, columnWidths: [W], rows: [new D.TableRow({ children: [new D.TableCell({ width: { size: W, type: D.WidthType.DXA }, shading: { fill: 'F7F7F8', type: D.ShadingType.CLEAR, color: 'auto' }, borders: cellBorders(INK, 10), margins: { top: 120, bottom: 120, left: 160, right: 160 }, children: kids })] })] });
    }
    var children = [box('Where the label goes: ' + (kind === 'syllabus' ? 'syllabus' : kind === 'exam' ? 'exam or student work' : 'assignment sheet'), spec.box, spec.fill, spec.border), new D.Paragraph({ spacing: { after: 60 } }),
                    new D.Paragraph({ children: [new D.TextRun({ text: spec.title(st), bold: true, font: 'Arial', size: 40, color: INK })], spacing: { after: 60 } }),
                    para(spec.sub(st), { color: GREY })];
    spec.body(st).forEach(function (sec) {
      if (sec[0]) children.push(heading(sec[0]));
      sec[1].forEach(function (t) { children.push(para(t, { color: sec[1].length && t.indexOf('Your own text') === 0 ? GREY : INK })); });
      if (sec[2] === 'LABEL') { children.push(labelBlock()); children.push(new D.Paragraph({ spacing: { after: 60 } })); }
    });
    var footerText = 'CAMPUS ONLY LABEL ' + C.code(st) + ' · ' + C.LEVELS[st.level].name + ' (' + C.LEVELS[st.level].code + '). ' + C.studentLead(st) + (st.train === 0 ? ' No AI training.' : '') + ' Label: ' + urls.label;
    var doc = new D.Document({
      creator: st.holder || 'Instructor', title: spec.title(st), description: 'Campus Only Label ' + C.code(st),
      styles: { default: { document: { run: { font: 'Georgia', size: 22 } } } },
      sections: [{
        properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1300, right: 1440, bottom: 1300, left: 1440 } } },
        footers: { default: new D.Footer({ children: [new D.Paragraph({ children: [new D.TextRun({ text: footerText, font: 'Arial', size: 15, color: GREY })] })] }) },
        children: children
      }]
    });
    return D.Packer.toBlob(doc).then(function (blob) { return { blob: blob, name: C.fileName(st, 'docx').replace('.docx', '-' + kind + '.docx') }; });
  });
}

/* ---------------- PowerPoint ---------------- */
function pptxFile (stIn) {
  var st = Object.assign({}, stIn); var urls = urlsFor(st); st.terms = st.terms || urls.label;
  return Promise.all([loadLib('pptx'), badgeDataURL(st)]).then(function (r) {
    var P = root.PptxGenJS; var badge = r[1]; var pres = new P(); pres.layout = 'LAYOUT_WIDE';
    var INK = '18171C', GREY = '55555C', GREEN = '317F43', RED = 'CC0605';
    var lvl = C.LEVELS[st.level]; var u = C.universalText(st, urls).split('\n'); var shortN = C.shortNotice(st);
    function T (s, x, y, w, h, o) { s.addText(o.text, Object.assign({ x: x, y: y, w: w, h: h, fontFace: 'Arial', color: INK, isTextBox: true, margin: 0, valign: 'top' }, o)); }
    // instruction slide
    var s = pres.addSlide(); s.background = { color: 'FFF4C2' };
    T(s, 0.7, 0.5, 12, 0.4, { text: 'INSTRUCTIONS FOR FACULTY (delete this slide before you share the deck)', fontSize: 12, bold: true, color: GREY });
    T(s, 0.7, 1.0, 12, 0.9, { text: 'Where the label goes in a slide deck', fontSize: 32, bold: true });
    T(s, 0.7, 2.1, 12, 4.8, { text: [
      { text: 'Badge image in the footer of the title slide and the last slide (slides 2 and 4).', options: { bullet: true, breakLine: true } },
      { text: 'The two-sentence label as real text on the last slide, so it survives export to PDF and copy-and-paste.', options: { bullet: true, breakLine: true } },
      { text: 'The short notice to AI systems in the speaker notes of slide 2 and slide 4. Exported notes and file-reading AI tools see it; students in the room do not.', options: { bullet: true, breakLine: true } },
      { text: 'An image alone is the one layer an AI cannot reliably read, which is why the text and the notes matter more than the badge.', options: { bullet: true, breakLine: true } },
      { text: 'If you post the deck as a PDF, paste the one-line label into the footer of the export as well.', options: { bullet: true } }], fontSize: 18, paraSpaceAfter: 8 });
    // title slide
    s = pres.addSlide();
    T(s, 0.8, 0.6, 12, 0.4, { text: ((st.inst || '') + ' · ' + (st.holder || '')).toUpperCase(), fontSize: 14, bold: true, color: GREY });
    T(s, 0.8, 2.2, 11.5, 1.6, { text: st.title || 'Lecture title', fontSize: 54, bold: true });
    T(s, 0.8, 4.4, 8, 0.8, { text: 'Subtitle or week', fontSize: 24, color: GREY });
    s.addImage({ data: badge, x: 8.9, y: 6.0, w: 3.8, h: 3.8 * 0.36 });
    T(s, 0.8, 6.3, 7.8, 0.9, { text: C.studentLead(st) + ' Slides are copyrighted' + (st.train === 0 ? '; no AI training.' : '.'), fontSize: 11, color: GREY });
    s.addNotes('LABEL (students do not see this; AI tools reading the file do):\n' + C.universalText(st, urls));
    // content slide
    s = pres.addSlide();
    T(s, 0.8, 0.6, 12, 0.9, { text: 'Content slide', fontSize: 40, bold: true });
    [['Point one', INK], ['Point two', st.level === 2 ? RED : GREEN], ['Point three', INK]].forEach(function (c, i) {
      s.addShape(pres.ShapeType.rect, { x: 0.8 + i * 4.1, y: 2.0, w: 3.8, h: 0.9, fill: { color: c[1] }, line: { color: c[1] } });
      T(s, 0.95 + i * 4.1, 2.15, 3.5, 0.6, { text: c[0], fontSize: 22, bold: true, color: 'FFFFFF' });
      T(s, 0.8 + i * 4.1, 3.1, 3.8, 2.5, { text: 'Your content here.', fontSize: 16 });
    });
    T(s, 0.8, 6.9, 12, 0.4, { text: 'CAMPUS ONLY LABEL ' + C.code(st) + ' · ' + lvl.name + ' (' + lvl.code + '). ' + C.studentLead(st), fontSize: 9, color: GREY });
    // last slide
    s = pres.addSlide();
    T(s, 0.8, 0.6, 12, 0.9, { text: 'Before you take these slides anywhere', fontSize: 40, bold: true });
    s.addImage({ data: badge, x: 0.8, y: 1.9, w: 5.2, h: 5.2 * 0.36 });
    T(s, 6.4, 1.9, 6.2, 3.0, { text: u[0] + '\n' + u[1] + '\n' + u[2].replace('  ·  ', '\n'), fontSize: 14 });
    T(s, 0.8, 5.0, 11.8, 2.3, { text: shortN.split('\n').slice(0, 3).join('\n'), fontSize: 8, fontFace: 'Courier New', color: GREY });
    s.addNotes(C.universalText(st, urls));
    var name = C.fileName(st, 'pptx').replace('.pptx', '-slides.pptx');
    return pres.write({ outputType: 'blob' }).then(function (blob) { return { blob: blob, name: name }; });
  });
}

function saveResult (r) { C.download(r.name, r.blob); return r; }
root.COLDOC = { loadLib: loadLib, wordFile: wordFile, pptxFile: pptxFile, save: saveResult, urlsFor: urlsFor, kinds: Object.keys(DOCS) };
})(window);
