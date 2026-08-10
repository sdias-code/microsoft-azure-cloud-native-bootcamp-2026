import { useCallback, useEffect, useState } from 'react'
import {
  createPhoto,
  deletePhoto,
  listPhotos,
  updatePhoto,
} from './api'
import './App.css'

const MAX_FILE_BYTES = 1 * 1024 * 1024

function formatDate(value) {
  if (!value) return ''
  return new Date(value).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function UploadForm({ onUploaded }) {
  const [titulo, setTitulo] = useState('')
  const [descricao, setDescricao] = useState('')
  const [file, setFile] = useState(null)
  const [error, setError] = useState(null)
  const [saving, setSaving] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError(null)

    if (!titulo.trim() || !file) {
      setError('O título e a imagem são obrigatórios.')
      return
    }
    if (file.size > MAX_FILE_BYTES) {
      setError(
        `Arquivo excede o limite de ${MAX_FILE_BYTES / (1024 * 1024)} MB. Escolha uma imagem menor.`,
      )
      return
    }

    setSaving(true)
    try {
      await createPhoto({ titulo: titulo.trim(), descricao, file })
      setTitulo('')
      setDescricao('')
      setFile(null)
      event.target.reset()
      onUploaded()
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <section className="upload-section">
      <form className="upload-form" onSubmit={handleSubmit}>
        <h2>Publicar nova foto</h2>
        <label>
          Título da Foto *
          <input
            type="text"
            value={titulo}
            onChange={(e) => setTitulo(e.target.value)}
            placeholder="Ex.: Pôr do sol na praia"
          />
        </label>
        <label>
          Descrição / Legenda
          <textarea
            value={descricao}
            onChange={(e) => setDescricao(e.target.value)}
            rows="2"
            placeholder="Conte um pouco sobre essa foto"
          />
        </label>
        <label>
          Selecione a Imagem (png, jpg, jpeg — máx. 1 MB) *
          <input
            type="file"
            accept="image/png,image/jpeg"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
        </label>
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={saving}>
          {saving ? 'Salvando...' : 'Salvar na Galeria'}
        </button>
      </form>
    </section>
  )
}

function EditForm({ photo, onSaved, onCancel }) {
  const [titulo, setTitulo] = useState(photo.titulo)
  const [descricao, setDescricao] = useState(photo.descricao ?? '')
  const [error, setError] = useState(null)
  const [saving, setSaving] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError(null)

    if (!titulo.trim()) {
      setError('O título não pode ficar vazio.')
      return
    }

    setSaving(true)
    try {
      await updatePhoto(photo.id, { titulo: titulo.trim(), descricao })
      onSaved()
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <section className="edit-section">
      <form className="upload-form" onSubmit={handleSubmit}>
        <h2>Editar foto</h2>
        <label>
          Novo Título *
          <input
            type="text"
            value={titulo}
            onChange={(e) => setTitulo(e.target.value)}
          />
        </label>
        <label>
          Nova Descrição
          <textarea
            value={descricao}
            onChange={(e) => setDescricao(e.target.value)}
            rows="2"
          />
        </label>
        {error && <p className="error">{error}</p>}
        <div className="row">
          <button type="submit" disabled={saving}>
            {saving ? 'Salvando...' : 'Salvar Alterações'}
          </button>
          <button type="button" className="secondary" onClick={onCancel}>
            Cancelar
          </button>
        </div>
      </form>
    </section>
  )
}

function PhotoCard({ photo, onEdit, onDelete }) {
  return (
    <div className="gallery-card">
      <img src={photo.imagemUrl} alt={photo.titulo} loading="lazy" />
      <h4>{photo.titulo}</h4>
      {photo.descricao && <p>{photo.descricao}</p>}
      <span className="date">{formatDate(photo.dataUpload)}</span>
      <div className="card-actions">
        <button className="secondary" onClick={() => onEdit(photo)}>
          Editar
        </button>
        <button className="danger" onClick={() => onDelete(photo)}>
          Excluir
        </button>
      </div>
    </div>
  )
}

function DeleteModal({ photo, onConfirm, onCancel }) {
  return (
    <div className="modal-overlay">
      <div className="modal">
        <h3>Excluir foto</h3>
        <p>
          Tem certeza que deseja excluir a foto{' '}
          <strong>"{photo.titulo}"</strong>? Esta ação não poderá ser desfeita.
        </p>
        <div className="row">
          <button className="danger" onClick={() => onConfirm(photo)}>
            Sim, excluir
          </button>
          <button className="secondary" onClick={onCancel}>
            Cancelar
          </button>
        </div>
      </div>
    </div>
  )
}

export default function App() {
  const [photos, setPhotos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [editing, setEditing] = useState(null)
  const [deleting, setDeleting] = useState(null)

  const loadPhotos = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      setPhotos(await listPhotos())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadPhotos()
  }, [loadPhotos])

  async function handleConfirmDelete(photo) {
    try {
      await deletePhoto(photo.id)
      setDeleting(null)
      await loadPhotos()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>Gerenciador de Fotos - Azure Cloud Native</h1>
      </header>

      <UploadForm onUploaded={loadPhotos} />

      {error && <p className="banner error">Erro: {error}</p>}

      <section className="gallery">
        <h2>Minhas Fotos na Nuvem</h2>
        {loading ? (
          <p className="muted">Carregando fotos...</p>
        ) : photos.length === 0 ? (
          <p className="muted">Nenhuma foto cadastrada na galeria.</p>
        ) : (
          <div className="gallery-grid">
            {photos.map((photo) => (
              <PhotoCard
                key={photo.id}
                photo={photo}
                onEdit={setEditing}
                onDelete={setDeleting}
              />
            ))}
          </div>
        )}
      </section>

      {editing && (
        <EditForm
          photo={editing}
          onSaved={async () => {
            setEditing(null)
            await loadPhotos()
          }}
          onCancel={() => setEditing(null)}
        />
      )}

      {deleting && (
        <DeleteModal
          photo={deleting}
          onConfirm={handleConfirmDelete}
          onCancel={() => setDeleting(null)}
        />
      )}
    </div>
  )
}
