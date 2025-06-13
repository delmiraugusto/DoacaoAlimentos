import requests
from src.models.Endereco import Endereco
from src.repositories.EnderecoRepository import EnderecoRepository
from sqlalchemy.orm import Session

class EnderecoService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = EnderecoRepository(session)

    def listar_todos(self):
        return self.repo.get_all()

    def listar_por_id(self, endereco_id):
        endereco = self.repo.get_by_id(endereco_id)
        if not endereco:
            raise ValueError("Endereço não encontrado.")
        return endereco

    def obter_ou_criar_endereco_por_cep(self, cep: str) -> Endereco:
        cep = cep.replace("-", "").strip()
        if not cep:
            raise ValueError("CEP é obrigatório.")

        via_cep_resp = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if via_cep_resp.status_code != 200:
            raise ValueError("Erro ao consultar o CEP.")

        via_cep_data = via_cep_resp.json()
        if "erro" in via_cep_data:
            raise ValueError("CEP inválido.")

        cep_formatado = via_cep_data["cep"]

        existente = self.repo.get_by_cep(cep_formatado)
        if existente:
            return existente

        novo_endereco = Endereco(
            cep=cep_formatado,
            logradouro=via_cep_data["logradouro"],
            bairro=via_cep_data["bairro"],
            cidade=via_cep_data["localidade"],
            uf=via_cep_data["uf"]
        )
        return self.repo.add(novo_endereco)
    
    def obter_ou_atualizar_endereco(self, cep):
        if not cep:
            raise ValueError("CEP é obrigatório.")

        cep = cep.replace("-", "").strip()

        # busca no banco
        endereco = self.repo.get_by_cep(cep)
        if endereco:
            return endereco

        # via API
        via_cep_resp = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if via_cep_resp.status_code != 200:
            raise ValueError("Erro ao consultar o CEP.")

        via_cep_data = via_cep_resp.json()
        if "erro" in via_cep_data:
            raise ValueError("CEP inválido.")

        novo_endereco = Endereco(
            cep=via_cep_data["cep"],
            logradouro=via_cep_data["logradouro"],
            bairro=via_cep_data["bairro"],
            cidade=via_cep_data["localidade"],
            uf=via_cep_data["uf"]
        )

        self.repo.add(novo_endereco)
        return novo_endereco


    def atualizar_endereco(self, endereco_id, data):
        endereco = self.repo.get_by_id(endereco_id)
        if not endereco:
            raise ValueError("Endereço não encontrado.")

        if "cep" in data:
            endereco.cep = data["cep"]
        if "logradouro" in data:
            endereco.logradouro = data["logradouro"]
        if "bairro" in data:
            endereco.bairro = data["bairro"]
        if "cidade" in data:
            endereco.cidade = data["cidade"]
        if "uf" in data:
            endereco.uf = data["uf"]

        self.repo.update()
        return endereco

    def deletar_endereco(self, endereco_id):
        endereco = self.repo.get_by_id(endereco_id)
        if not endereco:
            raise ValueError("Endereço não encontrado.")
        self.repo.delete(endereco)
        return True
