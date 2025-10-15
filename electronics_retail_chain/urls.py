from electronics_retail_chain.apps import ElectronicsRetailChainConfig
from rest_framework.routers import SimpleRouter
from electronics_retail_chain.views import ProductViewSet, NetworkLinkViewSet

app_name = ElectronicsRetailChainConfig.name

router = SimpleRouter()

router.register("products", ProductViewSet)
router.register("networkolinks", NetworkLinkViewSet)

urlpatterns = [] + router.urls
