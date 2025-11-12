from fastapi import APIRouter


class RecomendationRouter(APIRouter):
    def __init__(self):
        super().__init__()

        self.add_api_route("/", self.get_products, methods=["GET"])
        self.add_api_route("/load", self.load, methods=["GET"])

    async def get_recomendation(self):
        pass

    async def load(self):
        pass
