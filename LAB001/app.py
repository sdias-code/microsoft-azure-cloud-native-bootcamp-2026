import streamlit as st

from config import log, MAX_FILE_BYTES
from database import (
    insert_photo_metadata,
    update_photo_metadata,
    delete_photo_metadata,
    list_photos_from_sql,
)
from storage import upload_image_to_blob
from ui import (
    render_upload_form,
    render_gallery,
    render_edit_section,
    render_edit_fields,
    render_delete_confirmation,
)

st.set_page_config(page_title="Galeria Azure Cloud", page_icon="📸", layout="wide")
st.title("📸 Gerenciador de Fotos - Azure Cloud Native")

titulo_foto, descricao_foto, uploaded_file, submit = render_upload_form()

if submit:
    if not titulo_foto or not uploaded_file:
        st.warning("O título e a imagem são obrigatórios!")
    elif uploaded_file.size > MAX_FILE_BYTES:
        st.error(
            f"Arquivo excede o limite de {MAX_FILE_BYTES // (1024 * 1024)} MB "
            f"({uploaded_file.size / (1024 * 1024):.2f} MB). Escolha uma imagem menor."
        )
    else:
        with st.spinner("Processando upload e salvando metadados..."):
            try:
                url_gerada = upload_image_to_blob(uploaded_file)
            except Exception as e:
                log.exception("Erro no Blob Storage")
                st.error(f"Erro no Blob Storage: {e}")
                url_gerada = None

            if url_gerada:
                photo_data = {
                    "titulo": titulo_foto,
                    "descricao": descricao_foto,
                    "imagem_url": url_gerada,
                }
                try:
                    if insert_photo_metadata(photo_data):
                        st.success("Foto publicada com sucesso!")
                        st.rerun()
                except Exception as e:
                    log.exception("Erro ao salvar no Azure SQL")
                    st.error(f"Erro ao salvar no Azure SQL: {e}")

st.markdown("---")

try:
    photos = list_photos_from_sql()
except Exception as e:
    log.exception("Erro ao ler registros do banco")
    st.error(f"Erro ao ler registros do banco: {e}")
    photos = []

foto_edit = render_edit_section(photos)
if foto_edit:
    novo_titulo, nova_descricao = render_edit_fields(foto_edit)
    if st.button("💾 Salvar Alterações"):
        if not novo_titulo.strip():
            st.warning("O título não pode ficar vazio!")
        else:
            try:
                if update_photo_metadata(foto_edit["id"], novo_titulo.strip(), nova_descricao):
                    st.success("Foto atualizada com sucesso!")
                    st.rerun()
            except Exception as e:
                log.exception("Erro ao editar no Azure SQL")
                st.error(f"Erro ao editar no Azure SQL: {e}")

    acao_exclusao = render_delete_confirmation(foto_edit)
    if acao_exclusao == "confirmar":
        try:
            if delete_photo_metadata(foto_edit["id"]):
                st.success("Foto excluída com sucesso!")
                st.rerun()
        except Exception as e:
            log.exception("Erro ao excluir no Azure SQL")
            st.error(f"Erro ao excluir no Azure SQL: {e}")
    elif acao_exclusao == "cancelar":
        st.rerun()

st.markdown("---")
render_gallery(photos)
