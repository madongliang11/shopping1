from django.shortcuts import render

from apps.main.models import Navigation, Category, Banner


# @cache_page(7 * 60)
def index(request):
    nav_list = Navigation.objects.all()
    cate_list = Category.objects.all()
    banner_list = Banner.objects.all()
    for cate in cate_list:
        sub_menus = cate.submenu_set.all()
        for sub_menu in sub_menus:
            # [值，]
            sub_menu2 = sub_menu.submenu2_set.filter(sub_menu_id=sub_menu.sub_menu_id).values_list('name',flat=True)
            sub_menu.sub_menu2 = sub_menu2
        # 查询分类信息下的所有的商品信息
        shops = cate.shop_set.all()
        for shop in shops:
            # 查询商品的图片信息
            # values_list  [(626,),(647,)]
            #  单值   flat=True  [626,647]
            # [(626,1,'type'),]
            # values [{shop_img_id:626}]
            # shop.img = shop.image_set.values('shop_img_id').first()
            shop.img = shop.image_set.values_list('shop_img_id', flat=True).first()
            # shop.img = shop.image_set.values_list('shop_img_id', 'shop_id', 'type')
            print(shop.img)
        cate.shops = shops
        cate.sub_menus = sub_menus
    return render(request, 'index.html', locals())
