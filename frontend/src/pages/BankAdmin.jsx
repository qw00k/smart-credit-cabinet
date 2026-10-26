import { useState, useEffect } from 'react'
import { api } from '../api'

export default function AdminkaBanka() {
  const [zayavki, setZayavki] = useState([])
  const [proverki, setProverki] = useState({})

  const zagruzit = async () => { const otvet = await api.get('/api/applications/'); setZayavki(otvet.data) }
  useEffect(() => { zagruzit() }, [])

  const zapustitProverki = (id) => {
    setProverki((p) => ({ ...p, [id]: 'running' }))
    setTimeout(() => { setProverki((p) => ({ ...p, [id]: 'done' })) }, 1500)
  }
  const prinyatReshenie = async (id, reshenie) => { await api.post(`/api/applications/${id}/decision`, { reshenie, kommentarii: 'Решение' }); zagruzit() }

  return (
    <div className="container">
      <h1>Админка банка</h1>
      {zayavki.map((z) => (
        <div key={z.id} className="card">
          <b>Заявка #{z.id}</b> — сумма {z.zaproshennaya_summa.toLocaleString()} ₽, срок {z.srok_mesyacev} мес.
          <div>Статус: <span className={`status-${z.status}`}>{z.status}</span></div>
          <div style={{ marginTop: 8 }}>
            {proverki[z.id] === 'done' ? (
              <div style={{ color: '#38a169' }}>✅ ЕГРЮЛ<br />✅ БКИ<br />✅ ФНС</div>
            ) : (
              <button className="btn" disabled={proverki[z.id] === 'running'} onClick={() => zapustitProverki(z.id)}>{proverki[z.id] === 'running' ? 'Проверяем...' : 'Запустить проверки'}</button>
            )}
          </div>
          {proverki[z.id] === 'done' && z.status === 'pending' && (
            <div style={{ marginTop: 12, display: 'flex', gap: 8 }}>
              <button className="btn" onClick={() => prinyatReshenie(z.id, 'approved')}>Одобрить</button>
              <button className="btn btn-secondary" onClick={() => prinyatReshenie(z.id, 'rejected')}>Отказ</button>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
