import streamlit as st

from config import MAX_FILE_MB

GALLERY_CSS = """
<style>
.gallery-grid {
    display: grid;
    gap: 16px;
    padding: 8px 0;
}
.gallery-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 10px;
    background: #fafafa;
    display: flex;
    flex-direction: column;
    min-width: 0;
}
.gallery-card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 6px;
}
.gallery-card h4 {
    margin: 8px 0 4px;
    font-size: 16px;
    color: #111;
    overflow-wrap: break-word;
}
.gallery-card p {
    margin: 0 0 4px;
    font-size: 13px;
    color: #555;
    overflow-wrap: break-word;
}
@media (min-width: 1200px) {
    .gallery-grid { grid-template-columns: repeat(4, 1fr); }
}
@media (min-width: 768px) and (max-width: 1199px) {
    .gallery-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 767px) {
    .gallery-grid { grid-template-columns: 1fr; }
}
</style>
"""


def render_upload_form():
    with st.form("form_foto", clear_on_submit=True):
        titulo_foto = st.text_input("Título da Foto")
        descricao_foto = st.text_area("Descrição / Legenda")
        uploaded_file = st.file_uploader(
            "Selecione a Imagem",
            type=["png", "jpg", "jpeg"],
            help=f"Tamanho máximo: {MAX_FILE_MB} MB",
        )
        submit = st.form_submit_button("Salvar na Galeria")
    return titulo_foto, descricao_foto, uploaded_file, submit


def render_gallery(photos):
    if photos:
        st.subheader("🖼️ Minhas Fotos na Nuvem")
        cards = []
        for photo in photos:
            cards.append(f"""
                <div class="gallery-card">
                    <h4>{photo['titulo']}</h4>
                    <p>{photo['descricao']}</p>
                    <img src="{photo['imagem_url']}" alt="{photo['titulo']}">
                </div>
            """)
        st.html(f"<div class='gallery-grid'>{''.join(cards)}</div>{GALLERY_CSS}")
    else:
        st.info("Nenhuma foto cadastrada na galeria.")


def render_edit_section(photos):
    st.subheader("✏️ Editar Foto")
    if not photos:
        st.info("Nenhuma foto disponível para edição.")
        return None

    opcoes = {p["id"]: f"{p['id']} - {p['titulo']}" for p in photos}
    id_selecionado = st.selectbox(
        "Selecione a foto",
        options=list(opcoes.keys()),
        format_func=lambda x: opcoes[x],
    )
    foto_edit = next((p for p in photos if p["id"] == id_selecionado), None)
    return foto_edit


def render_edit_fields(foto_edit):
    novo_titulo = st.text_input("Novo Título", value=foto_edit["titulo"])
    nova_descricao = st.text_area("Nova Descrição", value=foto_edit["descricao"])
    return novo_titulo, nova_descricao


def render_delete_confirmation(foto_edit):
    if st.button("🗑️ Excluir Foto", type="secondary"):
        st.session_state["confirmar_exclusao_id"] = foto_edit["id"]

    if st.session_state.get("confirmar_exclusao_id") == foto_edit["id"]:
        with st.form("form_confirmar_exclusao"):
            st.warning(
                f"Tem certeza que deseja excluir a foto '{foto_edit['titulo']}'? "
                "Esta ação não poderá ser desfeita."
            )
            c1, c2 = st.columns(2)
            with c1:
                confirmar = st.form_submit_button("✅ Sim, excluir", type="primary")
            with c2:
                cancelar = st.form_submit_button("Cancelar")

        if confirmar:
            st.session_state.pop("confirmar_exclusao_id", None)
            return "confirmar"
        if cancelar:
            st.session_state.pop("confirmar_exclusao_id", None)
            return "cancelar"
    return None
