"""Autoteste da validação do calendário (scripts/check.py). Rode: python3 -m pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from datetime import datetime  # noqa: E402

from check import avisar_fila, validar_post  # noqa: E402

BASE = {"id": "teste-x", "publicar_em": "2026-10-20T12:00:00-03:00", "aprovado": False,
        "legenda": "Gancho\n\n#sithia #a #b #c #d"}


def _val(**mudancas):
    return validar_post({**BASE, **mudancas}, publicados={}, ids_vistos=set())


def test_post_valido_passa():
    assert _val() == ([], [])


def test_data_sem_fuso_e_invalida():
    assert any("fuso" in e for e in _val(publicar_em="2026-10-20T12:00:00")[0])
    assert any("inválido" in e for e in _val(publicar_em="amanhã")[0])


def test_legenda_vazia_e_aprovado_nao_booleano():
    assert any("legenda vazia" in e for e in _val(legenda="  ")[0])
    assert any("true ou false" in e for e in _val(aprovado="sim")[0])


def test_imagem_inexistente_e_aprovado_sem_slides():
    erros, _ = _val(imagem_capa="criativos/fontes/nao-existe/capa.jpg", aprovado=True)
    assert any("imagem não encontrada" in e for e in erros)
    assert any("slides JPEG" in e for e in erros)


def test_mais_de_5_hashtags_e_erro():
    erros, _ = _val(legenda="Gancho #sithia #a #b #c #d #e")
    assert any("hashtags" in e for e in erros)


def test_id_repetido():
    vistos = {"teste-x"}
    assert any("repetido" in e for e in validar_post(dict(BASE), {}, vistos)[0])


def test_post_publicado_nao_exige_imagens():
    erros, _ = validar_post({**BASE, "imagem_capa": "nao/existe.jpg", "aprovado": True},
                            publicados={"teste-x": {}}, ids_vistos=set())
    assert erros == []


def test_hashtags_coladas_e_legenda_nao_texto():
    assert any("hashtags" in e for e in _val(legenda="G #sithia#a#b#c#d#e")[0])
    assert any("precisa ser texto" in e for e in _val(legenda=["x"])[0])


def test_fila_curta_avisa_e_fila_cheia_nao():
    agora = datetime.fromisoformat("2026-10-21T11:00:00-03:00")
    futuro = [{**BASE, "id": f"p{i}", "aprovado": True, "publicar_em": f"2026-10-2{i}T12:00:00-03:00"}
              for i in (2, 3)]
    assert avisar_fila(futuro, {}, agora) == []
    assert "só 1" in avisar_fila(futuro[:1], {}, agora)[0]
    assert "só 0" in avisar_fila([{**BASE, "aprovado": False}] + futuro[:0], {}, agora)[0]
    assert "só 1" in avisar_fila(futuro, {"p2": {}}, agora)[0]  # já publicado não conta
