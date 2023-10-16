import json
from multiprocessing import context
import re
from datetime import date, datetime
from email import message
from urllib import request

from abacusai import PredictionClient
from django.contrib.messages import constants as messages
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

from . import services
from .models import Collection, NFT


class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        context = {}
        url = request.POST.get("url")
        # context['sales_data'] = services.get_nft_sales_eth(collection_name, token_id)

        try:
            collection_name, token_id = url_regex_extraction(url)
            context = services.get_nft_data(collection_name, token_id)

            data_for_prediction = {key.upper(): value for key, value in context.items()}
            attributes = [
                "BACKGROUND",
                "CLOTHES",
                "EYES",
                "FUR",
                "HAT",
                "MOUTH",
                "N_SALES",
                "AVG_PRICE_USD",
                "AVG_PRICE",
                "LAST_PRICE_USD",
            ]
            data_pr = {item: data_for_prediction[item] for item in attributes}
            client = PredictionClient()
            price_prediction = client.predict(
                deployment_token="8f732920581d40169bc059c2c999fcd5",
                deployment_id="5fe47ac30",
                query_data=data_pr,
            )
            predicted_price = price_prediction["LAST_PRICE"]
            context["predicted_price"] = round(predicted_price, 2)

            context["sales_data"] = services.get_nft_sales_eth(
                collection_name, token_id
            )

        except:
            context = {}
            predicted_price = False
        return render(request, self.template_name, context)


def url_regex_extraction(url):

    new_dict = {}
    new_dict = re.findall(
        "(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])",
        url,
    )

    return new_dict


def change_json_to_dict(json_data):
    """
    @return: list of dict
    """
    List_of_dict = []
    data = json.loads(json_data)
    for item in data:
        List_of_dict.append({item["DATE"]: item["PRICE"]})

    return List_of_dict


