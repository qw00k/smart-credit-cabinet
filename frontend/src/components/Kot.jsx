import catHello from '../assets/cat_hello.png'
import catThink from '../assets/cat_think.png'
import catAdvice from '../assets/cat_advice.png'
import catWarn from '../assets/cat_warn.png'
import catHappy from '../assets/cat_happy.png'

const NASTROENIYA = {
  hello:  { kartinka: catHello,  cvet: '#3182ce', nadpis: 'Приветствие' },
  think:  { kartinka: catThink,  cvet: '#d69e2e', nadpis: 'Думает' },
  advice: { kartinka: catAdvice, cvet: '#38a169', nadpis: 'Советует' },
  warn:   { kartinka: catWarn,   cvet: '#dd6b20', nadpis: 'Предупреждает' },
  happy:  { kartinka: catHappy,  cvet: '#38a169', nadpis: 'Радуется' },
}

export default function Kot({ nastroenie = 'hello', tekst = '', razmer = 120 }) {
  const n = NASTROENIYA[nastroenie] || NASTROENIYA.hello
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 16, background: '#fff', padding: 16, borderRadius: 12, borderLeft: `6px solid ${n.cvet}`, marginBottom: 16 }}>
      <img src={n.kartinka} alt={n.nadpis} style={{ width: razmer, height: razmer, objectFit: 'contain' }} />
      <div>
        <div style={{ fontSize: 12, color: n.cvet, fontWeight: 700, textTransform: 'uppercase' }}>{n.nadpis}</div>
        <div style={{ fontSize: 16, marginTop: 4 }}>{tekst}</div>
      </div>
    </div>
  )
}
