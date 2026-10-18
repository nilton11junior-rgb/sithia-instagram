"""Autoteste da validação do calendário (scripts/check.py). Rode: python3 -m pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from check import validar_post  # noqa: E402

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


def test_hashtags_acima_da_regra_viram_aviso():
    erros, avisos = _val(legenda="Gancho #sithia #a #b #c #d #e")
    assert erros == [] and any("hashtags" in a for a in avisos)


def test_id_repetido():
    vistos = {"teste-x"}
    assert any("repetido" in e for e in validar_post(dict(BASE), {}, vistos)[0])


def test_post_publicado_nao_exige_imagens():
    erros, _ = validar_post({**BASE, "imagem_capa": "nao/existe.jpg", "aprovado": True},
                            publicados={"teste-x": {}}, ids_vistos=set())
    assert erros == []


def test_hashtags_coladas_e_legenda_nao_texto():
    assert any("hashtags" in a for a in _val(legenda="G #sithia#a#b#c#d#e")[1])
    assert any("precisa ser texto" in e for e in _val(legenda=["x"])[0])