def prediction_price_from_abacus(deployment_id, context):
    try:
        data_for_prediction = {key: value for key, value in context.items()}
        data_for_prediction["Column_c0"] = '21'
        data_for_prediction["date"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        attributes = [
            "Column_c0",
            "date",
            "tokenid",
            "num_sales",
            "average_price",
            "last_sale",
        ]
        data_pr = {item: data_for_prediction[item] for item in attributes}
        client = PredictionClient()
        price_prediction = client.predict(
            deployment_token="8f732920581d40169bc059c2c999fcd5",
            deployment_id=deployment_id,
            query_data=data_pr,
        )
        # predicted_price = price_prediction['PRICE']
        predicted_price = price_prediction["price"]

        context["predicted_price"] = round(predicted_price, 2)
    except:
        pass

    return context


def get_traits_rarity(collection_name):
    collection_data = services.get_nft_ethereum_meta_data_with_dynamic_address(
        collection_name
    )

    rarity = {}
    if collection_data is not None:
        for nft_data in collection_data:
            for meta_data_key, meta_data_value in nft_data["token_metadata"].items():
                if meta_data_key not in rarity:
                    rarity[meta_data_key] = {}
                    rarity[meta_data_key][meta_data_value] = 1
                else:
                    if meta_data_value not in rarity[meta_data_key]:
                        rarity[meta_data_key][meta_data_value] = 1
                    else:
                        rarity[meta_data_key][meta_data_value] += 1

    for item in rarity:
        rarity[item] = {
            k: (v / len(collection_data)) * 100 for k, v in rarity[item].items()
        }

    return rarity


def get_proper_data_for_scatter_plot(data):
    sales_price = []
    index = 0
    for item in data:
        sales_price.append({})
        py_date = datetime.strptime(item["date"][:19], "%Y-%m-%dT%H:%M:%S")
        formatted_date = py_date.strftime("%m/%d/%Y")

        sales_price[index]["DATE"] = formatted_date
        sales_price[index]["PRICE"] = item["price"]
        if "label" in item:
            # for ETH
            sales_price[index]["LABEL"] = item["label"]
        else:
            # FOR Polygon and Avalanche
            sales_price[index]["LABEL"] = "sale"

        index += 1
    return json.dumps(sales_price)


def get_data_for_box_plot(collection_name):
    # only ETH
    data = services.get_box_plot_data_for_a_collection_algorand(collection_name)
    box_plot_data = []
    index = 0
    if data is not None:
        for item in data:
            box_plot_data.append({})
            py_date = datetime.strptime(item["date"][:19], "%Y-%m-%dT%H:%M:%S")
            formatted_date = py_date.strftime("%m/%d/%Y")

            box_plot_data[index]["x"] = formatted_date
            del item["date"]
            box_plot_data[index]["y"] = list(item.values())

            index += 1
    return json.dumps(box_plot_data)


def get_nft_feature(unknown_collections, collection_name, nft_asset_id):

    """get features of a NFT"""
    context = {}
    collection = Collection.objects.filter(collection_name=collection_name).first()

    # context.update(services.get_nft_data_for_eth(collection_name, token_id))
    context["tokenid"] = nft_asset_id

    context['sales_data'], context['sales_data_table'] = services.get_nft_sales_eth(collection_name, nft_asset_id)
    # (context["sales_data"], context["sales_data_table"],) = services.get_nft_sales_algorand(nft_asset_id)

    context["item_activity"] = services.get_activity_for_ethereum(collection_name, nft_asset_id)


    if context["item_activity"] is not None:
        context["scatter_plot_data"] = get_proper_data_for_scatter_plot(
            context["item_activity"]
        )

        if collection_name != context['item_activity'][0]['project_name']:
            collection_name = context['item_activity'][0]['project_name']
            unknown_collections = True
        else:
            context["image_url"] = services.get_nft_image_url(collection.name.lower().replace(" ", "_"), nft_asset_id)
            context['features'] =  services.get_nft_ethereum_meta_data(collection.name.lower().replace(" ", "_"), nft_asset_id)['token_metadata']

    if context["item_activity"] is None:
        collection_name = ''
        unknown_collections = True

    context["box_plot_data"] = get_data_for_box_plot(collection_name)

    context.update(
        services.get_ethereum_sales_data_dynamic_token_and_address(
            collection_name, nft_asset_id
        )
    )

    context['traits_rarity'] = get_traits_rarity(collection.name.lower().replace(" ", "_"))

    if not unknown_collections:
        context.update(
            prediction_price_from_abacus(collection.abacus_deployment_id, context)
        )  #
        context["image_name"] = collection.name.lower().replace(" ", "_")

    context["collection"] = collection
    context["show_nft"] = True

    # co
    context["blockchain"] = "eth"
    context['unknown_collections']= unknown_collections
    return context


class CollectionExplorer(TemplateView):
    template_name = "collection_explorer.html"

    def get(self, request):
        context = {}
        nft_asset_id = request.GET.get("nft_asset_id", None)
        collection_name = request.GET.get("collection_name", None)
        context["show_nft"] = False

        unknown_collections = False

        if nft_asset_id and collection_name:
            context["show_nft"] = True
            context.update(get_nft_feature(unknown_collections, collection_name, nft_asset_id))

            context["nft_asset_id"] = nft_asset_id
            context["contract_id"] = collection_name
            
        context["collections"] = Collection.objects.all()
        context["tokenid"] = nft_asset_id
        context["collection_name"] = collection_name
        context["today_date"] = json.dumps(date.today().strftime("%m/%d/%y"))
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        url = request.POST.get("url")
        collection_name = ""
        nft_asset_id = ""

        context["collections"] = Collection.objects.all()
        unknown_collections = False
        context["show_nft"] = False

        collection_id = request.POST.get("collection_id")
        if collection_id:
            collection_name = (
                Collection.objects.filter(id=collection_id).first().collection_name
            )
            nft_asset_id = request.POST.get("n_asset")


        context["tokenid"] = nft_asset_id

        if services.check_nft_in_flipside(collection_name, nft_asset_id):
            context.update(
                get_nft_feature(unknown_collections, collection_name, nft_asset_id)
            )
            context['error'] = False
            context["show_nft"] = True
        else:
            context['error'] = True

        context["nft_asset_id"] = nft_asset_id
        context["contract_id"] = collection_name
        context["today_date"] = date.today().strftime('%Y-%m-%dT%H:%M:%S%z')
        return render(request, self.template_name, context)


class RoadMapView(TemplateView):
    template_name = "roadmap.html"

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


class NftGalleryView(TemplateView):
    template_name = "gallery.html"

    def get(self, request):
        context = {}
        nft_data = request.GET
        nft_owner = nft_data.get("seller", None)
        nft_hash = nft_data.get("asset_hash", None)
        nft_id = nft_data.get("asset_id", None)
        nft_price = nft_data.get("asset_price", None)
        collection_name = nft_data.get("collection_name", None)
        if nft_id:
            obj, created = NFT.objects.get_or_create(
                asset_id = nft_id,
                owner = nft_owner,
                price = nft_price,
                hash = nft_hash,
                collection_name = collection_name,
            )
            if created:
                obj.save()
        
        context['nfts'] = NFT.objects.all()
        return render(request, self.template_name, context)
