from xml.dom.minidom import Document
from xml.dom import minidom
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import base64
from cart.models import CartItem
from cart import cart
from ecomstore import settings

def get_checkout_url(request):
    redirect_url = ''
    req = _create_google_checkout_request(request)
    try:
        response_xml = urlopen(req).read()
    except (HTTPError, URLError) as err:
        raise err
    else:
        redirect_url = _parse_google_checkout_response(response_xml)
    return redirect_url

def _create_google_checkout_request(request):
    url = settings.GOOGLE_CHECKOUT_URL
    cart_xml = _build_xml_shopping_cart(request)
    
    req = Request(url=url, data=cart_xml.encode('utf-8'))
    
    merchant_id = settings.GOOGLE_CHECKOUT_MERCHANT_ID
    merchant_key = settings.GOOGLE_CHECKOUT_MERCHANT_KEY
    key_id = f"{merchant_id}:{merchant_key}"
    
    authorization_value = base64.b64encode(key_id.encode('utf-8')).decode('utf-8')
    
    req.add_header('Authorization', f'Basic {authorization_value}')
    req.add_header('Content-Type', 'application/xml; charset=UTF-8')
    req.add_header('Accept', 'application/xml; charset=UTF-8')
    
    return req

def _parse_google_checkout_response(response_xml):
    redirect_url = ''
    xml_doc = minidom.parseString(response_xml)
    root = xml_doc.documentElement
    node = root.childNodes[1]
    
    if node.tagName == 'redirect-url':
        redirect_url = node.firstChild.data
    elif node.tagName == 'error-message':
        raise RuntimeError(node.firstChild.data)
    
    return redirect_url

def _build_xml_shopping_cart(request):
    doc = Document()
    root = doc.createElement('checkout-shopping-cart')
    root.setAttribute('xmlns', 'http://checkout.google.com/schema/2')
    doc.appendChild(root)

    shopping_cart = doc.createElement('shopping-cart')
    root.appendChild(shopping_cart)

    items = doc.createElement('items')
    shopping_cart.appendChild(items)

    cart_items = cart.get_cart_items(request)
    for cart_item in cart_items:
        item = doc.createElement('item')
        items.appendChild(item)

        item_name = doc.createElement('item-name')
        item_name_text = doc.createTextNode(str(cart_item.name))
        item_name.appendChild(item_name_text)
        item.appendChild(item_name)

        item_description = doc.createElement('item-description') 
        item_description_text = doc.createTextNode(str(cart_item.name)) 
        item_description.appendChild(item_description_text) 
        item.appendChild(item_description) 
        
        unit_price = doc.createElement('unit-price') 
        unit_price.setAttribute('currency','USD') 
        unit_price_text = doc.createTextNode(str(cart_item.price)) 
        unit_price.appendChild(unit_price_text) 
        item.appendChild(unit_price) 
        
        quantity = doc.createElement('quantity') 
        quantity_text = doc.createTextNode(str(cart_item.quantity)) 
        quantity.appendChild(quantity_text) 
        item.appendChild(quantity) 

    checkout_flow = doc.createElement('checkout-flow-support')
    root.appendChild(checkout_flow)

    merchant_flow = doc.createElement('merchant-checkout-flow-support')
    checkout_flow.appendChild(merchant_flow)

    shipping_methods = doc.createElement('shipping-methods')
    merchant_flow.appendChild(shipping_methods)

    flat_rate_shipping = doc.createElement('flat-rate-shipping')
    flat_rate_shipping.setAttribute('name', 'FedEx Ground')
    shipping_methods.appendChild(flat_rate_shipping)

    shipping_price = doc.createElement('price') 
    shipping_price.setAttribute('currency','USD') 
    flat_rate_shipping.appendChild(shipping_price) 
    
    shipping_price_text = doc.createTextNode('9.99') 
    shipping_price.appendChild(shipping_price_text) 

    return doc.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')
