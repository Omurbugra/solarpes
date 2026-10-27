// Arayüz dili. Türkçe metinler data.js'te ve index.html'de durur; burada yalnızca İngilizceleri ve
// arayüz sözlüğü var. Dil seçimi tarayıcıda hatırlanır.
const UI = {
  tr: {
    docTitle: 'Enerji Renovasyon Senaryoları · SolarPES',
    brandSub: 'Okul enerji renovasyonu',
    kicker: 'Bir bakışta',
    h1: 'Enerji renovasyon senaryoları',
    lead: 'Model üzerinde bir sisteme gelin, parlasın; tıklayın, model o sisteme yaklaşsın. Yapısı ve dört indikatöre etkisi yanda açılır.',
    hint: 'Sürükle: döndür · Kaydır: yakınlaş · Tıkla: incele',
    stage: 'Okul 3B modeli',
    rot: 'Otomatik döndür', home: 'Başa dön', theme: 'Tema değiştir',
    systems: 'Sistemler', pins: 'İşaretler', pinsTitle: 'Model üzerindeki işaretler',
    prev: 'Önceki sistem', next: 'Sonraki sistem', close: 'Kapat',
    big: 'Detayı büyüt', bigClose: 'Büyük görünümü kapat',
    loading: 'Model yükleniyor', preparing: 'hazırlanıyor', failed: 'yüklenemedi',
    how: 'Nasıl çalışır', effects: 'Dört indikatöre etkisi', inspect: 'incele',
    miniLoading: 'Yükleniyor…', miniReal: 'Teknik detay · sürükle, döndür', miniPreview: 'Ön izleme · detay modeli eklenecek',
  },
  en: {
    docTitle: 'Energy Renovation Scenarios · SolarPES',
    brandSub: 'School energy retrofit',
    kicker: 'At a glance',
    h1: 'Energy renovation scenarios',
    lead: 'Hover a system on the model and it lights up; click and the model zooms in. Its build-up and its effect on the four indicators open on the side.',
    hint: 'Drag: orbit · Scroll: zoom · Click: inspect',
    stage: '3D model of the school',
    rot: 'Auto-rotate', home: 'Reset view', theme: 'Switch theme',
    systems: 'Systems', pins: 'Markers', pinsTitle: 'Markers on the model',
    prev: 'Previous system', next: 'Next system', close: 'Close',
    big: 'Enlarge detail', bigClose: 'Close large view',
    loading: 'Loading model', preparing: 'preparing', failed: 'failed to load',
    how: 'How it works', effects: 'Effect on the four indicators', inspect: 'inspect',
    miniLoading: 'Loading…', miniReal: 'Technical detail · drag to rotate', miniPreview: 'Preview · detail model to follow',
  },
};

const GROUPS_EN = { kabuk: 'Envelope', pasif: 'Passive', sistem: 'Systems', uretim: 'Generation' };
const INDICATORS_EN = { energy: 'Energy', emis: 'Emissions', cost: 'Cost', iod: 'Comfort' };
const EFF_EN = {
  'azalır': 'lower', 'çok azalır': 'much lower', 'az azalır': 'slightly lower', 'yüksek': 'high', 'orta': 'medium',
  'düşük': 'low', 'iyi': 'better', 'çok iyi': 'much better', 'kötüleşir': 'worse', 'nötr': 'neutral', 'etkisiz': 'no effect',
};

