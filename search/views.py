from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from search import search
from ecomstore import settings

def results(request, template_name="search/results.html"):
    # Lấy cụm từ tìm kiếm hiện tại
    q = request.GET.get('q', '')

    # Lấy số trang hiện tại. Đặt mặc định là 1 nếu không có hoặc không hợp lệ
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    # Lấy danh sách sản phẩm tương ứng
    matching = search.products(q).get('products')

    # Tạo đối tượng Paginator
    paginator = Paginator(matching, settings.PRODUCTS_PER_PAGE)

    try:
        # Lấy danh sách sản phẩm cho trang hiện tại
        results = paginator.page(page).object_list
    except (EmptyPage, PageNotAnInteger):
        # Trang không tồn tại hoặc là trang không hợp lệ, trả về trang đầu tiên
        results = paginator.page(1).object_list

    # Lưu thông tin tìm kiếm
    search.store(request, q)

    # Các biến thông thường...
    page_title = 'Kết quả tìm kiếm cho: ' + q
    context = {
        'results': results,
        'paginator': paginator,
        'page_title': page_title,
        'search_term': q,
    }

    return render(request, template_name, context)
