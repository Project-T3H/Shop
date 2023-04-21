from django.urls import path
from .views import *

urlpatterns = [
    path("", index),

    # =============== URL USER =====================
    path("register", UserView.register),
    path("login", UserView.login),
    path("list-user", UserView.list_user),
    path("list-manage", UserView.list_user_manage),
    path("list-customer", UserView.list_user_customer),
    path("logout", UserView.logout),
    path("search-user", UserView.search_user),
    path("update-user/<pk>", UserView.update_user),
    path("delete-user/<pk>", UserView.delete_user),
    path("create-user", UserView.create_user),
    # ===============================================

    # =============== URL SUPPLIER ===================
    path("create-supplier", SupplierView.create_supplier),
    path("list-supplier", SupplierView.list_supplier),
    path("search-supplier", SupplierView.search_supplier),
    path("update-supplier/<pk>", SupplierView.update_supplier),
    path("delete-supplier/<pk>", SupplierView.delete_supplier),
    # ================================================

    # =============== URL CATEGORY ===================
    path("create-category", CategoryView.create_category),
    path("list-category", CategoryView.list_category),
    path("search-category", CategoryView.search_category),
    path("get-category/<pk>", CategoryView.get_category_by_id),
    path("update-category/<pk>", CategoryView.update_category),
    path("delete-category/<pk>", CategoryView.delete_category),
    # ================================================

    # ============== URL BRANCH ======================
    path("create-branch", BranchView.create_branch),
    path("list-branch", BranchView.list_branch),
    path("update-branch/<pk>", BranchView.update_branch),
    path("delete-branch/<pk>", BranchView.delete_branch),
    # ================================================

    # ================= URL TICKET ===================
    path("list-ticketimport", TicketImportView.ticket_list),
    path("delete-ticketimport/<pk>", TicketImportView.delete_ticket),
    path("create-ticket", TickerAPIView.as_view()),
    path("create-ticket-import", TicketImportView.create_ticket_import),

    # ================================================

    # ============== URL TICKET DETAIL ===============
    path("create-ticketdetail", ImportDetailView.create_ticketdetail),
    path("ticketdetail/<pk>", ImportDetailView.ticketdetail_by_id),
    path("update-ticketdetail/<pk>", ImportDetailView.update_ticketdetail),
    path("delete-ticketdetail/<pk>", ImportDetailView.delete_ticketdetail),
    # ================================================

    # ============= URL PRODUCT ======================
    path("create-product", ProductView.create_product),
    path("list-product", ProductView.list_product),
    path("update-product/<pk>", ProductView.update_product),
    path("delete-product/<pk>", ProductView.delete_product),
    path("product-by-id/<pk>", ProductView.product_by_id),
    path("search-product", ProductView.search_product),
    path("filter", ProductView.filter_product),
    path("list-product-home", ProductView.list_product_home),
    path("list-product-shop", ProductView.list_product_shop),
    # =================================================

    # ============ URL PRODUCT DETAIL =================
    path("create-productdt", ProductDetailView.create_productdetail),
    path("update-productdt/<pk>", ProductDetailView.update_productdetail),
    path("delete-productdt/<pk>", ProductDetailView.delete_productdetail),
    # =================================================

    # ================== URL COLOR ====================
    path("list-color", ColorView.list_color),
    # =================================================

    # ================= URL SIZE ======================
    path("list-size", SizeView.list_size),
    # =================================================

    # ================= URL ORDER =====================
    path("create-order", OrderView.create_order),
    path("order-by-id/<pk>", OrderView.order_by_id),
    path("list-orders", OrderView.list_orders),
    path("update_order/<pk>", OrderView.update_orders),
    path("delete-order/<pk>", OrderView.delete_orders),
    path("search-order", OrderView.search_orders),
    # =================================================

    # ================= URL ORDER DETAIL ==============
    path("create-orderdetail", OrdersDetailView.create_orderdetail),
    path("update-orderdetail/<pk>", OrdersDetailView.update_orderdetail),
    path("delete-orderdetail/<pk>", OrdersDetailView.delete_orderdetail),
    path("list-orderdetailbyid/<pk>", OrdersDetailView.getlist_orderitemby_id),
    # =================================================
]