const FEATURES_EN = {
  wall: {
    tag: 'Envelope', title: 'Wall insulation',
    body: ['External walls are clad from the outside with EPS boards, finished with mesh, render and paint (ETICS).',
      'It cuts heating demand in winter and cooling demand in summer.'],
    how: 'It stops heat escaping through the large wall area. Because that area is large, the cost can be high.',
  },
  roof: {
    tag: 'Envelope', title: 'Roof insulation',
    body: ['The roof is the surface with the largest heat exchange. Mineral wool is laid on the top-floor slab, under the clay-tile roof.',
      'Applied on its own in this building, it is the envelope measure that removes the most overheating hours.'],
    how: 'A sun-heated roof passes heat into the rooms below; insulation largely blocks that flow.',
  },
  ground: {
    tag: 'Envelope · caution', title: 'Ground-floor insulation',
    body: ['In the slab on grade, 10 cm XPS boards are laid under the concrete slab, above a bitumen membrane, lean concrete and a crushed-stone bed.',
      'But in summer it cuts off the cooling effect of the ground, which can make classrooms even warmer.'],
    how: 'Helpful in winter, it can backfire in summer. It should be combined with roof insulation or shading.',
    warn: 'On its own it can make summer comfort worse.',
  },
  window: {
    tag: 'Envelope', title: 'Windows / insulated glazing',
    body: ['Double or triple glazing with argon fill and a low-e coating reduces heat transfer.',
      'Because good glazing also keeps heat inside in summer, its effect is balanced.'],
    how: 'The low-e coating reflects radiant heat. On its own the effect is limited; with shading it grows.',
  },
  shading: {
    tag: 'Passive', title: 'Solar shading',
    body: ['Horizontal overhangs on the south façade, vertical fins on the east and west. They stop the high summer sun before it reaches the glass.',
      'It works without using energy; its effect becomes clear in the 2050 climate.'],
    how: 'Using geometry alone, it keeps solar heat outside without consuming any energy.',
  },
  heatpump: {
    tag: 'System', title: 'Heat pump (VRF)',
    body: ['A single electric heat pump replaces the gas boiler and split air conditioners. Heat moves from the outdoor unit to the indoor units.',
      'It both heats and cools. A seasonal efficiency of about 3.4 is assumed, so one unit of electricity moves more than three units of heat.'],
    how: 'It moves heat with electricity instead of burning gas. As the grid gets cleaner (2050), the carbon advantage grows.',
  },
  pvroof: {
    tag: 'Generation', title: 'Rooftop solar panels',
    body: ['Panels on the south-facing roof slopes generate electricity from the sun.',
      'They cut the electricity bill and carbon. Combined with the heat pump, a larger share of the power is used on site.'],
    how: 'The electricity first covers the school’s own use. It has no direct effect on comfort.',
  },
  pvshade: {
    tag: 'Generation · passive', title: 'Solar shading panels',
    body: ['PV modules on the top floor of the south façade act as an overhang. They shade the windows from the high summer sun while generating power.',
      'Shading and generation in one element: a single investment instead of a separate canopy and a separate panel.'],
    how: 'The module tilt sets both the shadow depth and the yield. In winter the low sun passes underneath and warms the classroom.',
  },
  pvpark: {
    tag: 'Generation', title: 'Car-park solar canopy',
    body: ['A steel-framed PV canopy over the car park. It shades the cars, keeps the rain off and generates power.',
      'When roof area is limited, it is the easiest way to add generation; it pairs directly with EV charging.'],
    how: 'It is built without touching the building envelope. Generation overlaps school hours, so on-site use is high.',
  },
};

