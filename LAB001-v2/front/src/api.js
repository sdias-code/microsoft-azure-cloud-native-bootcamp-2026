const BASE_URL = '/api/photos'

async function handle(res) {
  if (!res.ok) {
    let detail = res.statusText
    try {
      const body = await res.json()
      if (body?.error) detail = body.error
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  if (res.status === 204) return null
  return res.json()
}

export async function listPhotos() {
  const res = await fetch(BASE_URL)
  return handle(res)
}

export async function createPhoto({ titulo, descricao, file }) {
  const form = new FormData()
  form.append('titulo', titulo)
  form.append('descricao', descricao)
  form.append('imagem', file)
  const res = await fetch(BASE_URL, { method: 'POST', body: form })
  return handle(res)
}

export async function updatePhoto(id, { titulo, descricao }) {
  const res = await fetch(`${BASE_URL}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ titulo, descricao }),
  })
  return handle(res)
}

export async function deletePhoto(id) {
  const res = await fetch(`${BASE_URL}/${id}`, { method: 'DELETE' })
  return handle(res)
}
