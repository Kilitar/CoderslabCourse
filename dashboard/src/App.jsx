import React, { useState, useEffect, useMemo } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, Legend, LineChart, Line, AreaChart, Area, 
  CartesianGrid, ScatterChart, Scatter, ZAxis
} from 'recharts';
import { motion, useScroll, useSpring, AnimatePresence, animate } from 'framer-motion';
import { 
  Shield, Ruler, History, Zap, UserCheck, Trophy, Target, Users, MapPin, Activity, Calendar, Search, BrainCircuit, Globe
} from 'lucide-react';
import data from './data.json';
import './index.css';

// --- ANIMATED COUNTER COMPONENT ---
const AnimatedCounter = ({ value, duration = 1, color }) => {
  const [displayValue, setDisplayValue] = useState(0);
  
  useEffect(() => {
    const controls = animate(0, value, {
      duration: duration,
      onUpdate: (latest) => setDisplayValue(Math.round(latest))
    });
    return () => controls.stop();
  }, [value, duration]);

  return <motion.span style={{ color }}>{displayValue}</motion.span>;
};

const COLORS = ['#e10600', '#b80500', '#900400', '#680300', '#400200'];

const Chapter = ({ id, question, label, children, insight }) => (
  <section id={id} className={`chapter story-container ${id === 'sandbox' ? 'full-width' : ''}`}>
    <motion.div initial={{ opacity: 0, y: 50 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: "-100px" }} transition={{ duration: 0.8, ease: "easeOut" }}>
      <span className="question-label">{label}</span>
      <h2 className="question-text">{question}</h2>
      <div className="ans-container">
        {children}
        {insight && <div className="insight-text">{insight}</div>}
      </div>
    </motion.div>
  </section>
);

