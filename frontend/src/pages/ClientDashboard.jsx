import { useState, useEffect } from 'react'
import { api } from '../api'
import Kot from '../components/Kot'

export default function LichnyiKabinet() {
  const [profil, setProfil] = useState({ nazvanie_kompanii: '', inn: '', vyruchka: 0, rashody: 0, dolgi: 0, stazh_let: 1 })
  const [profilId, setProfilId] = useState(null)
  const [rekomendacii, setRekomendacii] = useState(null)
  const [nastroenieKota, setNastroenieKota] = useState('hello')
  const [tekstKota, setTekstKota] = useState('Привет! Заполни данные о бизнесе, и я подберу кредит.')
  const [zayavkaId, setZayavkaId] = useState(null)
  const [statusZayavki, setStatusZayavki] = useState(null)

  const obrabotatOcr = async (e) => {
    const fail = e.target.files[0]; if (!fail) return
    setNastroenieKota('think'); setTekstKota('Смотрю документ...')
    const formDannye = new FormData(); formDannye.append('file', fail)
    try {
      const otvet = await api.post('/api/ocr/', formDannye)
      setProfil((p) => ({ ...p, inn: otvet.data.inn || p.inn, nazvanie_kompanii: otvet.data.nazvanie_kompanii || p.nazvanie_kompanii }))
      setNastroenieKota('advice'); setTekstKota('Данные распознаны!')
    } catch { setNastroenieKota('warn'); setTekstKota('Не удалось распознать.') }
  }

  const sohranitProfil = async () => {
    setNastroenieKota('think'); setTekstKota('Считаю...')
    const otvet = await api.post('/api/profiles/', profil)
    setProfilId(otvet.data.id)
    const r = await api.get(`/api/recommendations/${otvet.data.id}`)
    setRekomendacii(r.data)
    if (r.data.bezopasnaya_summa > 0) {
      setNastroenieKota('advice'); setTekstKota(`Безопасно взять до ${r.data.bezopasnaya_summa.toLocaleString()} ₽. Индекс: ${r.data.ball}/100.`)
    } else { setNastroenieKota('warn'); setTekstKota('Пока рискованно.') }
  }

  const podatZayavku = async (produkt) => {
    const summa = Math.min(rekomendacii.bezopasnaya_summa, produkt.max_summa) || 500000
    const otvet = await api.post('/api/applications/', { profil_id: profilId, produkt_id: produkt.id, zaproshennaya_summa: summa, srok_mesyacev: 12 })
    setZayavkaId(otvet.data.id); setStatusZayavki(otvet.data.status)
    setNastroenieKota('think'); setTekstKota('Отправил заявку. Жди проверки.')
  }

  useEffect(() => {
    if (!zayavkaId) return
    const t = setInterval(async () => {
      const otvet = await api.get(`/api/applications/${zayavkaId}`)
      setStatusZayavki(otvet.data.status)
      if (otvet.data.status === 'approved') { setNastroenieKota('happy'); setTekstKota('Ура! Кредит одобрен! 🎉') }
      else if (otvet.data.status === 'rejected') { setNastroenieKota('warn'); setTekstKota('К сожалению, отказ.') }
    }, 2000)
    return () => clearInterval(t)
  }, [zayavkaId])

  return (
    <div className="container">
      <h1>Умный кредитный кабинет</h1>
      <Kot nastroenie={nastroenieKota} tekst={tekstKota} />
      <div className="card">
        <h3>Данные бизнеса</h3>
        <input placeholder="Название" value={profil.nazvanie_kompanii} onChange={(e) => setProfil({...profil, nazvanie_kompanii: e.target.value})} />
        <input placeholder="ИНН" value={profil.inn} onChange={(e) => setProfil({...profil, inn: e.target.value})} />
        <input type="number" placeholder="Выручка" value={profil.vyruchka} onChange={(e) => setProfil({...profil, vyruchka: +e.target.value})} />
        <input type="number" placeholder="Расходы" value={profil.rashody} onChange={(e) => setProfil({...profil, rashody: +e.target.value})} />
        <input type="number" placeholder="Долги" value={profil.dolgi} onChange={(e) => setProfil({...profil, dolgi: +e.target.value})} />
        <input type="number" placeholder="Стаж (лет)" value={profil.stazh_let} onChange={(e) => setProfil({...profil, stazh_let: +e.target.value})} />
        <div style={{ marginBottom: 12 }}><label>Выписка ЕГРЮЛ (OCR): </label><input type="file" onChange={obrabotatOcr} /></div>
        <button className="btn" onClick={sohranitProfil}>Рассчитать</button>
      </div>
      {rekomendacii && (
        <div className="card">
          <h3>Рекомендации</h3>
          <p>Безопасная сумма: <b>{rekomendacii.bezopasnaya_summa.toLocaleString()} ₽</b></p>
          <p>Индекс: <b>{rekomendacii.ball}/100</b></p>
          {rekomendacii.produkty.map((p) => (
            <div key={p.id} style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8 }}>
              <span>{p.nazvanie} — {p.stavka}%</span>
              <button className="btn btn-secondary" onClick={() => podatZayavku(p)}>Оформить</button>
            </div>
          ))}
        </div>
      )}
      {statusZayavki && <div className="card"><h3>Заявка #{zayavkaId}</h3><p className={`status-${statusZayavki}`}>Статус: {statusZayavki}</p></div>}
    </div>
  )
}