// Teknik detay etiketleri (details.json'daki numaralarla eşleşir)
const DETAILS_EN = {
  wall: { 1: 'Internal plaster 2 cm', 2: 'Brick wall 19 cm', 3: 'Adhesive mortar', 4: 'EPS insulation board 8 cm', 5: 'Insulation anchor',
    6: 'Glass-fibre mesh + base coat', 7: 'Decorative finish render', 8: 'Starter track' },
  roof: { 1: 'Concrete slab 15 cm', 2: 'Vapour control layer', 3: 'Mineral wool 2 × 7 cm', 4: 'Timber post and purlin', 5: 'Rafter 5×12 cm',
    6: 'OSB 18 mm', 7: 'Roofing membrane', 8: 'Battens and counter-battens', 9: 'Clay tile' },
  ground: { 1: 'Ceramic floor tile', 2: 'Screed 5 cm', 3: 'Concrete slab 15 cm', 4: 'PE separation layer', 5: 'XPS insulation 10 cm',
    6: 'Bitumen waterproofing', 7: 'Lean concrete 10 cm', 8: 'Crushed-stone bed 15 cm', 9: 'Compacted soil' },
  window: { 1: 'Multi-chamber PVC frame', 2: 'Galvanised steel reinforcement', 3: 'Sash profile', 4: 'Triple glazing 4-16-4-16-4',
    5: 'Argon-filled cavity', 6: 'Low-e coating', 7: 'Warm-edge spacer', 8: 'EPDM gasket', 9: 'Aluminium outer sill', 10: 'Insulation return at reveal' },
  shading: { 1: 'Aerofoil aluminium blades', 2: 'Steel bracket and tie rod', 3: 'Wall fixing plate', 4: 'Summer sun 73° — blocked',
    5: 'Winter sun 27° — let in', 6: 'Vertical fin (east/west)' },
  heatpump: { 1: 'Axial fan Ø550 + guard', 2: 'Finned heat exchanger (coil)', 3: 'Compressor bay / service panel', 4: 'Service valves',
    5: 'Copper refrigerant lines (liquid / gas)', 6: 'Rubber pipe insulation', 7: 'Anti-vibration mounts', 8: 'Concrete plinth' },
  pvroof: { 1: 'Monocrystalline PV module', 2: 'Tempered glass + cells', 3: 'Aluminium frame', 4: 'End clamp', 5: 'Aluminium mounting rail',
    6: 'Stainless roof hook', 7: 'Clay tile', 8: 'Rafter' },
  pvshade: { 1: 'PV module as overhang', 2: 'Steel cantilever arm', 3: 'Tie rod', 4: 'Wall plate (chemical anchors)',
    5: 'Cable duct → inverter', 6: 'Summer sun 73° — window shaded' },
  pvpark: { 1: 'PV modules (3 × 3)', 2: 'Galvanised C purlin', 3: 'IPE 270 cantilever beam', 4: 'HEA 200 column',
    5: 'Base plate + anchors', 6: 'Reinforced-concrete pad footing', 7: 'LED lighting' },
};

let lang = 'tr';
try { lang = localStorage.getItem('sp-lang') === 'en' ? 'en' : 'tr'; } catch {}
const listeners = [];

export const getLang = () => lang;
export const t = (k) => UI[lang][k] ?? UI.tr[k] ?? k;
export function setLang(l) {
  lang = l === 'en' ? 'en' : 'tr';
  try { localStorage.setItem('sp-lang', lang); } catch {}
  applyStatic();
  for (const fn of listeners) fn(lang);
}
export const onLang = (fn) => listeners.push(fn);

// Özellik (sistem) metinleri: Türkçe data.js'ten, İngilizce burada
export const feat = (f) => (lang === 'en' ? { ...f, ...FEATURES_EN[f.key] } : f);
export const groupName = (g) => (lang === 'en' ? GROUPS_EN[g.id] ?? g.name : g.name);
export const indicatorLabel = (k, tr) => (lang === 'en' ? INDICATORS_EN[k] ?? tr : tr);
export const effValue = (v) => (lang === 'en' ? EFF_EN[v] ?? v : v);
export const detailLabel = (key, n, tr) => (lang === 'en' ? DETAILS_EN[key]?.[n] ?? tr : tr);

// data-i18n="anahtar" metin; data-i18n-title / data-i18n-aria öznitelikleri
export function applyStatic() {
  document.documentElement.lang = lang;
  document.title = t('docTitle');
  for (const el of document.querySelectorAll('[data-i18n]')) el.textContent = t(el.dataset.i18n);
  for (const el of document.querySelectorAll('[data-i18n-title]')) el.title = t(el.dataset.i18nTitle);
  for (const el of document.querySelectorAll('[data-i18n-aria]')) el.setAttribute('aria-label', t(el.dataset.i18nAria));
  for (const b of document.querySelectorAll('[data-lang]')) b.setAttribute('aria-pressed', String(b.dataset.lang === lang));
}