const App = () => {
  const { task1, task2, task3, task4, task5, task6, task7, task8, task9, task10, task11, task12, task13, task14 } = data;
  const [activeChapter, setActiveChapter] = useState('intro');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFighter, setSelectedFighter] = useState(task13[0]);
  const [explorerSort, setExplorerSort] = useState('activity');
  const [isCalculating, setIsCalculating] = useState(false);
  
  // Predictor State
  const [predictMode, setPredictMode] = useState('name'); // 'name' or 'attributes'
  const [p1, setP1] = useState(task13[0]);
  const [p2, setP2] = useState(task13[1]);
  const [attr, setAttr] = useState({ p1Height: 70, p2Height: 70, p1Age: 28, p2Age: 28, p1Corner: 'Red' });

  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, { stiffness: 100, damping: 30 });

  const chapters = [
    { id: 'hero', label: 'Start', title: 'Vítejte' },
    { id: 'intro', label: 'Kapitola 1', title: 'Historický dosah' },
    { id: 'weight', label: 'Kapitola 2', title: 'Bojiště vah' },
    { id: 'lethality', label: 'Kapitola 3', title: 'Trend brutality' },
    { id: 'advantage', label: 'Kapitola 4', title: 'Klíč k vítězství' },
    { id: 'referees', label: 'Kapitola 5', title: 'Vliv rozhodčích' },
    { id: 'geography', label: 'Kapitola 6', title: 'Dobytí světa' },
    { id: 'peak', label: 'Kapitola 7', title: 'Fyzický vrchol' },
    { id: 'sandbox', label: 'Sandbox', title: 'Interaktivní nástroje' },
  ];

  useEffect(() => {
    const handleScroll = () => {
      const offsets = chapters.map(ch => ({ id: ch.id, top: document.getElementById(ch.id)?.offsetTop || 0 }));
      const current = offsets.reverse().find(off => window.scrollY >= off.top - 200);
      if (current) setActiveChapter(current.id);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Trigger calculation animation
  useEffect(() => {
    setIsCalculating(true);
    const timer = setTimeout(() => setIsCalculating(false), 1000);
    return () => clearTimeout(timer);
  }, [p1, p2, attr, predictMode]);

  const calculateProb = () => {
     let p1Score = 50;
     let p2Score = 50;

     if (predictMode === 'name') {
        const hDiff = (p1.h_total - p2.h_total);
        p1Score += hDiff * task14.height_inch;
        p2Score -= hDiff * task14.height_inch;
        p1Score += 10; // Red corner assumption for P1
     } else {
        const hDiff = (attr.p1Height - attr.p2Height);
        p1Score += hDiff * task14.height_inch;
        p2Score -= hDiff * task14.height_inch;
        if (attr.p1Corner === 'Red') p1Score += task14.red_corner;
        else p2Score += task14.red_corner;
        if (attr.p1Age >= 25 && attr.p1Age <= 30) p1Score += task14.age_prime;
        if (attr.p2Age >= 25 && attr.p2Age <= 30) p2Score += task14.age_prime;
     }

     const total = p1Score + p2Score;
     return Math.round((p1Score / total) * 100);
  };

  const prob = calculateProb();

  return (
    <div style={{ paddingBottom: '10vh' }}>
      <AnimatePresence>
        {activeChapter !== 'hero' && (
          <motion.header initial={{ y: -100 }} animate={{ y: 0 }} exit={{ y: -100 }} className="main-header">
            <div className="story-container header-content">
              <div className="brand">
                <img src="/logo.png" alt="UFC Data" className="header-logo" />
                <span>DATA ANALYTICS</span>
              </div>
              <div className="header-title">UFC Dashboard 2026</div>
            </div>
          </motion.header>
        )}
      </AnimatePresence>

      <motion.div style={{ scaleX, position: 'fixed', top: 0, left: 0, right: 0, height: '4px', background: 'var(--accent-red)', zIndex: 110, transformOrigin: '0%' }} />
      <div className="side-nav">
        {chapters.map(ch => <a key={ch.id} href={`#${ch.id}`} className={`nav-dot ${activeChapter === ch.id ? 'active' : ''}`} title={ch.title} />)}
      </div>

      {/* HERO SECTION */}
      <section id="hero" className="hero-section">
        <div className="hero-overlay" />
        
        {/* LOGO VISÍCÍ ZE STROPU */}
        <motion.img 
            initial={{ y: -100, opacity: 0 }} 
            animate={{ y: 0, opacity: 1 }} 
            transition={{ duration: 1.5, ease: "easeOut" }}
            src="/logo.png" 
            alt="UFC Logo" 
            className="hero-logo" 
        />

        {/* NÁPIS UPROSTŘED ARÉNY */}
        <div className="hero-content">
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }} 
            animate={{ opacity: 1, scale: 1 }} 
            transition={{ delay: 1, duration: 1.2 }}
          >
            <h1 className="hero-title">UMĚNÍ DAT V OKTAGONU</h1>
            <p className="hero-subtitle">Komplexní analýza historie, trendů a úspěchu v UFC</p>
          </motion.div>
        </div>

        <motion.div 
          animate={{ y: [0, 10, 0] }} 
          transition={{ repeat: Infinity, duration: 2 }}
          className="scroll-indicator"
        >
          <span>Začněte příběh</span>
          <Activity size={24} color="var(--accent-red)" />
        </motion.div>
      </section>

      <Chapter id="intro" label="Kapitola 1" question="Jak masivní je odkaz UFC po 30 letech?" insight={<p>Od roku 1994 se z UFC stala miliardová mašinérie. S <strong>{task1.unique_fighters.toLocaleString()}</strong> bojovníky a <strong>{task1.total_events}</strong> turnaji definuje moderní pojetí bojových sportů.</p>}>
        <div className="small-metrics">
          <div className="metric-item"><span className="metric-value">{task1.unique_fighters}</span><span className="metric-label">Bojovníků</span></div>
          <div className="metric-item"><span className="metric-value">{task1.total_events}</span><span className="metric-label">Eventů</span></div>
          <div className="metric-item"><span className="metric-value">{task1.oldest_fighter_age}</span><span className="metric-label">Věk nejstaršího</span></div>
        </div>
      </Chapter>

      <Chapter id="weight" label="Kapitola 2" question="Ve kterých vahách se píše historie?" insight={<p>Dominance lehké a velterové váhy není náhodná – tyto divize nabízejí nejširší pool talentů a největší frekvenci zápasů.</p>}>
        <ResponsiveContainer width="100%" height={450}>
          <BarChart data={task2} layout="vertical" margin={{ left: 30, right: 30 }}>
            <XAxis type="number" hide />
            <YAxis dataKey="name" type="category" width={140} tick={{ fill: '#8e8e93', fontSize: 11 }} interval={0} />
            <Tooltip contentStyle={{ background: '#111', border: '1px solid #333' }} />
            <Bar dataKey="value" fill="var(--accent-red)" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </Chapter>

      <Chapter id="lethality" label="Kapitola 3" question="Končí dnes více zápasů před limitem?" insight={<p>Statistiky ukazují, že sport technicky dospívá. I když KO tvoří <strong>{task3.ko_tko_percentage}%</strong> ukončení, průměrná délka zápasu se v čase prodlužuje.</p>}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '4rem' }}>
          <div>
            <h4 className="metric-label" style={{marginBottom: '1rem'}}>Distribuce způsobů ukončení</h4>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={task3.distribution} layout="vertical" margin={{ left: 20 }}>
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" width={100} tick={{ fill: '#8e8e93' }} />
                <Tooltip />
                <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                  {task3.distribution.map((e, i) => <Cell key={i} fill={i === 0 ? '#e10600' : i === 1 ? '#0a5cd2' : '#444'} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div>
            <h4 className="metric-label" style={{marginBottom: '1rem'}}>Průměrná délka vs. Síla úderu</h4>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={task8}>
                <CartesianGrid stroke="#222" vertical={false} />
                <XAxis dataKey="year" tick={{fill:'#666'}} />
                <YAxis yAxisId="L" hide />
                <YAxis yAxisId="R" orientation="right" hide />
                <Tooltip />
                <Line yAxisId="L" type="monotone" dataKey="ko_pct" stroke="#e10600" dot={false} strokeWidth={3} />
                <Line yAxisId="R" type="monotone" dataKey="avg_rounds" stroke="#0a5cd2" dot={false} strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </Chapter>

      <Chapter id="advantage" label="Kapitola 4" question="Je červený roh skutečně vítězný?" insight={<p>Data potvrzují "Defender Advantage". Červený roh (favorit/šampion) vyhrává v <strong>{task6.Red}%</strong> případů. Statistika výšky je sice zajímavá, ale roh je silnější prediktor.</p>}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem', textAlign: 'center' }}>
          <div className="card" style={{padding: '2rem'}}>
             <span className="stat-label" style={{display: 'block', marginBottom: '1rem'}}>Red Corner Win Rate</span>
             <span className="stat-value" style={{color:'#e10600', fontSize: '3rem', fontWeight: 800}}>{task6.Red}%</span>
          </div>
          <div className="card" style={{padding: '2rem'}}>
             <span className="stat-label" style={{display: 'block', marginBottom: '1rem'}}>Height Advantage Edge</span>
             <span className="stat-value" style={{color:'#0a5cd2', fontSize: '3rem', fontWeight: 800}}>{task7.height_advantage}%</span>
          </div>
        </div>
      </Chapter>

      <Chapter id="referees" label="Kapitola 5" question="Kdo jsou nejostřejší rozhodčí?" insight={<p>Rozhodčí nejsou jen statisté. John McCarthy nebo Larry Landless mají historicky nejvyšší poměr ukončení zápasů před limitem. Někteří rozhodčí zkrátka "nechávají bojovat" déle než jiní.</p>}>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={task11} margin={{ bottom: 50 }}>
            <XAxis dataKey="referee" angle={-45} textAnchor="end" height={80} tick={{fill:'#8e8e93', fontSize: 11}} />
            <YAxis tick={{fill:'#8e8e93'}} />
            <Tooltip contentStyle={{background:'#111'}} />
            <Bar dataKey="ko_pct" fill="#e10600" radius={[4, 4, 0, 0]} name="Míra ukončení (%)" />
          </BarChart>
        </ResponsiveContainer>
      </Chapter>

      <Chapter id="geography" label="Kapitola 6" question="Jak UFC dobylo svět?" insight={<p>Z Las Vegas do celého světa. UFC navštívilo již <strong>{task12.timeline[task12.timeline.length-1].countries}</strong> zemí. Největší expanze nastala po roce 2010.</p>}>
         <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={task12.timeline}>
              <XAxis dataKey="year" tick={{fill:'#666'}} />
              <YAxis tick={{fill:'#666'}} />
              <Tooltip />
              <Area type="stepAfter" dataKey="countries" stroke="#e10600" fill="rgba(225, 6, 0, 0.1)" strokeWidth={3} name="Počet zemí" />
            </AreaChart>
         </ResponsiveContainer>
      </Chapter>

      <Chapter id="peak" label="Kapitola 7" question="Kdy přichází vrchol sil?" insight={<p>Bojovník v UFC dosahuje vrcholu mezi <strong>25. a 29. rokem</strong>. V této fázi se potkává fyzická dravost s potřebnou zkušeností (alespoň 5+ zápasů).</p>}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
          <ResponsiveContainer width="100%" height={250}><BarChart data={task10}><XAxis dataKey="group" /><YAxis hide /><Bar dataKey="wins" fill="#e10600" /></BarChart></ResponsiveContainer>
          <ResponsiveContainer width="100%" height={250}><AreaChart data={task9}><XAxis dataKey="fight_num" /><YAxis hide /><Area dataKey="win_rate" stroke="#0a5cd2" fill="rgba(10, 92, 210, 0.1)" /></AreaChart></ResponsiveContainer>
        </div>
      </Chapter>

      {/* NEW SANDBOX SECTION */}
      <section id="sandbox" className="chapter story-container full-width" style={{background: 'rgba(255,255,255,0.01)', borderTop: '1px solid #222'}}>
        <div className="story-container">
           <span className="question-label">Interaktivní Laboratoř</span>
           <h2 className="question-text">Vyzkoušejte si sílu dat v praxi</h2>
           
           <div className="chart-grid">
              {/* Predictor */}
              <div className="card" style={{gridColumn: 'span 7', padding: '2rem', position: 'relative', overflow: 'hidden'}}>
                 
                 {/* Ongoing Fight Scanner Effect - ONLY WHEN CALCULATING */}
                 {isCalculating && <div className="ongoing-fight-scanner" style={{ '--active-color': prob > 50 ? 'var(--accent-red)' : '#0a5cd2' }} />}

                 <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: '2rem', position: 'relative', zIndex: 10}}>
                    <h3 className="chart-title" style={{display:'flex', alignItems:'center', gap:'0.5rem'}}>
                       <BrainCircuit size={20} /> Winner Predictor 
                       {isCalculating && <Activity size={16} className="heartbeat" color={prob > 50 ? 'var(--accent-red)' : '#0a5cd2'} />}
                    </h3>
                    <div className="toggle-group">
                       <button onClick={() => setPredictMode('name')} className={predictMode === 'name' ? 'active' : ''}>Jména</button>
                       <button onClick={() => setPredictMode('attributes')} className={predictMode === 'attributes' ? 'active' : ''}>Atributy</button>
                    </div>
                 </div>

                 <div style={{position: 'relative', zIndex: 10}}>
                    {predictMode === 'name' ? (
                       <div style={{display:'flex', gap:'2rem', alignItems: 'center'}}>
                          <div style={{flex:1, borderLeft: '4px solid var(--accent-red)', paddingLeft: '1.5rem'}}>
                             <span style={{fontSize: '0.7rem', color: 'var(--accent-red)', fontWeight: 800, letterSpacing: '2px'}}>RED CORNER</span>
                             <select value={p1.name} onChange={(e) => setP1(task13.find(f => f.name === e.target.value))} className="custom-select" style={{marginTop:'0.5rem'}}>
                                {task13.map(f => <option key={f.name} value={f.name}>{f.name}</option>)}
                             </select>
                             <p style={{fontSize:'0.8rem', color:'#666', marginTop:'0.5rem'}}>WR: {p1.win_rate}% | Height: {p1.h_total}"</p>
                          </div>
                          
                          <div style={{color:'#444', fontWeight: 800}}>VS</div>

                          <div style={{flex:1, borderRight: '4px solid #0a5cd2', paddingRight: '1.5rem', textAlign: 'right'}}>
                             <span style={{fontSize: '0.7rem', color: '#0a5cd2', fontWeight: 800, letterSpacing: '2px'}}>BLUE CORNER</span>
                             <select value={p2.name} onChange={(e) => setP2(task13.find(f => f.name === e.target.value))} className="custom-select" style={{marginTop:'0.5rem', textAlign: 'right'}}>
                                {task13.map(f => <option key={f.name} value={f.name}>{f.name}</option>)}
                             </select>
                             <p style={{fontSize:'0.8rem', color:'#666', marginTop:'0.5rem'}}>WR: {p2.win_rate}% | Height: {p2.h_total}"</p>
                          </div>
                       </div>
                    ) : (
                       <div style={{display:'grid', gridTemplateColumns: '1fr auto 1fr', gap:'2rem', alignItems: 'center'}}>
                          <div style={{borderLeft: '4px solid var(--accent-red)', paddingLeft: '1.5rem'}}>
                             <span style={{fontSize: '0.7rem', color: 'var(--accent-red)', fontWeight: 800, letterSpacing: '2px'}}>RED CORNER</span>
                          <div style={{display:'flex', justifyContent:'space-between', marginTop: '1rem'}}>
                             <label className="metric-label">Výška P1</label>
                             <span style={{fontSize:'0.8rem', color:'var(--accent-red)'}}>{attr.p1Height}" ({Math.round(attr.p1Height * 2.54)} cm)</span>
                          </div>
                          <input type="range" min="60" max="84" value={attr.p1Height} onChange={(e) => setAttr({...attr, p1Height: e.target.value})} style={{width:'100%', accentColor: 'var(--accent-red)'}} />
                          
                          <div style={{display:'flex', justifyContent:'space-between', marginTop: '0.5rem'}}>
                             <label className="metric-label">Věk P1</label>
                             <span style={{fontSize:'0.8rem', color:'var(--accent-red)'}}>{attr.p1Age} let</span>
                          </div>
                          <input type="range" min="18" max="45" value={attr.p1Age} onChange={(e) => setAttr({...attr, p1Age: e.target.value})} style={{width:'100%', accentColor: 'var(--accent-red)'}} />
                          </div>

                          <div style={{color:'#444', fontWeight: 800}}>VS</div>

                          <div style={{borderRight: '4px solid #0a5cd2', paddingRight: '1.5rem', textAlign: 'right'}}>
                             <span style={{fontSize: '0.7rem', color: '#0a5cd2', fontWeight: 800, letterSpacing: '2px'}}>BLUE CORNER</span>
                          <div style={{display:'flex', justifyContent:'space-between', marginTop: '1rem', flexDirection: 'row-reverse'}}>
                             <label className="metric-label">Výška P2</label>
                             <span style={{fontSize:'0.8rem', color:'#0a5cd2'}}>{attr.p2Height}" ({Math.round(attr.p2Height * 2.54)} cm)</span>
                          </div>
                          <input type="range" min="60" max="84" value={attr.p2Height} onChange={(e) => setAttr({...attr, p2Height: e.target.value})} style={{width:'100%', accentColor: '#0a5cd2'}} />
                          
                          <div style={{display:'flex', justifyContent:'space-between', marginTop: '0.5rem', flexDirection: 'row-reverse'}}>
                             <label className="metric-label">Věk P2</label>
                             <span style={{fontSize:'0.8rem', color:'#0a5cd2'}}>{attr.p2Age} let</span>
                          </div>
                          <input type="range" min="18" max="45" value={attr.p2Age} onChange={(e) => setAttr({...attr, p2Age: e.target.value})} style={{width:'100%', accentColor: '#0a5cd2'}} />
                          </div>
                       </div>
                    )}
                 </div>

                 <div style={{marginTop: '3.5rem', textAlign: 'center', position: 'relative', zIndex: 10}}>
                    <div style={{fontSize: '0.8rem', textTransform: 'uppercase', color: '#666', letterSpacing: '2px'}}>
                       {prob > 50 ? 'Pravděpodobnost výhry RED' : prob < 50 ? 'Pravděpodobnost výhry BLUE' : 'Vyrovnané šance'}
                    </div>
                    <div style={{fontSize: '5rem', fontWeight: 800, transition: 'color 0.5s ease', color: prob > 50 ? 'var(--accent-red)' : prob < 50 ? '#0a5cd2' : '#fff'}}>
                       <AnimatedCounter value={prob > 50 ? prob : 100 - prob} color="inherit" />%
                    </div>
                    <div style={{width: '100%', height: '16px', background: '#222', borderRadius: '8px', overflow: 'hidden', marginTop: '1rem', border: '1px solid #333'}}>
                       <motion.div 
                         animate={{ 
                           width: `${prob}%`,
                           background: prob > 50 ? 'var(--accent-red)' : '#0a5cd2'
                         }} 
                         transition={{ duration: 1 }}
                         style={{height: '100%'}} 
                       />
                    </div>
                 </div>
              </div>

              {/* Fighter Search */}
              <div className="card" style={{gridColumn: 'span 5', padding: '2rem'}}>
                 <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: '2rem'}}>
                    <h3 className="chart-title"><Search size={20} /> Fighter Explorer (Top 200)</h3>
                    <div className="toggle-group" style={{transform: 'scale(0.8)', transformOrigin: 'right'}}>
                       <button onClick={() => setExplorerSort('activity')} className={explorerSort === 'activity' ? 'active' : ''}>Aktivita</button>
                       <button onClick={() => setExplorerSort('success')} className={explorerSort === 'success' ? 'active' : ''}>Úspěch</button>
                    </div>
                 </div>
                 <div style={{position:'relative', marginBottom: '2rem'}}>
                    <input 
                      type="text" 
                      placeholder="Hledat bojovníka..." 
                      className="custom-input"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                    />
                 </div>
                 <div style={{maxHeight: '350px', overflowY: 'auto'}}>
                    {[...task13]
                       .sort((a,b) => explorerSort === 'activity' ? b.total_fights - a.total_fights : b.wins - a.wins)
                       .filter(f => f.name.toLowerCase().includes(searchTerm.toLowerCase())).map(f => (
                       <div key={f.name} className={`fighter-item ${selectedFighter?.name === f.name ? 'active' : ''}`} onClick={() => setSelectedFighter(f)}>
                          <span>{f.name}</span>
                          <span style={{fontSize:'0.7rem', color:'#666'}}>{f.wins}W - {f.losses}L</span>
                       </div>
                    ))}
                 </div>
                 {selectedFighter && (() => {
                    const sortedFighters = [...task13].sort((a,b) => explorerSort === 'activity' ? b.total_fights - a.total_fights : b.wins - a.wins);
                    const rank = sortedFighters.findIndex(f => f.name === selectedFighter.name) + 1;
                    return (
                       <motion.div initial={{opacity:0}} animate={{opacity:1}} style={{marginTop:'1.5rem', borderTop:'1px solid #333', paddingTop:'1rem', display: 'flex', alignItems: 'center', gap: '1.5rem'}}>
                          <div style={{
                             width: '50px', 
                             height: '50px', 
                             background: 'var(--accent-red)', 
                             borderRadius: '12px', 
                             display: 'flex', 
                             flexDirection: 'column',
                             alignItems: 'center', 
                             justifyContent: 'center',
                             boxShadow: '0 0 15px var(--accent-red-glow)'
                          }}>
                             <span style={{fontSize: '0.6rem', fontWeight: 800, opacity: 0.8}}>RANK</span>
                             <span style={{fontSize: '1.2rem', fontWeight: 800}}>#{rank}</span>
                          </div>
                          <div>
                             <p style={{fontSize:'1rem', fontWeight: 700}}>
                                <strong>{selectedFighter.name}</strong> 
                                <span style={{fontSize: '0.8rem', color: 'var(--accent-red)', marginLeft: '8px', opacity: 0.8}}>({selectedFighter.weight_class})</span>
                             </p>
                             <p style={{fontSize:'0.8rem', color:'#8e8e93'}}>
                                {explorerSort === 'activity' ? `Nejaktivnější: #${rank} / 200` : `Nejúspěšnější: #${rank} / 200`}
                             </p>
                             <p style={{fontSize:'0.75rem', color:'#666', marginTop: '4px'}}>Míra výher: {selectedFighter.win_rate}% | Height: {selectedFighter.h_total}"</p>
                          </div>
                       </motion.div>
                    );
                 })()}
              </div>
           </div>
        </div>
      </section>

      <footer className="story-container" style={{ padding: '4rem 0', textAlign: 'center', opacity: 0.5 }}>
        <p>UFC Super-Dashboard | Advanced Analysis 2026</p>
      </footer>
    </div>
  );
};

export default App;
